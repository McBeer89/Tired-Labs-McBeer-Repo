---
description: Phases 2-3 — DDM construction and procedure identification. Requires completed Phase 1 scoping document.
argument-hint: "<TRR ID> [platform]"
---

# DDM: $ARGUMENTS

Build the Detection Data Model and identify procedures for:

> **$ARGUMENTS**

Requires a completed Phase 1 scoping document in `WIP TRRs\TRR####\win\Supporting Docs\phase1_research.md`. If it doesn't exist, tell the user to run `/scope` first.

---

### Step 1: Verify Prerequisites

Read the Phase 1 scoping document. Confirm:
- [ ] Scope statement exists and is specific
- [ ] Exclusion table exists with rationale
- [ ] Essential constraints table exists
- [ ] No unresolved `[?]` markers that would block DDM work

If prerequisites are not met, stop and tell the user what's missing.

---

### Step 2: Phase 2 — DDM Construction

Spawn **ddm-builder** with the Phase 1 research notes.

The builder must:
- Map all essential operations with explicit inclusion test verdicts
- Model prerequisites as prerequisite nodes (not inline pipeline steps)
- Label all branch conditions on branching arrows
- Place telemetry labels (descriptive format) on correct operations
- Run its internal validation checklist before returning

Save to: `WIP TRRs\TRR####\win\ddms\ddm_trr####_win.json`

**STOP. Present the DDM. Ask: are there alternate paths not yet explored? Wait for confirmation.**

---

### Step 3: Phase 3 — Alternate Paths + Procedures

Spawn **2 subagents in parallel**:

1. **trr-researcher**: Investigate alternate execution paths. For each candidate path, answer: "Does this change the essential operations?" If yes → new procedure. If no → same procedure, tangential variation.

2. **ddm-builder** (after researcher returns): Trace all distinct procedures, assign IDs, create procedure table, produce per-procedure JSON exports with red arrows on active paths.

Save procedures to: `WIP TRRs\TRR####\win\Supporting Docs\procedures.md`
Save exports to: `WIP TRRs\TRR####\win\ddms\trr####_win_[a/b/c].json`

---

### Step 4: Review Gate

Spawn **reviewer** against all DDM files (master + per-procedure exports).

**If FAIL**: Fix all critical issues. Re-run reviewer. Do not proceed.
**If PASS_WITH_NOTES**: Recommend fixing warnings. May proceed.
**If PASS**: Confirm DDM is ready.

**STOP. Present procedure table and reviewer verdict. Confirm before any TRR writing begins.**
