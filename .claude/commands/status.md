---
description: Show current TRR work state, git status, session health, and DDM inventory.
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

1. **TRR ID and technique** — read from README.md or Supporting Docs\phase1_research.md
2. **Phase status** — check for committed artifacts:
   - Phase 1: `Supporting Docs\phase1_research.md` exists?
   - Phase 2: `ddms\ddm_trr####_win.json` exists?
   - Phase 3: `ddms\trr####_win_a.json` (or b, c) exists?
   - Phase 4: `README.md` exists and has content beyond a placeholder?
3. **DDM inventory**:
   - Master DDM file? (size, last modified)
   - How many per-procedure exports? (list filenames)
   - PNG exports present? (for Arrows.app renders)
4. **Open `[?]` markers** — grep across the TRR folder:
   ```bash
   grep -rn "\[?\]" "WIP TRRs/TRR####" --include="*.md" --include="*.json" 2>/dev/null
   ```
5. **Last reviewer verdict** — check recent git log for reviewer-related commits or look for review notes in Supporting Docs.

### Step 3: Session Health

Check session continuity:
- **Latest session note**: What date? Is it recent or stale?
  ```bash
  ls -t docs/session-notes/*.md 2>/dev/null | head -1
  ```
- **Auto-wrap notes count** — how many contain "(auto-wrap)" in the filename or header?
  ```bash
  grep -l "auto-wrap\|auto-generated" docs/session-notes/*.md 2>/dev/null | wc -l
  ```
- **Unfilled TODOs in session notes** — any session notes with unresolved `[TODO]` markers?
  ```bash
  grep -l "\[TODO\]" docs/session-notes/*.md 2>/dev/null
  ```

### Step 4: Present Summary

```
## Repository Status

Branch: [branch]
Clean: [yes/no — uncommitted changes listed if no]
Last commits:
  [hash] [message]
  [hash] [message]
  ...

## Active TRR Work

### TRR#### — [Technique Name]
Phase 1 (Scoping):     ✅ committed / ⏳ in progress / ❌ not started
Phase 2 (DDM):         ✅ / ⏳ / ❌
Phase 3 (Procedures):  ✅ / ⏳ / ❌
Phase 4 (TRR Doc):     ✅ / ⏳ / ❌
Last Review:           PASS / FAIL / PASS_WITH_NOTES / none
Open Questions:        [count] — [brief list of what they're about]

DDM Inventory:
  Master:     ddm_trr####_win.json ([size])
  Exports:    trr####_win_a.json, trr####_win_b.json
  PNGs:       [present / missing]

## Session Health

Latest session note:   [date] — [filename]
Auto-wrap notes:       [count] (should be low — manual /wrap is preferred)
Unfilled TODOs:        [list of session note files with [TODO] markers]

## Recommended Action

[Based on the status, suggest what to do next:]
- If a phase gate is ready: "Phase 2 artifacts are committed. Ready for Phase 3."
- If [?] markers exist: "[N] open questions need resolution before proceeding."
- If session notes are stale: "Last session note is [N] days old. Run /wrap to update."
- If auto-wraps outnumber manual wraps: "Too many auto-wraps. Use /wrap proactively."
```
