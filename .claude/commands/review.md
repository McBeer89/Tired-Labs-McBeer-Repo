---
description: Run the reviewer against TRR documents and/or DDM JSON. Returns structured verdicts. FAIL blocks progression.
argument-hint: "[TRR ID or file path(s)]"
---

# Review: $ARGUMENTS

Run a full methodology review on the specified target.

---

### Step 1: Identify Review Targets

If `$ARGUMENTS` is a TRR ID (e.g., `TRR0023`):
- Find the TRR folder: `WIP TRRs\TRR####\`
- Queue for review: `README.md` (TRR document) + all `.json` files in `ddms\`

If `$ARGUMENTS` is a file path:
- Queue that specific file for review.

If `$ARGUMENTS` is empty:
- Look for the most recently modified TRR folder in `WIP TRRs\` and review it.

---

### Step 2: Spawn Reviewer(s)

Spawn **reviewer** subagent(s):

- If reviewing both TRR document and DDM JSON, spawn **two reviewers in parallel**:
  1. One for the README.md (TRR document checklist)
  2. One for the DDM JSON files (DDM checklist)

- If reviewing a single file, spawn one reviewer.

Each reviewer returns a structured report with a JSON verdict block.

---

### Step 3: Parse Verdicts

Extract the JSON verdict from each reviewer return:

```json
{
  "verdict": "PASS" | "FAIL" | "PASS_WITH_NOTES",
  "critical_count": 0,
  "warning_count": 0,
  "blocking": true | false
}
```

---

### Step 4: Report Results

Present a combined summary:

```
## Review Results: [TRR ID]

| Target | Verdict | Critical | Warnings | Blocking |
|--------|---------|----------|----------|----------|
| README.md | PASS/FAIL | N | N | yes/no |
| DDM JSON | PASS/FAIL | N | N | yes/no |

### Critical Issues (must fix)
[List all critical issues from both reviews]

### Warnings (should fix)
[List all warnings]
```

---

### Step 5: Enforce

- **If any verdict is FAIL**: State clearly that this TRR cannot be committed or advanced to the next phase until all critical issues are resolved. List the specific fixes needed. If the verdict contains `routed_issues`, suggest: "Run `/resolve-review $ARGUMENTS` to auto-route mechanical fixes and surface judgment calls, or fix manually and re-run `/review`."
- **If PASS_WITH_NOTES**: State that progression is allowed but recommend fixing warnings first. If warnings have `routed_issues`, note that `/resolve-review` can auto-fix mechanical warnings too.
- **If all PASS**: Confirm the artifact is ready for commit.

After manual fixes are made, tell the user to run `/review` again to verify. Do not self-certify fixes — the reviewer must re-validate.
