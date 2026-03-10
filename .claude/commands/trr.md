---
description: Full TRR pipeline — scoping through final README.md. Runs all phases with stop gates, inline commits, and reviewer enforcement.
argument-hint: "<ATT&CK technique ID or technique name> [platform]"
---

# TRR: $ARGUMENTS

Execute the full TRR research pipeline for:

> **$ARGUMENTS**

Work is saved to `WIP TRRs\TRR####\[platform]\`. Replace `####` with the assigned TRR number and `[platform]` with `win`, `lnx`, etc.

**Session discipline:** Each phase is a natural session boundary. If context gets heavy after a phase, run `/wrap` and recommend a fresh session rather than pushing through. A clean session with committed artifacts beats a compacted session that lost nuance.

---

### Step 0: Setup and Context Assembly

**Create the directory structure** for this TRR if it doesn't already exist:

```bash
mkdir -p "WIP TRRs/TRR####/win/ddms"
mkdir -p "WIP TRRs/TRR####/win/Supporting Docs"
mkdir -p "WIP TRRs/TRR####/win/Procedure Lab"
mkdir -p "WIP TRRs/TRR####/win/images"
```

Then gather known context to front-load into researcher spawns:

1. **ATT&CK URL**: Build the full URL for the technique (e.g., `https://attack.mitre.org/techniques/T1505/003/`)
2. **Adjacent TRRs**: Check `Completed TRR Reports\` and `WIP TRRs\` for TRRs covering related sub-techniques or techniques. Note their IDs and scope boundaries so researchers don't duplicate or contradict existing work.
3. **Platform constraints**: Extract from `$ARGUMENTS` or confirm with the user.
4. **Known procedure leads**: If the user mentioned specific execution paths, tools (for attribution only), or variants, capture them.
5. **Source Scraper output**: If the user ran the TRR Source Scraper before this session and provided a file path, read it now.

Include this assembled context in every researcher spawn below. This prevents researchers from spending tokens rediscovering what is already known.

---

### Phase 1: Scoping and Technical Background

Spawn **3 trr-researcher subagents in parallel** (include Step 0 context in each):

1. **ATT&CK + Atomic Red Team researcher**: Pull the technique entry, tactic, platforms, procedure examples, sub-techniques. What is the attacker trying to accomplish?

2. **Technology researcher**: Research the underlying OS internals, APIs, protocols, services, and security controls. Focus on *how the technology works*, not exploitation. This feeds directly into the Technical Background section.

3. **Real-world researcher**: Find threat reports, security blog posts, and PoC repositories. What distinct execution paths exist in practice? What tools are used (for reference/attribution only)?

Synthesize into the scoping document format (matching `/scope` output structure):

```markdown
# Phase 1 Scoping: [Technique Name]

## Scope Statement
[One precise sentence]

## Exclusion Table
| Excluded Item | Rationale |
|---|---|

## Essential Constraints Table
| # | Constraint | Essential? | Immutable? | Observable? | Telemetry |
|---|-----------|------------|------------|-------------|-----------|

## Technical Background Notes
[Detailed notes on underlying technology]

## Open Questions
[Unresolved items with [?] markers]

## Sources
```

Save to: `WIP TRRs\TRR####\win\Supporting Docs\phase1_research.md`

**Commit this phase:**
```
git add "WIP TRRs/TRR####/"
git commit -m "TRR####: Phase 1 -- Initial overview and technical background"
```

**STOP. Present the scoping document. Wait for explicit user confirmation before proceeding. Do not pre-start Phase 2.**

---

### Phase 2: DDM Construction

Spawn **ddm-builder** with the Phase 1 research notes. Build the master DDM:
- Map all essential operations with explicit inclusion test verdicts per operation
- Model prerequisites correctly (not inline)
- Label all branch conditions
- Annotate telemetry with descriptive labels on correct operations

Save to: `WIP TRRs\TRR####\win\ddms\ddm_trr####_win.json`

**Commit this phase:**
```
git add "WIP TRRs/TRR####/win/ddms/"
git commit -m "TRR####: Phase 2 -- DDM draft with telemetry map"
```

**STOP. Present the DDM. Ask: are there alternate paths not yet explored? Wait for confirmation.**

---

### Phase 3: Alternate Paths + Procedure Identification

Spawn **2 subagents in parallel**:

1. **trr-researcher**: Investigate alternate execution paths — alternate APIs, mechanisms, or variants. For each: do they change essential operations (new procedure) or only implementation details (same procedure, tangential)?

2. **ddm-builder** (after researcher returns): Once alternate paths are confirmed, trace all distinct procedures, assign IDs (`TRR####.WIN.A`, `.B`, etc.), create procedure table, produce per-procedure JSON exports with red arrows (`#f44e3b`) on active path.

Save procedures to: `WIP TRRs\TRR####\win\Supporting Docs\procedures.md`
Save exports to: `WIP TRRs\TRR####\win\ddms\trr####_win_[a/b/c].json`

Then spawn **reviewer** to validate the master DDM and procedure exports against all checklists.

**If reviewer returns FAIL**: Run `/resolve-review TRR####` to auto-route mechanical fixes and surface judgment calls. If `/resolve-review` achieves PASS or PASS_WITH_NOTES, proceed. If it escalates (second FAIL), STOP and resolve remaining issues before continuing. If the verdict does not contain `routed_issues` (legacy format), fix issues manually and re-run `/review`.

**Commit this phase** (after reviewer passes):
```
git add "WIP TRRs/TRR####/"
git commit -m "TRR####: Phase 3 -- Procedures identified (WIN.A, WIN.B), DDM validated"
```

**STOP. Present procedures and reviewer verdict. Confirm before proceeding.**

---

### Phase 4: TRR Document

Spawn **trr-writer** with:
- Phase 1 research notes
- Validated procedure table
- DDM filenames

Writer produces: `WIP TRRs\TRR####\win\README.md`

Then spawn **reviewer** to run the full TRR document checklist.

**If reviewer returns FAIL**: Run `/resolve-review TRR####` to auto-route mechanical fixes and surface judgment calls. If `/resolve-review` achieves PASS or PASS_WITH_NOTES, proceed to commit. If it escalates (second FAIL), STOP and resolve remaining issues before committing. If the verdict does not contain `routed_issues` (legacy format), fix issues manually and re-run `/review`.

**Commit this phase** (after reviewer passes):
```
git add "WIP TRRs/TRR####/"
git commit -m "TRR####: Phase 4 -- TRR document complete"
```

Present final summary: TRR ID, procedure IDs, files created, reviewer verdicts, any open warnings.

Recommend running `/wrap` to close out the session.
