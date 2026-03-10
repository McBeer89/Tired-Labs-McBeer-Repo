# KQL Validator — Level 1 Implementation Plan

## Overview

Add a Python-based KQL syntax validator to the tooling suite. This validator runs against `.kql` files produced by the `kql-builder` agent and catches structural errors before commit — the same role `trr-prose-guard.sh` plays for TRR prose.

**Location:** `tools/kql-validator/`

---

## Why Level 1 Is Worth Having

KQL syntax errors are the most common failure mode when LLMs generate queries. The errors are always the same class: missing pipe operators, unclosed parentheses, SQL keywords used instead of KQL equivalents (`AND` instead of `and`), wrong clause ordering, bare strings without quotes. These are the errors that waste time when someone copies a query into Sentinel and gets a parse error on line 3.

Level 1 catches all of these instantly, locally, with zero infrastructure. Even if Level 3 (live workspace compilation) is available, Level 1 still runs first because it's faster and gives more specific error messages. A live workspace API returns "syntax error at line 5" — Level 1 returns "unclosed parenthesis opened at line 5, column 23" or "SQL keyword 'AND' used instead of KQL 'and' at line 5."

The cost is low: a Python script under 500 lines, no external dependencies beyond the standard library, runs in milliseconds.

---

## Compatibility with Levels 2 and 3

The three levels are strictly additive — each catches a different error class, and they chain naturally:

| Level | What It Validates | Dependencies | Error Class |
|-------|-------------------|--------------|-------------|
| **1 — Syntax** | Structural grammar, balanced delimiters, valid operators, table names against known mapping | None (Python stdlib) | "This isn't valid KQL" |
| **2 — Schema** | Field names and table names against `kql-environment-profile.md` | Populated environment profile | "This is valid KQL but references fields/tables your environment doesn't have" |
| **3 — Live** | Full compilation against a Log Analytics workspace API | Azure subscription, workspace credentials, network access | "This compiles but your workspace rejects it (permissions, missing functions, version issues)" |

**Design principle:** Each level is a separate Python module. The main entry point (`validate.py`) runs whichever levels are available. Level 1 always runs. Level 2 runs if the environment profile is populated. Level 3 runs if Azure credentials are configured. Each level returns a structured result; the pipeline aggregates them.

```
tools/kql-validator/
├── validate.py          ← CLI entry point — runs available levels, aggregates results
├── level1_syntax.py     ← Level 1: structural parsing (implement now)
├── level2_schema.py     ← Level 2: environment profile validation (future — stub only)
├── level3_live.py       ← Level 3: workspace API compilation (future — stub only)
├── kql_tables.py        ← Known table/telemetry mapping (extracted from kql-builder)
├── tests/
│   ├── test_level1.py   ← Unit tests with known-good and known-bad KQL
│   ├── good/            ← Valid .kql files for regression testing
│   └── bad/             ← Invalid .kql files with expected error annotations
└── README.md            ← Tool documentation + Level 2/3 upgrade notes
```

Level 1 does not interfere with Levels 2 or 3. When Level 2 is implemented, it imports `level1_syntax.py` and adds its own pass. When Level 3 is implemented, it imports both and adds the live check. The `validate.py` entry point handles orchestration:

```python
# Pseudocode for future multi-level flow
results = []
results.append(level1_syntax.validate(kql_text))       # always runs
if environment_profile_exists():
    results.append(level2_schema.validate(kql_text))    # runs if profile populated
if azure_credentials_configured():
    results.append(level3_live.validate(kql_text))      # runs if credentials exist
return aggregate(results)
```

---

## What Level 1 Checks

### 1. Statement Structure
- Every query statement begins with a table name or `let` binding, followed by pipe-separated operators
- Pipes (`|`) connect operators in sequence
- Multi-statement queries (separated by `;`) are each validated independently
- Comment-only lines (`//`) are allowed and skipped

### 2. Operator Keywords
Validate that pipe-separated tokens are recognized KQL operators:

`where`, `project`, `project-away`, `project-keep`, `project-rename`, `project-reorder`, `extend`, `summarize`, `join`, `union`, `let`, `count`, `distinct`, `sort`, `order`, `top`, `take`, `limit`, `render`, `mv-expand`, `mv-apply`, `parse`, `parse-where`, `evaluate`, `make-series`, `search`, `print`, `invoke`, `lookup`, `as`, `consume`, `fork`, `facet`, `getschema`, `sample`, `sample-distinct`, `serialize`, `range`

Flag unrecognized operators with a suggestion if a close match exists (e.g., `SELECT` → "Did you mean `project`?").

### 3. Balanced Delimiters
- Parentheses `()` — count opens vs. closes, report position of unclosed opener
- Square brackets `[]` — same
- Quoted strings `""` and `''` — detect unclosed strings, report line/position
- Respect escaping (`\"`, `\'`)

### 4. Common LLM Errors
These are specific patterns that LLMs (including Opus) commonly produce when generating KQL:

| Pattern | Problem | Fix |
|---------|---------|-----|
| `AND` / `OR` / `NOT` | SQL logical operators | `and` / `or` / `not` (KQL is lowercase) |
| `WHERE` / `SELECT` / `FROM` | SQL keywords | `where` / `project` / table name without `FROM` |
| `= ` (assignment in where) | SQL equality | `==` (KQL equality) |
| `!=` used correctly | — | (no fix needed — just don't flag it) |
| `LIKE` / `%` wildcards | SQL pattern matching | `has`, `contains`, `startswith`, `endswith`, `matches regex` |
| Missing `\|` between operators | Common omission | Flag: "Expected pipe operator between [op1] and [op2]" |
| `ago("24h")` | String instead of timespan | `ago(24h)` — timespan literals are unquoted |
| Trailing pipe with no operator | Incomplete query | Flag: "Trailing pipe with no operator" |
| `in ("a", "b")` | Wrong `in` syntax | `in ("a", "b")` is actually correct in KQL — don't flag |
| `timestamp` field | Common generic name | Flag only if table name is known and field doesn't exist |

### 5. Table Name Validation
Cross-reference the first token of each statement against the known telemetry-to-table mapping extracted from `kql-builder.md`. The mapping is codified in `kql_tables.py`:

```python
KNOWN_TABLES = {
    # Sentinel tables
    "SysmonEvent", "SecurityEvent", "W3CIISLog", "Event",
    "SigninLogs", "AuditLogs", "AADNonInteractiveUserSignInLogs",
    # Defender tables
    "DeviceProcessEvents", "DeviceFileEvents", "DeviceRegistryEvents",
    "DeviceImageLoadEvents", "DeviceNetworkEvents", "DeviceLogonEvents",
    "DeviceEvents",
    # Other common tables
    "Usage", "Heartbeat", "Perf", "Syslog",
}
```

If a table name isn't recognized, issue a **warning** (not an error) — it might be a custom table. Level 2 would promote this to an error if the table isn't declared in the environment profile.

### 6. Header Comment Validation
The `kql-builder` agent is instructed to produce a 2-3 line header comment on each query identifying the procedure ID, DDM operation, and telemetry source. Level 1 checks that:

- The first non-empty line starts with `//`
- The header mentions a TRR procedure ID pattern (`TRR\d{4}\.WIN\.[A-Z]`)
- The header mentions a DDM operation pattern (`n\d+` or `"Operation Name"`)

This is a warning, not an error — valid KQL doesn't require comments, but the pipeline convention does.

---

## Integration Points

### Option A: Step in `/kql` Command Pipeline (recommended)

Add a validation step between query generation and reviewer pass. In `/kql.md`, between Steps 4 and 5:

```markdown
### Step 4b: Validate Query Syntax

Run the KQL validator against all generated .kql files:

\```bash
python tools/kql-validator/validate.py "Completed TRR Reports/TRR####/win/kql/*.kql"
\```

If errors are found:
- Route the error report back to kql-builder with specific fix instructions
- Re-generate only the queries with errors
- Re-validate

If only warnings: include them in COVERAGE.md under a "Validation Notes" section.
```

This is the cleanest integration because it runs after generation, before review, and the errors are specific enough for the kql-builder to act on.

### Option B: PreToolUse Hook on .kql Writes (optional, later)

A hook like `kql-syntax-check.sh` could validate KQL files at write time, similar to `trr-prose-guard.sh`. The concern is performance — parsing KQL in a hook adds latency to every `.kql` file write. Recommended only if Level 1 validation in the pipeline proves insufficient (i.e., the kql-builder frequently writes invalid KQL that passes the pipeline step but fails on re-edits).

### Option C: Standalone CLI for Manual Use

Always available regardless of other integration:

```bash
# Validate a single file
python tools/kql-validator/validate.py path/to/file.kql

# Validate all .kql files in a directory
python tools/kql-validator/validate.py "Completed TRR Reports/TRR0016/win/kql/*.kql"

# Output format: JSON for pipeline consumption, text for human use
python tools/kql-validator/validate.py --format json path/to/file.kql
python tools/kql-validator/validate.py --format text path/to/file.kql
```

**Recommendation:** Implement Option A + C. Hook (Option B) deferred unless needed.

---

## Output Format

The validator returns structured results consumable by both humans and the pipeline:

```json
{
  "file": "trr0016_win_a.kql",
  "level": 1,
  "status": "FAIL",
  "errors": [
    {
      "line": 5,
      "column": 23,
      "severity": "error",
      "code": "L1-DELIM-001",
      "message": "Unclosed parenthesis opened at line 5, column 23",
      "suggestion": "Add closing parenthesis"
    },
    {
      "line": 8,
      "column": 1,
      "severity": "error",
      "code": "L1-KEYWORD-002",
      "message": "SQL keyword 'AND' used instead of KQL 'and'",
      "suggestion": "Replace 'AND' with 'and'"
    }
  ],
  "warnings": [
    {
      "line": 1,
      "column": 1,
      "severity": "warning",
      "code": "L1-TABLE-001",
      "message": "Table 'CustomTable_CL' not in known table list",
      "suggestion": "Verify table exists in your environment. Level 2 validation will check against the environment profile."
    }
  ]
}
```

Text output for CLI:

```
trr0016_win_a.kql: FAIL (2 errors, 1 warning)

  ERROR  L5:C23  L1-DELIM-001  Unclosed parenthesis
  ERROR  L8:C1   L1-KEYWORD-002  SQL keyword 'AND' — use 'and'
  WARN   L1:C1   L1-TABLE-001  Unknown table 'CustomTable_CL'
```

---

## Implementation Steps

### Step 1: Scaffold the Tool

Create the directory structure, `validate.py` entry point, `kql_tables.py` with the known table mapping, and stub modules for Levels 2 and 3.

**Coder subagent task.** Estimated: ~100 lines for scaffolding.

### Step 2: Implement Level 1 Core

Build `level1_syntax.py` with the checks described above. This is the bulk of the work:

- Tokenizer: split KQL into meaningful tokens (comments, strings, keywords, identifiers, operators, delimiters)
- Statement parser: validate pipe-chain structure
- Delimiter balancer: track opens/closes with positions
- LLM error detector: pattern match for common mistakes
- Table validator: check first token against `kql_tables.py`
- Header validator: check comment convention

**Coder subagent task.** Estimated: 300-400 lines.

### Step 3: Write Tests

Build test fixtures:
- `tests/good/` — valid KQL files extracted from real Sentinel/Defender queries. Include edge cases: multi-statement with `let`, `join` with inner queries, `union` across tables, `mv-expand`, `parse` operator.
- `tests/bad/` — invalid KQL files with known errors. Each file has a companion `.expected` file listing the expected error codes.
- `tests/test_level1.py` — pytest suite that validates good files pass and bad files produce the expected errors.

**Coder subagent task.** Estimated: ~200 lines of tests + ~20 fixture files.

### Step 4: Integrate into `/kql` Command

Add Step 4b to `/kql.md` as described in Integration Option A. Update the `kql-builder` agent definition to note that its output will be validated and to expect structured error reports for re-generation.

**Manual edit** to `.claude/commands/kql.md` and `.claude/agents/kql-builder.md`.

### Step 5: Document

Write `tools/kql-validator/README.md` with usage instructions, error code reference, and Level 2/3 upgrade path.

Update the project `README.md` to list the validator in the tooling section.

---

## Test Strategy

### Good KQL Fixtures (should PASS)

```kql
// Basic single-table query
DeviceProcessEvents
| where TimeGenerated > ago(24h)
| where FileName == "cmd.exe"
| project TimeGenerated, DeviceName, FileName, ProcessCommandLine

// Let binding + join
let suspicious = DeviceProcessEvents
| where InitiatingProcessFileName == "w3wp.exe";
suspicious
| join kind=inner (DeviceFileEvents | where ActionType == "FileCreated") on DeviceId
| project TimeGenerated, DeviceName, FileName

// Multi-statement
SecurityEvent
| where EventID == 4688
| where NewProcessName endswith "\\cmd.exe"
| summarize count() by Computer;
SecurityEvent
| where EventID == 4689
| project TimeGenerated, Computer

// Union
union DeviceProcessEvents, DeviceEvents
| where ActionType == "ProcessCreated"
| take 100
```

### Bad KQL Fixtures (should FAIL with specific errors)

```kql
// BAD: SQL keywords
SELECT TimeGenerated, DeviceName FROM DeviceProcessEvents WHERE FileName = 'cmd.exe'
// Expected: L1-KEYWORD-002 (SELECT), L1-KEYWORD-002 (FROM), L1-KEYWORD-002 (WHERE), L1-KEYWORD-003 (= instead of ==)

// BAD: Unclosed parenthesis
DeviceProcessEvents
| where (FileName == "cmd.exe" and InitiatingProcessFileName == "w3wp.exe"
| project TimeGenerated
// Expected: L1-DELIM-001 (unclosed paren at line 2)

// BAD: AND instead of and
DeviceProcessEvents
| where FileName == "cmd.exe" AND ProcessCommandLine has "whoami"
// Expected: L1-KEYWORD-002 (AND → and)

// BAD: Trailing pipe
DeviceProcessEvents
| where TimeGenerated > ago(24h)
|
// Expected: L1-STRUCT-001 (trailing pipe)

// BAD: ago() with string
DeviceProcessEvents
| where TimeGenerated > ago("24h")
// Expected: L1-FUNC-001 (ago() takes timespan, not string)
```

---

## Acceptance Criteria

Level 1 is done when:

- [ ] All good fixtures pass with zero errors
- [ ] All bad fixtures produce the expected error codes
- [ ] CLI works standalone: `python validate.py path/to/file.kql`
- [ ] JSON and text output formats both work
- [ ] Glob patterns work: `python validate.py "kql/*.kql"`
- [ ] `/kql` command includes validation step (Step 4b)
- [ ] `tools/kql-validator/README.md` documents usage, error codes, and Level 2/3 path
- [ ] Project `README.md` updated with validator in tooling section
- [ ] Level 2 and 3 stubs exist with docstrings explaining what they'll do
- [ ] Zero external dependencies — Python stdlib only

---

## Level 2 and 3: Future Upgrade Notes

### Level 2 — Schema Validation (implement when environment profile is populated)

**Trigger:** Fill in `kql-environment-profile.md` §2 (Available Log Sources) and §3 (Field Name Mappings). Once populated, Level 2 has something to validate against.

**What it adds:**
- Promotes "unknown table" from warning to error if the table isn't declared in the profile
- Validates every field name referenced in `where`, `project`, `extend`, `summarize` against the declared schema for that table
- Flags field names that exist but under a different name in the environment (uses §3 mappings)
- Checks that telemetry sources marked "No" in §2 don't have queries generated for them (this duplicates a kql-builder check, but defense in depth)

**Implementation:** `level2_schema.py` parses the environment profile markdown, builds an in-memory schema, and validates field references. Estimated: ~200 lines + environment profile parser.

**Dependency:** Populated `kql-environment-profile.md`. No external services.

### Level 3 — Live Workspace Compilation (implement when Azure infrastructure is available)

**Trigger:** Azure Log Analytics workspace accessible with API credentials. Production environment where you want to validate that queries compile against real data schemas.

**What it adds:**
- Submits each query to the [Log Analytics Query API](https://learn.microsoft.com/en-us/rest/api/loganalytics/dataaccess/query/execute) with `prefer: wait=0, ai.include-error-payload=true` to get compilation results without executing
- Catches errors that static analysis can't: missing workspace functions, permission issues, table schema version mismatches, custom function references
- Returns the workspace's error message alongside Level 1's structural analysis

**Implementation:** `level3_live.py` uses `requests` or `azure-identity` + `azure-monitor-query` SDK. Requires Azure credentials (service principal or managed identity). Estimated: ~150 lines + credential management.

**Dependency:** Azure subscription, Log Analytics workspace, API credentials configured (environment variable or Azure CLI login). Network access from the execution environment.

**Note:** Level 3 is the only level that requires network access and external credentials. Levels 1 and 2 are fully offline. In air-gapped or lab environments, Levels 1+2 provide the validation floor; Level 3 adds production confidence when infrastructure supports it.
