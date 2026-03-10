---
description: Analyze recent session notes and audit logs to surface TRR workflow patterns — what's working, what's failing, where time is spent.
argument-hint: "[optional: 'week' for last 7 days, 'month' for last 30, or a specific date range]"
---

# Insights: $ARGUMENTS

Analyze recent TRR workflow activity and surface actionable patterns.

---

### Step 1: Gather Data

Collect the raw material for analysis. Default: last 7 days. Adjust based on $ARGUMENTS.

**Session notes:**
```bash
find docs/session-notes/ -name "*.md" -mtime -7 2>/dev/null | sort
```

**Audit log:**
```bash
if [ -f ~/.claude/bash-audit.log ]; then
  CUTOFF=$(python3 -c "from datetime import datetime,timedelta; print((datetime.utcnow()-timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ'))" 2>/dev/null || echo "1970-01-01T00:00:00Z")
  awk -v cutoff="$CUTOFF" '$0 >= cutoff' ~/.claude/bash-audit.log 2>/dev/null | tail -200
fi
```

**Git history:**
```bash
git log --oneline --since="7 days ago" --stat
```

**Hook activity (trr-prose-guard blocks):**
```bash
# Check git log for any commits that mention fixing detection language or prose guard issues
git log --all --oneline --since="7 days ago" --grep="detection language\|prose guard\|Fix --" 2>/dev/null
```

**Open questions across all WIP TRRs:**
```bash
grep -rn "\[?\]" "WIP TRRs" --include="*.md" --include="*.json" 2>/dev/null
```

If `$ARGUMENTS` specifies a different range (e.g., `month`, or `2026-02-01..2026-03-01`), adjust all queries accordingly.

---

### Step 2: Analyze Patterns

Read the gathered data and look for these patterns:

**TRR Production Health:**
- How many TRRs are in WIP status? How long has each been in WIP?
- How many phase commits happened this period? Which phases?
- How many sessions per TRR phase (from session notes)?
- Any phases that required multiple sessions when one should have sufficed?
- Any TRRs that appear stalled (no commits in 7+ days)?

**Quality Gate Patterns:**
- How many reviewer FAIL verdicts occurred? What failure categories?
- How many reviewer PASS_WITH_NOTES? What were the notes about?
- How many times did the trr-prose-guard hook likely fire? (Look for fix commits mentioning detection language.)
- How many times did the anti-rationalization Stop hook likely reject? (Hard to measure directly — look for sessions with multiple attempts at the same phase.)

**Failure Mode Frequency:**
- Which of the 9 documented failure modes appeared most often?
  - Detection language creep (FM1)
  - Re-walked pipelines (FM2)
  - Grouped telemetry (FM3)
  - Bare telemetry labels (FM4)
  - Prerequisite modeling (FM5)
  - Instance/procedure confusion (FM6)
  - Verbose overviews (FM7)
  - Phase 1 artifact leakage (FM8)
  - Telemetry enablement guidance (FM9)
- Look for patterns in fix commits, reviewer verdicts, and session note "Decisions Made" sections.

**Open Question Lifecycle:**
- How many `[?]` markers exist across all WIP TRRs?
- Are any `[?]` markers older than 2 sessions (carried forward without resolution)?
- What type of questions remain open? (lab-only, research-needed, scoping decisions)

**Context & Session Health:**
- How many auto-wrap notes were generated (indicates sessions hitting context limits)?
- How many manual `/wrap` notes vs. auto-wrap notes? (Manual should dominate.)
- Were session handoffs clean (does "What's Next" in session notes get acted on in the following session)?
- Any sessions with unfilled TODO sections in session notes?

**Tool Usage:**
- Most frequently used bash commands (from audit log)
- Source Scraper invocations (frequency and targets)
- WebFetch domains hit most often (what sources are being researched?)

---

### Step 3: Generate Recommendations

Based on the patterns, generate specific, actionable recommendations:

**If a failure mode keeps recurring:**
> "Failure Mode [N] ([name]) appeared [X] times this period. Consider: [specific countermeasure — add a hook check, add a reviewer checklist item, add a CLAUDE.md reminder]."

**If sessions are hitting context limits:**
> "[N] auto-wrap notes generated vs. [M] manual wraps. Sessions are running too long. Break phases more aggressively or use `/wrap` before the auto-wrap safety net fires."

**If `[?]` markers are aging:**
> "These questions have been open for [N] sessions: [list]. They need lab time, additional research, or a scoping decision from the PM."

**If reviewer FAILs are high:**
> "Reviewer returned FAIL [N] times. Most common: [pattern]. Consider adding a self-review step in the subagent that produces this artifact."

**If a specific source/domain is hit frequently:**
> "[domain] was fetched [N] times. Consider adding it to the researcher's standard source list or pre-fetching during Source Scraper runs."

---

### Step 4: Present Report

```markdown
# TRR Workflow Insights — [date range]

## Summary
[2-3 sentences: overall health of the TRR workflow this period]

## TRR Production
- **Active WIP TRRs**: [count]
- **Phase commits this period**: [count] ([breakdown by phase])
- **Sessions this period**: [count] (from session notes)
- **TRRs completed this period**: [count]
- **Stalled TRRs (no activity 7+ days)**: [list or "none"]

## Quality
- **Reviewer FAIL verdicts**: [count] — [top categories]
- **Detection language fixes**: [count]
- **Open questions across all WIP**: [count] — [N] older than 2 sessions

## Top Failure Modes This Period
1. [Most frequent failure mode — count and examples]
2. [Second]
3. [Third]
(If none detected, note that — it's a good sign.)

## Session Health
- **Manual wraps**: [count]
- **Auto-wraps (safety net)**: [count]
- **Average sessions per phase**: [estimate from data]

## Recommendations
1. [Specific, actionable change] — because [evidence from data]
2. [Specific, actionable change] — because [evidence from data]
3. [Specific, actionable change] — because [evidence from data]

## Unresolved from Previous Insights
[Recommendations from last insights report that haven't been acted on yet — or "First run, no history."]
```

---

### Step 5: Save and Track

Save the report to `docs/insights/YYYY-MM-DD.md` (create the `docs/insights/` directory if it doesn't exist).

Commit:
```bash
git add docs/insights/
git commit -m "docs: insights for [date]"
```

Suggest to the PM:
> "Run `/insights` weekly to track trends. Acting on one recommendation per week compounds — after a month your TRR production pipeline is measurably tighter."
