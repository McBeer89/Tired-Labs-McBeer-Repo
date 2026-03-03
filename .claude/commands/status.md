---
description: Show current TRR work state, git status, and session health
---

# Status

Report the current state of the repository and any active TRR work.

---

### Step 1: Git Status

Run `git status` and `git log --oneline -5` to show:
- Current branch
- Uncommitted changes
- Last 5 commits

### Step 2: Active TRR Work

Check `WIP TRRs\` for any TRR folders. For each:
- TRR ID and technique name (from README.md or research notes)
- Which phases are complete (check for committed artifacts: phase1_research.md, ddm JSON, procedure exports, README.md)
- Any `[?]` markers in current files (grep for them)
- Last reviewer verdict (if a review report exists)

### Step 3: Present Summary

```
## Repository Status

Branch: [branch]
Clean: [yes/no — uncommitted changes listed if no]
Last commits:
  [hash] [message]
  [hash] [message]

## Active TRR Work

### TRR#### — [Technique Name]
Phase 1 (Scoping):     ✅ committed / ⏳ in progress / ❌ not started
Phase 2 (DDM):         ✅ / ⏳ / ❌
Phase 3 (Procedures):  ✅ / ⏳ / ❌
Phase 4 (TRR Doc):     ✅ / ⏳ / ❌
Last Review:           PASS / FAIL / none
Open [?] markers:      [count]
```
