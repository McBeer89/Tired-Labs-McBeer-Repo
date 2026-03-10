---
description: Generate KQL query sets from a completed TRR and its DDM. Derivative detection-team output — run only after the TRR is complete.
argument-hint: "<TRR ID> [platform - default: win]"
---

# KQL: $ARGUMENTS

Generate KQL detection queries for:

> **$ARGUMENTS**

This is a **derivative document** — detection-team work product built from completed TRR source material.

---

### Step 1: Validate Prerequisites

Before spawning any subagents, confirm these files exist:

- `Completed TRR Reports\TRR####\win\README.md` (the completed TRR)
- `Completed TRR Reports\TRR####\win\ddms\ddm_trr####_win.json` (master DDM)
- Per-procedure DDM exports in `ddms\`

If the TRR still lives in `WIP TRRs\` (not yet moved), use that path — but confirm with the user that the TRR is actually finished.

If any required files are missing, **STOP**. Report what's needed. Do not generate queries from incomplete research.

---

### Step 2: Read Environment Profile

Check for `kql-environment-profile.md` at the repo root. If it exists and has
content, it governs log source availability, field names, and known baselines
for all generated queries. Pass it to the kql-builder in Step 4. If empty or
missing, queries will use generic schema — note this in COVERAGE.md.

---

### Step 3: Research and Parse

Spawn **2 subagents in parallel**:

1. **trr-researcher**: Read the TRR README.md. Extract:
   - All procedure IDs and names
   - Telemetry constraints documented in Technical Background (e.g., "Sysmon 7 does not fire for CLR-managed assembly loads", indistinguishable events)
   - Any boundary cases or scope limitations that affect query logic

2. **kql-builder**: Read the master DDM JSON and all per-procedure JSON exports. For each procedure, trace the red arrow path and catalog:
   - Every operation on the active path
   - Telemetry labels on each operation
   - Immutable properties on each operation (these become query filters)
   - Branch conditions (these become query variants)
   - Operations with no telemetry labels (blind spots)

Wait for both to return.

---

### Step 4: Generate Query Files

Spawn **kql-builder** with the combined research and environment profile. For each procedure:

1. Map each operation's telemetry labels to log tables (Sentinel + Defender)
2. Build queries that filter on immutable attributes from DDM node properties
3. Each query gets a minimal 2-3 line header (procedure ID, DDM operation, telemetry source) — **no inline commentary**
4. Produce separate queries for each branch path
5. The .kql files must be copy-paste ready — all filter rationale, tangential warnings, and telemetry constraints go in COVERAGE.md, not inline

Save to: `Completed TRR Reports\TRR####\win\kql\trr####_win_[a/b/c].kql`

---

### Step 4b: Validate Query Syntax

Run the KQL Level 1 validator against all generated `.kql` files:

```bash
python tools/kql-validator/validate.py "Completed TRR Reports/TRR####/win/kql/*.kql"
```

If **errors** are found: route the error report back to kql-builder with specific fix instructions, re-generate only the queries with errors, and re-validate.

If **warnings only**: proceed — include them in COVERAGE.md under Telemetry Constraints if relevant.

If **PASS**: proceed to Step 5.

---

### Step 5: Coverage Document

Spawn **kql-builder** to produce `COVERAGE.md`:

- Procedure coverage table (operations covered vs. blind spots)
- Table dependency list
- Blind spots table (operations without queryable telemetry)
- Telemetry constraints carried from the TRR
- Vendor-specific telemetry not queryable in Sentinel/Defender
- Query file inventory
- **Query annotations** — per-query tables with Filter / DDM Trace / Rationale columns, plus tangential elements deliberately not filtered

Save to: `Completed TRR Reports\TRR####\win\kql\COVERAGE.md`

---

### Step 6: Review

Spawn **reviewer** to validate:

- [ ] Every query filter traces to a DDM operation
- [ ] No tangential elements are hardcoded in filters
- [ ] `.kql` files contain queries only with minimal 2-3 line headers (no inline commentary)
- [ ] COVERAGE.md contains query annotations with Filter / DDM Trace / Rationale tables for every query
- [ ] Telemetry constraints from the TRR are documented in COVERAGE.md
- [ ] Coverage summary accurately reflects DDM operations vs. query coverage
- [ ] Blind spots are documented, not silently omitted
- [ ] Both Sentinel and Defender variants produced where applicable

Resolve reviewer findings.

---

### Step 7: Present Results

Present:
- List of `.kql` files created
- Coverage summary (how many operations per procedure have queries)
- Blind spots (operations with no telemetry)
- Any telemetry constraints that limit query effectiveness

Commit convention:
```
TRR####: Derivative -- KQL query set for [platform]
```
