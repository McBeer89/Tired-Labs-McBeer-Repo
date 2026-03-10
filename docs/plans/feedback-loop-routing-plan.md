# Feedback Loop Routing — Implementation Plan

## The Problem

When the reviewer returns FAIL, the current commands say "Fix all critical issues. Re-run reviewer." But what actually happens is one of two things:

1. **The orchestrator tries to fix everything itself** — which means Opus-as-orchestrator is doing ddm-builder work and trr-writer work inline, without the specialized agent context. It works sometimes, but the fixes are lower quality than what the specialized agent would produce.

2. **You read the verdict and manually decide what to do** — which is the right call for hard judgment calls, but wastes your time on mechanical fixes like "replace bare telemetry label on line 47."

The goal is to route mechanical fixes automatically while escalating judgment calls to you.

---

## How It Works Today

```
/trr Phase 3:
  orchestrator spawns reviewer
    reviewer returns FAIL with critical issues [C1], [C2], [C3]
      orchestrator reads the issues
        ??? (no structured routing — orchestrator improvises)
          orchestrator re-runs reviewer
            if PASS: proceed
            if FAIL again: ??? (no retry limit — depends on orchestrator behavior)
```

The reviewer's output has critical issues with descriptions like:

```markdown
- **[C1]** README.md:L47 -- Detection language: "provides visibility" in Procedure B narrative
- **[C2]** ddms/ddm_trr0030_win.json:n7 -- Inclusion test: "Download Payload" fails immutability
- **[C3]** README.md -- Scope statement is two sentences
```

These are human-readable, but the orchestrator has to *interpret* each one to figure out what to do. There's no structured routing.

---

## Design

### Principle: Route Mechanical Fixes, Escalate Judgment Calls

Every reviewer finding falls into one of two categories:

**Mechanical** — the fix is deterministic. Bare telemetry label, detection language phrase, scope statement too long, missing DDM file reference, wrong arrow color. A subagent can fix these with the issue description alone. No judgment required.

**Judgment** — the fix requires analytical decision-making. An operation's inclusion test verdict is disputed, a procedure distinction is questionable, a technical claim in the background section needs verification. These need either deeper research or your input.

The routing system should handle mechanical fixes autonomously and surface judgment calls to you.

### Architecture

Three changes, each buildable independently:

1. **Enhanced reviewer output** — add `route_to` and `category` to each issue
2. **New `/resolve-review` command** — reads a reviewer verdict, routes fixes, re-reviews
3. **Integration into `/trr` and `/ddm`** — replace "Fix all critical issues" with conditional routing

---

## Change 1: Enhanced Reviewer Output

### What Changes in `reviewer.md`

The reviewer's JSON verdict block gains a `routed_issues` array. The existing markdown report stays identical — this is additive, not a format change.

**Current output:**

```json
{
  "verdict": "FAIL",
  "critical_count": 3,
  "warning_count": 1,
  "blocking": true
}
```

**Enhanced output:**

```json
{
  "verdict": "FAIL",
  "critical_count": 3,
  "warning_count": 1,
  "blocking": true,
  "routed_issues": [
    {
      "id": "C1",
      "severity": "critical",
      "category": "detection_language",
      "route_to": "trr-writer",
      "fix_type": "mechanical",
      "file": "README.md",
      "location": "Procedure B narrative, line 47",
      "description": "Uses 'provides visibility' — discipline-neutrality violation (FM1)",
      "fix_instruction": "Restate as telemetry fact. Replace 'provides visibility into process creation' with 'This operation produces Sysmon 1 (ProcessCreate) telemetry.'"
    },
    {
      "id": "C2",
      "severity": "critical",
      "category": "inclusion_test",
      "route_to": "ddm-builder",
      "fix_type": "judgment",
      "file": "ddms/ddm_trr0030_win.json",
      "location": "Node n7 'Download Payload'",
      "description": "Fails immutability test — delivery method is attacker-controlled",
      "fix_instruction": "Remove node n7 and its relationships. Reassess what the first essential operation is after delivery. May require trr-researcher input to determine the correct entry point."
    },
    {
      "id": "C3",
      "severity": "critical",
      "category": "scope_condensation",
      "route_to": "trr-writer",
      "fix_type": "mechanical",
      "file": "README.md",
      "location": "Scope section",
      "description": "Scope statement is two sentences (FM8)",
      "fix_instruction": "Condense to one sentence. Current: 'This TRR covers X. It focuses on Y.' → 'This TRR covers X focused on Y.'"
    }
  ]
}
```

### New Fields

| Field | Values | Purpose |
|-------|--------|---------|
| `route_to` | `trr-writer`, `ddm-builder`, `trr-researcher`, `orchestrator` | Which agent should fix this |
| `fix_type` | `mechanical`, `judgment` | Can this be auto-routed or does it need human review? |
| `category` | See table below | Maps to the 9 known failure modes + general categories |

### Category Mapping

| Category | Failure Mode | Typical Route | Typical Fix Type |
|----------|-------------|---------------|-----------------|
| `detection_language` | FM1 | trr-writer | mechanical |
| `rewalked_pipeline` | FM2 | trr-writer | mechanical |
| `grouped_telemetry` | FM3 | ddm-builder | mechanical |
| `bare_telemetry_label` | FM4 | trr-writer or ddm-builder | mechanical |
| `prerequisite_modeling` | FM5 | ddm-builder | judgment |
| `instance_procedure_confusion` | FM6 | orchestrator (needs research) | judgment |
| `verbose_overview` | FM7 | trr-writer | mechanical |
| `scope_condensation` | FM8 | trr-writer | mechanical |
| `telemetry_enablement` | FM9 | trr-writer | mechanical |
| `inclusion_test` | — | ddm-builder or trr-researcher | judgment |
| `naming` | — | ddm-builder | mechanical |
| `structure` | — | ddm-builder | mechanical |
| `accuracy` | — | varies | varies |
| `file_reference` | — | trr-writer | mechanical |

### Routing Rules for the Reviewer

Add these to the reviewer agent definition:

```markdown
## Routing Rules

When producing the `routed_issues` array:

**Route to `trr-writer`** when the fix involves:
- Prose changes in README.md (detection language, scope statement, overview length, re-walked pipeline, telemetry presentation)
- Exclusion table condensation
- DDM image reference mismatches in markdown

**Route to `ddm-builder`** when the fix involves:
- DDM JSON changes (node properties, arrow colors, telemetry labels, node removal/addition, relationship changes)
- Procedure table corrections in Supporting Docs

**Route to `trr-researcher`** when the fix requires:
- Additional information not present in current research notes
- Verification of a technical claim
- Resolving a disputed inclusion test verdict with primary sources

**Route to `orchestrator`** when:
- The fix requires a scoping decision (in/out of scope judgment)
- Multiple agents need coordinated changes (e.g., DDM change that cascades to prose)
- The issue is `fix_type: judgment` and involves procedure distinctness or boundary cases

**Mark `fix_type: mechanical`** when:
- The fix instruction is specific enough that the target agent can execute it without additional context
- No analytical judgment is required — it's a find-and-replace, a removal, or a reformulation

**Mark `fix_type: judgment`** when:
- The fix requires analyzing whether something is essential/immutable/observable
- The fix could change the DDM structure or procedure count
- The fix depends on information the reviewer doesn't have
- Multiple valid fixes exist and someone needs to choose
```

---

## Change 2: New `/resolve-review` Command

### File: `.claude/commands/resolve-review.md`

```markdown
---
description: Auto-route reviewer FAIL fixes to the appropriate subagents, then re-review. Max one automatic retry — escalates to user on second FAIL.
argument-hint: "<TRR ID> [platform - default: win]"
---

# Resolve Review: $ARGUMENTS

Auto-fix reviewer findings for:

> **$ARGUMENTS**

This command reads the most recent reviewer verdict, routes mechanical fixes
to the appropriate subagents, and re-runs the reviewer. It does NOT handle
judgment calls — those are surfaced to you for decision.

---

### Step 1: Find the Reviewer Verdict

Read the most recent reviewer output. Check (in order):
1. Was a reviewer verdict returned in the current session? (check conversation context)
2. Is there a review report in `Supporting Docs/`?

If no verdict found, run `/review $ARGUMENTS` first, then proceed.

Parse the `routed_issues` array from the JSON verdict block.

If the verdict is already PASS or PASS_WITH_NOTES, report that and stop.

---

### Step 2: Triage Issues

Separate the issues into three buckets:

**Bucket A — Mechanical fixes (auto-route):**
All issues where `fix_type` is `mechanical`.
Group by `route_to` target.

**Bucket B — Judgment calls requiring research:**
Issues where `fix_type` is `judgment` AND `route_to` is `trr-researcher`.

**Bucket C — Judgment calls requiring user decision:**
Issues where `fix_type` is `judgment` AND `route_to` is `orchestrator`.
Also: any issue where `route_to` is `ddm-builder` with `fix_type: judgment`
that could change procedure count or DDM structure.

---

### Step 3: Execute Mechanical Fixes (Bucket A)

Spawn subagents **in parallel** for each `route_to` group:

- If Bucket A has trr-writer issues: spawn **trr-writer** with:
  - The file to edit (README.md)
  - The specific issues routed to it (C1, C3, etc.)
  - The fix instructions from the reviewer

- If Bucket A has ddm-builder issues: spawn **ddm-builder** with:
  - The DDM JSON file(s) to edit
  - The specific issues routed to it
  - The fix instructions from the reviewer
  - The current procedure table (for reference, not for rewriting)

These are independent — trr-writer fixes prose, ddm-builder fixes JSON.
They can run simultaneously.

Wait for all Bucket A agents to return.

---

### Step 4: Execute Research Fixes (Bucket B)

If Bucket B is non-empty, spawn **trr-researcher** subagents for each
research question. Each researcher receives:
- The specific issue and what needs verification
- The current research notes from Supporting Docs
- Instructions to return a definitive answer or mark as still-unresolved

After researchers return:
- If the answer resolves the issue, apply the fix (spawn the appropriate
  agent from the `route_to` field to make the change)
- If still unresolved, move the issue to Bucket C

---

### Step 5: Present Judgment Calls (Bucket C)

If Bucket C is non-empty, present these issues to the user:

```markdown
## Issues Requiring Your Decision

These cannot be auto-fixed — they involve scoping decisions, procedure
distinctness, or structural changes that need your judgment.

### [C2] Inclusion test: "Download Payload" fails immutability
**File:** ddms/ddm_trr0030_win.json — Node n7
**Reviewer says:** Delivery method is attacker-controlled
**Options:**
  1. Remove node n7 and redefine the pipeline entry point
  2. Keep n7 but rename/redefine as the first immutable operation after delivery
  3. Research further — spawn a researcher to investigate

**What would you like to do?**
```

Wait for user input on each Bucket C item. Apply their decision.

---

### Step 6: Re-Review

After all fixes are applied (Buckets A + B resolved, Bucket C decided by user):

Spawn **reviewer** to re-validate.

**If PASS or PASS_WITH_NOTES:** Report success. The artifact is ready for commit.

**If FAIL again:** Do NOT auto-retry a second time. Present the remaining
issues to the user:

```markdown
## Second FAIL — Escalating to You

The reviewer found additional issues after the first round of fixes.
Auto-routing has reached its one-retry limit.

### Remaining Critical Issues
[list them]

### Recommendation
[Fix manually, spawn specific agents with targeted instructions, or
re-run /resolve-review after making manual adjustments]
```

The one-retry limit prevents token-burning loops where the system
chases its tail on issues that need human judgment.

---

### Step 7: Summary

```markdown
## Resolve-Review Summary: $ARGUMENTS

| Bucket | Issues | Resolved | Escalated |
|--------|--------|----------|-----------|
| Mechanical (auto) | N | N | — |
| Research (auto) | N | N | N moved to user |
| Judgment (user) | N | N | — |

**Final verdict:** PASS / FAIL (escalated)

**Agents spawned:** [list with what each fixed]
**Files modified:** [list]
```
```

---

## Change 3: Integration into `/trr` and `/ddm`

### Modify `/trr.md` — Phases 3 and 4

Replace the current:

```markdown
**If reviewer returns FAIL**: Fix all critical issues. Re-run reviewer.
Do not proceed until PASS or PASS_WITH_NOTES.
```

With:

```markdown
**If reviewer returns FAIL**:
- If the verdict contains `routed_issues`: run `/resolve-review TRR####`
  to auto-route mechanical fixes and surface judgment calls.
- If `/resolve-review` achieves PASS or PASS_WITH_NOTES: proceed.
- If `/resolve-review` escalates (second FAIL): STOP. Present remaining
  issues to the user. Do not proceed until they are resolved and the
  reviewer passes.
- If the verdict does NOT contain `routed_issues` (legacy format):
  fix issues manually and re-run `/review`.
```

### Modify `/ddm.md` — Step 4

Same pattern: replace the manual "resolve reviewer findings" instruction with the conditional `/resolve-review` routing.

### Modify `/review.md` — Step 5

Add after "State clearly that this TRR cannot be committed":

```markdown
**Auto-fix option:** If the reviewer verdict contains `routed_issues`,
suggest: "Run `/resolve-review $ARGUMENTS` to auto-route fixes, or fix
manually and re-run `/review`."
```

---

## Implementation Order

### Phase 1: Enhanced Reviewer (smallest change, highest value)

**Edit:** `.claude/agents/reviewer.md`
**What:** Add the Routing Rules section and the `routed_issues` array to the output format.
**Effort:** ~40 lines added to the agent definition.
**Test:** Run `/review` against a completed TRR that you know has issues (or introduce a test issue). Verify the `routed_issues` array appears in the JSON block with correct `route_to` and `fix_type` values.

This change is backward-compatible — the existing markdown report is unchanged, and the existing `verdict`/`critical_count`/`blocking` fields remain. Commands that don't know about `routed_issues` just ignore it.

### Phase 2: `/resolve-review` Command

**Create:** `.claude/commands/resolve-review.md`
**What:** The new command as designed above.
**Effort:** ~120 lines for the command definition.
**Test:** Introduce a known FAIL condition (write detection language into a TRR, add a bare telemetry label to a DDM). Run `/review`, then `/resolve-review`. Verify:
- Mechanical fixes are routed to the right agent
- Judgment calls are presented to you
- Re-review runs after fixes
- Second FAIL escalates instead of looping

### Phase 3: Integration

**Edit:** `.claude/commands/trr.md`, `.claude/commands/ddm.md`, `.claude/commands/review.md`
**What:** Replace manual fix instructions with conditional `/resolve-review` routing.
**Effort:** ~15 lines changed across three files.
**Test:** Run a full `/trr` pipeline where the writer produces a known failure mode. Verify the pipeline auto-routes the fix rather than stopping for manual intervention.

### Phase 4: Observation and Tuning

After running 2-3 TRRs through the pipeline with routing enabled:
- Check `/insights` for patterns in what gets auto-fixed vs. escalated
- If a category is consistently misrouted (e.g., `bare_telemetry_label` in DDM JSON is being routed to `trr-writer`), adjust the routing rules
- If the one-retry limit is too conservative (fixes are always clean on re-review), consider allowing two retries for mechanical-only FAILs
- If judgment calls are consistently resolvable by research, consider auto-routing more to `trr-researcher` before escalating

---

## Guard Rails

### One-Retry Limit
`/resolve-review` runs the reviewer exactly twice: once to find issues, once to verify fixes. If the second review fails, it stops and escalates. This prevents:
- Token-burning loops on issues that need human judgment
- Cascading fixes where fixing one thing breaks another (a sign the original issue was misdiagnosed)
- The system rationalizing that "close enough" is good enough

### Judgment Escalation
Issues marked `fix_type: judgment` always go to the user, even on first pass. The system never autonomously decides:
- Whether an operation passes the inclusion test
- Whether two paths are distinct procedures
- Whether a scoping decision should change
- Whether a DDM structural change is warranted

### Stop Hook Compatibility
The existing anti-rationalization Stop hook still fires. If `/resolve-review` tries to declare issues resolved without actually fixing them, the Stop hook catches it. The two systems reinforce each other — routing makes fixes faster, the Stop hook prevents shortcutting.

### Cascading Changes
When a DDM fix cascades to prose (e.g., removing a node means removing its reference in the procedure narrative), the routing system handles this by:
1. ddm-builder fixes the JSON
2. After ddm-builder returns, the orchestrator checks if the fix affects prose
3. If yes, spawns trr-writer with the specific cascade instruction
4. The re-review catches anything that was missed

This is why `route_to: orchestrator` exists — some fixes need coordination across agents, and the orchestrator is the only entity that can sequence them.

---

## What This Doesn't Change

- **The reviewer is still read-only.** It produces verdicts, not fixes.
- **The verdict format is backward-compatible.** `routed_issues` is additive.
- **Human oversight is preserved.** Judgment calls always escalate. Second FAILs always escalate.
- **The Stop hook still fires.** Routing doesn't bypass anti-rationalization.
- **The existing `/resolve` command is unchanged.** It handles `[?]` markers. `/resolve-review` handles reviewer FAILs. Different problems, different tools.
