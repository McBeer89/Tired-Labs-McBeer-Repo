---
description: Show current project status including recent work, git state, and outputs
---

# Status

## Instructions

Give a quick overview of the current project state. Check these things:

### Git Status
```bash
git status --short
git log --oneline -10
```

### Recent Outputs
```bash
find outputs/ -type f -name "*.md" -mtime -7 2>/dev/null | head -20
```

### Project Structure
```bash
ls -la
```

### Present

Summarize in a clean format:

**Recent Activity**: What's been done in the last few commits.

**Current State**: Any uncommitted changes, what branch we're on.

**Outputs**: List of recent deliverables in `outputs/`.

**Pending**: Anything that looks unfinished or needs attention.
