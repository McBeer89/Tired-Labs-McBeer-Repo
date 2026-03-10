---
description: Auto-route reviewer FAIL fixes to the appropriate subagents, then re-review. Max one automatic retry — escalates to user on second FAIL.
argument-hint: "<TRR ID> [platform - default: win]"
---

# Resolve Review: $ARGUMENTS

Auto-fix reviewer findings for:

> **$ARGUMENTS**

This command reads the most recent reviewer verdict, routes mechanical fixes
to the appropriate subagents, and re-runs the reviewer. It does NOT handle
judgment calls autonomously — those are surfaced to the user for decision.

---

### Step 1: Find the Reviewer Verdict

Locate the most recent reviewer output. Check in order:
1. Was a reviewer verdict returned earlier in the current session? (check conversation context)
2. Is there a review report in `WIP TRRs/$ARGUMENTS/win/Supporting Docs/`?

If no verdict found, run `/review $ARGUMENTS` first, then proceed with the result.

Parse the `routed_issues` array from the JSON verdict block.

If the verdict is already PASS or PASS_WITH_NOTES with no critical issues, report that and stop — nothing to fix.

---

### Step 2: Triage Issues

Separate the `routed_issues` into three buckets:

**Bucket A — Mechanical fixes (auto-route):**
All issues where `fix_type` is `mechanical`.
Group by `route_to` target.

**Bucket B — Judgment calls requiring research:**
Issues where `fix_type` is `judgment` AND `route_to` is `trr-researcher`.
These might be resolvable with additional research before escalating to the user.

**Bucket C — Judgment calls requiring user decision:**
- Issues where `fix_type` is `judgment` AND `route_to` is `orchestrator`
- Issues where `route_to` is `ddm-builder` with `fix_type: judgment` that could change procedure count or DDM structure
- Any issue that could cascade across multiple files (DDM change affecting prose)

---

### Step 3: Execute Mechanical Fixes (Bucket A)

Spawn subagents **in parallel** for each `route_to` group in Bucket A:

**If trr-writer issues exist:** spawn **trr-writer** with:
- The file to edit (`README.md`)
- The specific issues routed to it (listed by ID)
- The `fix_instruction` from each issue
- Instruction: apply fixes, run self-review checklist, return

**If ddm-builder issues exist:** spawn **ddm-builder** with:
- The DDM JSON file(s) to edit
- The specific issues routed to it (listed by ID)
- The `fix_instruction` from each issue
- The current procedure table (for reference, not for rewriting)
- Instruction: apply fixes, run validation checklist, return

These are independent — trr-writer fixes prose, ddm-builder fixes JSON. They run simultaneously.

Wait for all Bucket A agents to return.

---

### Step 4: Execute Research Fixes (Bucket B)

If Bucket B is non-empty, spawn **trr-researcher** subagents for each research question. Each researcher receives:
- The specific issue and what needs verification
- The current research notes from `Supporting Docs/`
- Instructions to return a definitive answer or mark as still-unresolved

After researchers return:
- If the answer resolves the issue: spawn the appropriate agent from the `route_to` field to make the change
- If still unresolved: move the issue to Bucket C (escalate to user)

---

### Step 5: Present Judgment Calls (Bucket C)

If Bucket C is non-empty, present each issue to the user with options:

```markdown
## Issues Requiring Your Decision

These cannot be auto-fixed — they involve scoping decisions, procedure
distinctness, or structural changes that need your judgment.

### [C2] inclusion_test: "Download Payload" fails immutability
**File:** ddms/ddm_trr0030_win.json — Node n7
**Reviewer says:** Delivery method is attacker-controlled
**Options:**
  1. Remove node n7 and redefine the pipeline entry point
  2. Keep n7 but rename/redefine as the first immutable operation after delivery
  3. Research further — spawn a researcher to investigate
  4. Override — keep as-is with documented rationale

**What would you like to do?**
```

Wait for user input on each Bucket C item. Apply their decisions by spawning the appropriate agent.

If Bucket C is empty (all issues were mechanical or research-resolved), skip this step.

---

### Step 6: Re-Review

After all fixes are applied (Buckets A + B resolved, Bucket C decided by user):

Spawn **reviewer** to re-validate the same artifacts.

**If PASS or PASS_WITH_NOTES:** Report success. The artifact is ready for commit or phase progression.

**If FAIL again:** Do NOT auto-retry a second time. Present the remaining issues to the user:

```markdown
## Second FAIL — Escalating

The reviewer found additional issues after the first round of fixes.
Auto-routing has reached its one-retry limit to prevent token-burning loops.

### Remaining Critical Issues
[list them with full routed_issues detail]

### Recommendation
Fix these manually and re-run `/review`, or run `/resolve-review` again
after making targeted adjustments.
```

The one-retry limit prevents loops where the system chases its tail on issues that need human judgment or where a fix introduces a new problem.

---

### Step 7: Summary

Present a summary regardless of outcome:

```markdown
## Resolve-Review Summary: $ARGUMENTS

| Bucket | Issues | Resolved | Escalated |
|--------|--------|----------|-----------|
| Mechanical (auto) | N | N | — |
| Research (auto) | N | N | N moved to user |
| Judgment (user) | N | N | — |

**Final verdict:** PASS / PASS_WITH_NOTES / FAIL (escalated)

**Agents spawned:** [list with what each fixed]
**Files modified:** [list]
**Re-review result:** [verdict]
```

If the final verdict is PASS and this was called from within `/trr` or `/ddm`, signal to the orchestrator that phase progression can continue.
