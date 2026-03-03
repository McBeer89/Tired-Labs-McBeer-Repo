---
description: Scan all files in a TRR folder for unresolved [?] markers and resolve them using parallel research agents.
argument-hint: "<TRR ID> (e.g. TRR0028)"
---

# Resolve: $ARGUMENTS

Hunt and resolve all unresolved `[?]` markers in:

> **$ARGUMENTS**

---

### Step 1: Scan for [?] Markers

Read every file in `WIP TRRs\$ARGUMENTS\` recursively:
- `Supporting Docs\*.md`
- `ddms\*.json`
- `README.md` (if it exists)

Collect every `[?]` item into a list with:
- The question text
- The file it came from
- The line number

If no `[?]` markers are found — report that and stop. Nothing to do.

---

### Step 2: Triage

Group the `[?]` items by type:
- **Telemetry behavior** — does X telemetry fire in Y scenario?
- **API/OS behavior** — does this API behave this way on this platform?
- **Platform constraint** — is this prerequisite/limitation correct?
- **Procedure distinctness** — is this a different procedure or the same?
- **Lab-only** — cannot be resolved without empirical testing (flag these, do not attempt to research)

Flag any `[?]` items that are **lab-only** immediately — list them separately and do not spawn researchers for them. These must be resolved through lab validation, not research.

---

### Step 3: Parallel Research

For each resolvable group, spawn one **trr-researcher subagent** per group in parallel.

Each researcher receives:
- The specific `[?]` questions in its group
- The context from the file where they appeared
- Instructions to find a definitive answer from primary sources (Microsoft docs, GitHub, security research)
- Instructions to mark answers as `[CONFIRMED]`, `[LIKELY]`, or `[UNRESOLVED]` with source citations

Wait for all researchers to return.

---

### Step 4: Update Source Documents

For each resolved item:
- Replace the `[?]` marker in the source file with the confirmed answer
- Add a source citation inline
- If the answer changes a DDM operation or telemetry tag, flag it explicitly for manual review — do not silently update DDM JSON

For each `[UNRESOLVED]` item (researched but still uncertain):
- Leave the `[?]` marker in place
- Append the researcher's findings as a note below the question
- Add to the lab-only list

---

### Step 5: Report

```markdown
## Resolve Report: $ARGUMENTS

### Resolved
- [?] [question] → [answer] ([source]) — updated in [file]

### Escalated to Lab (cannot resolve through research)
- [?] [question] — requires empirical testing: [why]

### Unresolved (researched, still uncertain)
- [?] [question] — findings: [what was found], still needs: [what's missing]

### DDM Impact (requires manual review)
- [item] — [how it may affect DDM operations or telemetry]
```

Present the report and ask: are there any lab-only items you want to attempt to resolve now, or should we proceed with the remaining open questions documented?
