---
description: End-of-session handoff. Writes a structured session note so the next session can pick up cleanly. Run at every phase gate or when context gets heavy.
argument-hint: "[optional: summary of what was accomplished]"
---

# Wrap: $ARGUMENTS

Create a session handoff document for the next session to pick up from.

---

### Step 1: Gather Current State

Collect the following:
- Run `git status` — what's committed, what's staged, what's modified
- Run `git log --oneline -5` — recent commits
- Check for any `[?]` markers in TRR files:
  ```bash
  grep -rn "\[?\]" "WIP TRRs" --include="*.md" --include="*.json" 2>/dev/null
  ```
- Check for any TODO/FIXME markers similarly
- Note which files were created or modified in this session (from git diff or recent changes)

### Step 2: Identify Active TRR State

Scan `WIP TRRs\` to determine current TRR work:
- **TRR ID**: Which TRR folder(s) exist in `WIP TRRs\`?
- **Platform**: Which platform folder is active (win, lnx, etc.)?
- **Phase status**: Check for committed artifacts:
  - Phase 1: `Supporting Docs\phase1_research.md` exists?
  - Phase 2: `ddms\ddm_trr####_win.json` exists?
  - Phase 3: `ddms\trr####_win_a.json` (or b, c) exists?
  - Phase 4: `README.md` exists and has content beyond placeholder?
- **Last reviewer verdict**: Check for review output in recent git log messages or supporting docs.
- **Open `[?]` count**: From Step 1 grep, filter to this TRR's folder.

### Step 3: Write the Handoff Note

Create the `docs/session-notes/` directory if it doesn't exist, then write `docs/session-notes/YYYY-MM-DD.md` (use today's date, append `-N` if one already exists for today).

**IMPORTANT**: The global `block-destructive.sh` hook blocks commits containing `[?]` markers in staged files. Session notes must use `OPEN:` to document unresolved questions instead of `[?]` — the `[?]` markers live in the TRR files themselves, not in session notes.

```markdown
# Session Notes — [Date]

## What Was Accomplished
[Summary of work done — phases completed, DDM operations mapped, research findings, reviewer verdicts.
Use $ARGUMENTS if the user provided a summary, otherwise synthesize from git log and session context.]

## Active TRR State
- **TRR ID**: TRR#### — [Technique Name]
- **Platform**: win / lnx
- **Phase Status**:
  - Phase 1 (Scoping):     ✅ committed / ⏳ in progress / ❌ not started
  - Phase 2 (DDM):         ✅ / ⏳ / ❌
  - Phase 3 (Procedures):  ✅ / ⏳ / ❌
  - Phase 4 (TRR Doc):     ✅ / ⏳ / ❌
- **Last Phase Gate Cleared**: Phase [N] — confirmed by user on [date/this session]
- **Next Phase Gate**: Phase [N+1] — [what needs to happen before it clears]
- **Last Reviewer Verdict**: PASS / FAIL / PASS_WITH_NOTES / not yet reviewed
- **Open Questions**: [count] remaining in TRR files

## Current State
- **Branch**: [current branch]
- **Last Commit**: [hash — message]
- **Uncommitted Changes**: [list or "none"]

## Files Changed This Session
- [file] — [what changed and why]

## Subagent Returns This Session
[Brief summary of what each subagent contributed, so the next session doesn't re-spawn for already-answered questions.]
- **trr-researcher**: [what was researched, key findings]
- **ddm-builder**: [what was built, validation status]
- **trr-writer**: [what was drafted, self-review status]
- **reviewer**: [verdict, critical issues found]
[Omit agents that were not used this session.]

## What's Next
[Concrete next steps. Be specific enough that the next session can start working immediately.]

1. [Next task — enough detail to act on]
2. [Next task]
3. [Next task]

## Unresolved Questions
[Questions that remain open for the next session. These correspond to markers in TRR files.]

- OPEN: [question — which file, what context, what would resolve it]
- OPEN: [question]

## Decisions Made
[Any scoping decisions, DDM inclusion/exclusion verdicts, or procedure differentiation choices. The next session must know these to avoid re-debating them.]

- [Decision: X because Y]

## Blockers
[Anything that can't proceed without user input, lab testing, or external information.]

- [Blocker — what's needed to unblock]
```

### Step 4: Commit the Note

```bash
git add docs/session-notes/
git commit -m "docs: session notes for [date]"
```

If the commit is blocked by the `[?]` hook, you have `[?]` markers in the session note itself — replace them with `OPEN:` prefix as documented above. Session notes document open questions; they do not contain them.

### Step 5: Recommend Next Session Start

Tell the user:

> Session wrapped. Next time, start with:
> ```
> Read docs/session-notes/[date].md and continue from "What's Next"
> ```
> Or just say "pick up where we left off" and I'll find the latest session note.

If a phase boundary was reached, also recommend:

> Phase [N] is committed. I'd recommend starting a fresh session for Phase [N+1] — [reason: research will need clean context / DDM construction is context-heavy / etc.].

---

### Special Case: Starting a New Session

When a user says "pick up where we left off" or similar:

1. Find the most recent file in `docs/session-notes/`
2. Read it
3. Also read the current TRR's `README.md` and latest DDM JSON (if they exist) to restore full context
4. Present the "Active TRR State" and "What's Next" sections
5. Ask: "Want me to start on the first item, or do you want to adjust the plan?"

### Special Case: Wrapping Mid-Phase

If wrapping before a phase is complete (context getting heavy, not at a gate):

1. In "Phase Status," mark the current phase as ⏳ and note exactly where within the phase work stopped
2. In "What's Next," be very specific about resumption point: "Continue Phase 2 — DDM has 5 of ~8 operations mapped. Next: investigate alternate paths for the code execution branch."
3. In "Subagent Returns," capture any partial research so it's not lost to compaction
