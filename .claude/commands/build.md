---
description: Build something end-to-end with research, implementation, and review subagents
---

# Build: $ARGUMENTS

## Instructions

Build the following:

> **$ARGUMENTS**

Follow this process using subagents:

### Step 1: Quick Research

Spawn a **researcher subagent** to:
- Check if relevant code already exists in the project
- Identify any patterns, conventions, or dependencies to follow
- Note any potential gotchas

### Step 2: Implement

Based on the research, spawn one or more **coder subagents**. If the work has independent parts, spawn multiple coders in parallel. For example:
- One coder for the main implementation
- Another coder for tests (if the implementation doesn't depend on test structure)

Each coder should:
- Follow existing project conventions found by the researcher
- Write clean, documented code
- Run their code to verify it works if possible

### Step 3: Review

Spawn a **reviewer subagent** to:
- Check all new/modified code for bugs, security issues, and style
- Run any available test suites
- Verify the implementation matches the original goal

### Step 4: Report

If the reviewer passes the code, present a summary:
- What was built
- Files created/modified
- How to use it
- Any follow-up items

If the reviewer finds issues, fix them and re-review. Do not present work that hasn't passed review.
