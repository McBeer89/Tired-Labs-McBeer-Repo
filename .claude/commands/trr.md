---
description: Full TRR pipeline — scoping through final README.md. Runs all phases with stop gates and reviewer enforcement.
argument-hint: "<ATT&CK technique ID or technique name> [platform]"
---

# TRR: $ARGUMENTS

Execute the full TRR research pipeline for:

> **$ARGUMENTS**

Work is saved to `WIP TRRs\TRR####\[platform]\`. Replace `####` with the assigned TRR number and `[platform]` with `win`, `lnx`, etc.

**Session discipline:** Each phase is a natural session boundary. If context gets heavy after a phase, recommend a fresh session rather than pushing through. A clean session with committed artifacts beats a compacted session that lost nuance.

---

### Phase 1: Scoping and Technical Background

Spawn **3 trr-researcher subagents in parallel**:

1. **ATT&CK + Atomic Red Team researcher**: Pull the technique entry, tactic, platforms, procedure examples, sub-techniques. What is the attacker trying to accomplish?

2. **Technology researcher**: Research the underlying OS internals, APIs, protocols, services, and security controls. Focus on *how the technology works*, not exploitation. This feeds directly into the Technical Background section.

3. **Real-world researcher**: Find threat reports, security blog posts, and PoC repositories. What distinct execution paths exist in practice? What tools are used (for reference/attribution only)?

Synthesize into a scoping document:
- Scope Statement (one precise sentence)
- Exclusion Table (what's out and why, referencing the inclusion test)
- Essential Constraints Table

Save to: `WIP TRRs\TRR####\win\Supporting Docs\phase1_research.md`

**STOP. Present the scoping document. Wait for explicit user confirmation before proceeding. Do not pre-start Phase 2.**

---

### Phase 2: DDM Construction

Spawn **ddm-builder** with the Phase 1 research notes. Build the master DDM:
- Map all essential operations with explicit inclusion test verdicts per operation
- Model prerequisites correctly (not inline)
- Label all branch conditions
- Annotate telemetry with descriptive labels on correct operations

Save to: `WIP TRRs\TRR####\win\ddms\ddm_trr####_win.json`

**STOP. Present the DDM. Ask: are there alternate paths not yet explored? Wait for confirmation.**

---

### Phase 3: Alternate Paths + Procedure Identification

Spawn **2 subagents in parallel**:

1. **trr-researcher**: Investigate alternate execution paths — alternate APIs, mechanisms, or variants. For each: do they change essential operations (new procedure) or only implementation details (same procedure, tangential)?

2. **ddm-builder**: Once alternate paths are confirmed, trace all distinct procedures, assign IDs (`TRR####.WIN.A`, `.B`, etc.), create procedure table, produce per-procedure JSON exports with red arrows (`#f44e3b`) on active path.

Save procedures to: `WIP TRRs\TRR####\win\Supporting Docs\procedures.md`
Save exports to: `WIP TRRs\TRR####\win\ddms\trr####_win_[a/b/c].json`

Then spawn **reviewer** to validate the master DDM and procedure exports against all checklists.

**If reviewer returns FAIL**: Fix all critical issues. Re-run reviewer. Do not proceed until PASS or PASS_WITH_NOTES.

**STOP. Present procedures and reviewer verdict. Confirm before proceeding.**

---

### Phase 4: TRR Document

Spawn **trr-writer** with:
- Phase 1 research notes
- Validated procedure table
- DDM filenames

Writer produces: `WIP TRRs\TRR####\win\README.md`

Then spawn **reviewer** to run the full TRR document checklist.

**If reviewer returns FAIL**: Fix all critical issues. Re-run reviewer. Do not commit a FAIL'd document.

---

### Phase 5: Commit

Only after reviewer PASS or PASS_WITH_NOTES on both DDM and TRR document:

```
TRR####: Phase 1 — Initial overview and technical background
TRR####: Phase 2 — DDM draft with telemetry map
TRR####: Phase 3 — Procedures identified (WIN.A, WIN.B), DDM validated
TRR####: Phase 4 — TRR document complete
```

Present final summary: TRR ID, procedure IDs, files created, reviewer verdicts, any open warnings.
