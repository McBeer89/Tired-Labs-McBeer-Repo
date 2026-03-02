---
description: Review recent changes or specified files for quality, bugs, and improvements
---

# Review: $ARGUMENTS

## Instructions

Review the following for quality:

> **$ARGUMENTS**

If no specific files or changes were mentioned, review the most recent git changes:
```bash
git diff HEAD~1
```

### Step 1: Spawn Parallel Reviewers

Launch **2 reviewer subagents in parallel** with different focuses:

1. **Correctness reviewer**: Check for bugs, logic errors, edge cases, and security issues. Run tests if available.
2. **Quality reviewer**: Check for code style, readability, documentation, error handling, and maintainability.

### Step 2: Consolidate

Merge both reviewers' findings into a single report:

```markdown
# Code Review

## Verdict: PASS / FAIL

## Critical Issues (must fix)
- ...

## Warnings (should fix)
- ...

## Suggestions (nice to have)
- ...

## Tests
- Tests run: [results]
- Coverage gaps: [if any]
```

### Step 3: Present

If PASS: Present the report and confirm the code is ready.
If FAIL: Present the issues and ask if you should fix them.
