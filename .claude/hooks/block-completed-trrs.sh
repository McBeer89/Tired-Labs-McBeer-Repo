#!/usr/bin/env bash
# PreToolUse hook: Block edits to completed/accepted TRR core files.
# Allows writes to kql/ subdirectories (derivative outputs).
# Exit 0 = allow, Exit 2 = block (message fed back to Claude)

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')

PROTECTED_DIR="Completed TRR Reports"

block() {
  echo "BLOCKED: $1" >&2
  echo "" >&2
  echo "Completed TRRs are reviewed and accepted. Their core files" >&2
  echo "(README.md, ddms/, images/) are read-only." >&2
  echo "" >&2
  echo "KQL derivative queries in kql/ subdirectories ARE allowed." >&2
  echo "" >&2
  echo "Report any findings to the user and move on. Do not attempt" >&2
  echo "to fix completed TRR files or create log files for them." >&2
  exit 2
}

# --- Guard: Write / Edit / MultiEdit tools (file path check) ---
if [[ "$TOOL" == "Write" || "$TOOL" == "Edit" || "$TOOL" == "MultiEdit" ]]; then
  FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty')

  # Only check files inside the protected directory
  if echo "$FILE_PATH" | grep -qF "$PROTECTED_DIR"; then
    # ALLOW writes to kql/ subdirectories (derivative output)
    if echo "$FILE_PATH" | grep -qiE '/kql/|\\kql\\'; then
      exit 0
    fi
    # Block everything else in the protected directory
    block "Attempted to edit '$FILE_PATH' which is inside '$PROTECTED_DIR'."
  fi
fi

# --- Guard: Bash tool (catch sed, echo, mv, cp, rm, etc.) ---
if [[ "$TOOL" == "Bash" ]]; then
  CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

  # Only check commands that reference the protected directory
  if echo "$CMD" | grep -qF "$PROTECTED_DIR"; then
    # ALLOW read-only commands
    if echo "$CMD" | grep -qiE '^\s*(cat|head|tail|less|more|grep|find|ls|dir|wc|diff|git\s+(log|show|diff|status))\b'; then
      exit 0
    fi
    # ALLOW commands targeting kql/ specifically
    if echo "$CMD" | grep -qiE '/kql/|\\kql\\|/kql"|\\kql"'; then
      exit 0
    fi
    # Block write-like commands
    if echo "$CMD" | grep -qiE '(sed\b|awk\b|echo\b.*>|printf\b.*>|tee\b|>\s|>>\s|mv\b|cp\b|rm\b|chmod\b|chown\b|patch\b|truncate\b|mkdir\b)'; then
      block "Bash command references '$PROTECTED_DIR' with a write operation."
    fi
  fi
fi

exit 0
