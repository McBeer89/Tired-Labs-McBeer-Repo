---
description: Generate a TRR conventional commit message from staged changes, present for approval, and commit.
argument-hint: "[optional: context about what was done and why]"
---

# Commit: $ARGUMENTS

Generate a commit message following TRR conventions and commit after approval.

---

### Step 1: Check Staged Changes

Run `git diff --cached --stat` to see what's staged.

If nothing is staged:
- Run `git status --short` to show what's available
- Ask: "Nothing staged. Want me to stage specific files, or `git add -A` to stage everything?"
- Wait for confirmation before staging.

---

### Step 2: Analyze the Diff

Run `git diff --cached` to read the actual changes (not just file names).

Identify:
- **What changed** — TRR phases, DDM operations, research notes, tooling, docs
- **Which TRR** — look at file paths to determine TRR ID (e.g., `WIP TRRs\TRR0002\`)
- **Which phase** — what kind of artifact was changed (scoping doc, DDM JSON, procedure exports, README.md)
- **Scope** — single file vs. multi-file, single TRR vs. cross-cutting

---

### Step 3: Generate Commit Message

Follow TRR commit conventions:

**Phase commits** (most common — one per phase gate):

| Pattern | When |
|---------|------|
| `TRR####: Phase 1 -- Initial overview and technical background` | Scoping doc committed |
| `TRR####: Phase 2 -- DDM draft with telemetry map` | Master DDM JSON committed |
| `TRR####: Phase 3 -- Procedures identified (WIN.A, WIN.B), DDM validated` | Per-procedure exports committed |
| `TRR####: Phase 4 -- TRR document complete` | README.md committed |
| `TRR####: Derivative -- Detection methods document` | Post-TRR derivative work |
| `TRR####: Fix -- [description]` | Post-review corrections |

**Non-TRR commits:**

| Pattern | When |
|---------|------|
| `tools: [description]` | Source Scraper or other tooling changes |
| `docs: session notes for [date]` | Session handoff notes |
| `docs: insights for [date]` | Workflow insights analysis |
| `docs: [description]` | Methodology, guides, or other documentation |

**Rules:**
- Phase commits include the procedure IDs if Phase 3+ (e.g., `(WIN.A, WIN.B, WIN.C)`)
- Fix commits describe what was fixed, not just "fixes" (e.g., `Fix -- bare telemetry labels in DDM, detection language in Procedure B narrative`)
- If `$ARGUMENTS` provides context, use it to inform the message
- If the diff spans multiple TRRs (rare), use separate commits per TRR

---

### Step 4: Pre-Commit Checks

Before presenting the commit message, verify:

1. **No `[?]` markers in staged files** — run `git diff --cached --unified=0 | grep '\[?\]'`. If found, warn: "Staged files contain unresolved questions. The block-destructive hook will reject this commit. Resolve them first or unstage those files."

2. **No detection language in staged TRR files** — spot-check README.md diffs for banned phrases from the trr-prose-guard hook. If found, warn before the hook catches it.

3. **Consistent phase** — if the commit message says "Phase 2" but the diff includes README.md changes that look like Phase 4, flag the mismatch.

---

### Step 5: Present for Approval

Show the proposed commit message and the file list. Ask:

> **Proposed commit:**
> ```
> [the message]
> ```
> **Files:** [N files — list them]
>
> Commit this, or want me to adjust the message?

**Wait for confirmation.** Do not commit without approval.

---

### Step 6: Commit

After approval:
```bash
git add [files if not already staged]
git commit -m "[message]"
```

If multi-line details are needed:
```bash
git commit -m "TRR####: Phase 3 -- Procedures identified (WIN.A, WIN.B), DDM validated" -m "- Master DDM: 8 operations, all passing inclusion test" -m "- 2 procedures: OS command execution (A), in-process .NET (B)"
```

Report the commit hash and short log entry when done.
