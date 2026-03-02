---
description: Deep parallel research on a topic using multiple researcher subagents
---

# Research: $ARGUMENTS

## Instructions

Conduct thorough research on the following topic:

> **$ARGUMENTS**

### Step 1: Identify Research Angles

Break the topic into 3-4 distinct research angles that can be investigated independently.

### Step 2: Launch Parallel Researchers

Spawn **one researcher subagent per angle**, all in parallel. Each should:
- Focus exclusively on their assigned angle
- Search the codebase, web, or documentation as appropriate
- Return structured findings

### Step 3: Synthesize

Once all researchers return, combine their findings into a single research document:

```markdown
# Research: [Topic]
Date: [today]

## Executive Summary
2-3 sentences on the key takeaway.

## Findings

### [Angle 1]
[Synthesized findings]

### [Angle 2]
[Synthesized findings]

### [Angle 3]
[Synthesized findings]

## Comparison / Analysis
[If comparing options, include a clear comparison]

## Recommendation
[Your recommendation based on all findings]

## Sources
[List of sources consulted]
```

### Step 4: Save

Save the research document to `outputs/research/` with a descriptive filename.
