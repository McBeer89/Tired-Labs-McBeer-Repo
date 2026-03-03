#!/usr/bin/env bash
# PreToolUse hook: Block destructive bash commands
# Exit 0 = allow, Exit 2 = block (message fed back to Claude)

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block rm -rf (suggest trash or targeted rm instead)
if echo "$CMD" | grep -qE 'rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|--recursive\s+--force|-[a-zA-Z]*f[a-zA-Z]*r)\s'; then
  echo "BLOCKED: Do not use rm -rf. Use targeted 'rm' on specific files, or move files to a temp directory first. Be surgical." >&2
  exit 2
fi

# Block direct push to main/master
if echo "$CMD" | grep -qE 'git\s+push\s+(origin\s+)?(main|master)(\s|$)'; then
  echo "BLOCKED: Do not push directly to main/master. Create a feature branch, push there, then merge." >&2
  exit 2
fi

# Block committing with unresolved [?] markers
if echo "$CMD" | grep -qE 'git\s+commit'; then
  # Check staged files for [?] markers
  MARKERS=$(git diff --cached --unified=0 2>/dev/null | grep -c '\[?\]' || true)
  if [ "$MARKERS" -gt 0 ]; then
    echo "BLOCKED: Staged files contain $MARKERS unresolved [?] markers. Resolve all uncertainties before committing. This is a core methodology rule — never commit with open questions." >&2
    exit 2
  fi
fi

exit 0
