# Claude Code Configuration for TIRED Labs TRR Research

Hardened Claude Code configuration for producing Technique Research Reports (TRRs) and Detection Data Models (DDMs) following the TIRED Labs methodology. Adapted from patterns in [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config), tailored for technique research workflows.

## What's Different from the Previous Setup

This version adds three layers that the original `.claude/` setup was missing:

**1. Enforcement hooks** — `settings.json` includes PreToolUse hooks that block detection-oriented language in TRR files before they're written, block commits containing `[?]` markers, and prevent destructive bash commands. A Stop hook powered by a fast model catches rationalization patterns (declaring incomplete work done, hedging on the inclusion test, blowing past phase gates).

**2. Hard failure-mode rules** — The CLAUDE.md now includes explicit "never do this" constraints learned from TRR0000: detection language creep, re-walked shared pipelines, grouped telemetry, bare telemetry labels, prerequisites modeled as inline steps, and tool-focused analysis. These were previously only in the claude.ai Project system prompt — Claude Code couldn't see them.

**3. Reviewer enforcement** — The reviewer agent now returns structured JSON verdicts (`PASS`/`FAIL`/`PASS_WITH_NOTES`) with `blocking: true/false`. Commands check these verdicts and block progression on FAIL. A FAIL from the reviewer means the work doesn't get committed until the issues are fixed and the reviewer passes on a re-run.

## Installation

### From Scratch

Copy these files into your repo root:

```
your-repo/
├── CLAUDE.md                          ← Orchestrator instructions (replaces old one)
├── settings.json                      ← Copy to ~/.claude/settings.json
├── hooks/
│   ├── block-destructive.sh           ← PreToolUse: blocks rm -rf, push to main, [?] commits
│   └── trr-prose-guard.sh             ← PreToolUse: blocks detection language in TRR files
├── .claude/
│   ├── agents/
│   │   ├── trr-researcher.md          ← Research subagent (updated)
│   │   ├── ddm-builder.md             ← DDM construction subagent (updated)
│   │   ├── trr-writer.md              ← TRR document writer (updated)
│   │   ├── coder.md                   ← Code/script implementation (unchanged)
│   │   └── reviewer.md                ← Quality reviewer (hardened, JSON verdicts)
│   └── commands/
│       ├── trr.md                     ← /trr — full pipeline with enforcement
│       ├── scope.md                   ← /scope — Phase 1 scoping
│       ├── ddm.md                     ← /ddm — Phases 2-3
│       ├── review.md                  ← /review — standalone review with enforcement
│       ├── plan.md                    ← /plan — goal decomposition
│       └── status.md                  ← /status — repo and TRR state
```

### Settings

`settings.json` goes to `~/.claude/settings.json` (global) or stays in the repo root (project-level). The template includes:

- `alwaysThinkingEnabled: true` — extended thinking stays on across sessions. Critical for DDM reasoning.
- `cleanupPeriodDays: 365` — keeps conversation history for a year.
- `hooks` — see below.
- `permissions.deny` — blocks reading SSH keys, cloud creds, and editing shell config.

If you already have a `~/.claude/settings.json`, merge the `hooks` and `permissions` sections into your existing file rather than replacing it.

### Hooks

The `hooks/` directory must be in your repo root (or adjust the paths in `settings.json`).

| Hook | Event | What It Does |
|------|-------|-------------|
| `block-destructive.sh` | PreToolUse (Bash) | Blocks `rm -rf`, direct push to main/master, and `git commit` when staged files contain `[?]` markers |
| `trr-prose-guard.sh` | PreToolUse (Write/Edit) | Scans content being written to TRR `.md` files for detection-oriented language, tool-focused analysis, numbered step lists, and bare telemetry labels. Blocks with specific feedback. |
| Stop hook (prompt) | Stop | Sends Claude's final response to a fast model that checks for rationalization, skipped phase gates, incomplete inclusion tests, detection creep, and tool-focused analysis. Rejects with specific fix instructions. |
| Bash audit log | PostToolUse (Bash) | Appends every bash command to `.claude/bash-audit.log` with timestamp. |

Make hook scripts executable:
```bash
chmod +x hooks/block-destructive.sh hooks/trr-prose-guard.sh
```

## How It Works

### The Enforcement Chain

```
You type /trr T1505.003 win
  │
  ├→ Phase 1: Researchers run in parallel → scoping document
  │   └→ STOP gate: presents findings, waits for your OK
  │
  ├→ Phase 2: DDM builder runs → master DDM JSON
  │   └→ trr-prose-guard hook catches detection language if writing TRR notes
  │   └→ STOP gate: presents DDM, waits for your OK
  │
  ├→ Phase 3: Researcher + DDM builder → procedures + exports
  │   └→ Reviewer runs → structured JSON verdict
  │   └→ If FAIL: orchestrator must fix and re-review
  │   └→ STOP gate: presents procedures + verdict
  │
  ├→ Phase 4: TRR writer runs → README.md
  │   └→ trr-prose-guard hook blocks detection language on write
  │   └→ Reviewer runs → structured JSON verdict
  │   └→ If FAIL: orchestrator must fix and re-review
  │
  └→ Phase 5: Commit
      └→ block-destructive hook blocks commit if [?] markers in staged files
      └→ Stop hook checks final response for rationalization
```

### What the Stop Hook Catches

The prompt-based Stop hook runs after every Claude response and checks for:

1. **Rationalization** — "pre-existing," "out of scope" (without exclusion table entry), "follow-up" (unrequested), "probably," "likely" without verification
2. **Skipped phase gates** — blowing past STOP checkpoints without user confirmation
3. **Incomplete inclusion test** — adding DDM operations without explicit essential/immutable/observable verdicts
4. **Detection language creep** — prescriptive detection framing in TRR prose
5. **Tool-focused analysis** — naming tools as operation subjects

If any check fails, the Stop hook rejects the response and tells Claude exactly what to fix. Claude must address the issue before the response is accepted.

### Reviewer Verdicts

The reviewer returns structured JSON:

```json
{
  "verdict": "FAIL",
  "critical_count": 2,
  "warning_count": 1,
  "blocking": true
}
```

- **FAIL** (`blocking: true`): Work cannot be committed. All critical issues must be fixed and reviewer re-run.
- **PASS_WITH_NOTES** (`blocking: false`): Work can proceed. Warnings should be fixed.
- **PASS** (`blocking: false`): Clean. Ready for commit.

Automatic FAIL triggers: any detection language, any unresolved `[?]` marker, any DDM operation without full inclusion test verdict.

## Commands

| Command | Phases | What It Does |
|---------|--------|-------------|
| `/trr <technique>` | 1-4 | Full pipeline: scope → DDM → procedures → TRR document |
| `/scope <technique>` | 1 | Scoping document + essential constraints table only |
| `/ddm <TRR ID>` | 2-3 | DDM construction + procedure identification (requires Phase 1) |
| `/review [target]` | — | Run reviewer against TRR doc and/or DDM files |
| `/plan <goal>` | — | Decompose any goal into a researched plan |
| `/status` | — | Show repo state, active TRR work, phase completion |

## Agents

| Agent | Model | Tools | Role |
|-------|-------|-------|------|
| trr-researcher | Sonnet | Read, Glob, Grep, WebSearch, WebFetch | Research with inclusion test tagging |
| ddm-builder | Sonnet | Read, Write, Edit, Glob, Grep | DDM JSON with explicit per-operation verdicts |
| trr-writer | Sonnet | Read, Write, Edit, Glob, Grep | Discipline-neutral TRR prose |
| coder | Sonnet | Read, Write, Edit, Grep, Glob, Bash | Scripts, automation, tooling |
| reviewer | Sonnet | Read, Glob, Grep | Quality gate with structured JSON verdicts |

The orchestrator (you talking to Claude Code) runs on whatever model you've selected. Use Opus for complex analytical work (scoping, DDM validation, procedure differentiation). Sonnet handles routine tasks fine.

## Session Discipline

The CLAUDE.md instructs the orchestrator to treat each phase as a session boundary by default. This means:

- Phase 1 (scope) → commit → optionally new session
- Phase 2 (DDM) → commit → optionally new session
- Phase 3 (procedures) → commit → optionally new session
- Phase 4 (TRR doc) → commit → done

The orchestrator will recommend a fresh session when context is getting heavy. This is especially important for complex techniques with 3+ procedures or deep technical backgrounds.

## Differences from Trail of Bits Config

This setup borrows concepts from `trailofbits/claude-code-config` but is purpose-built for technique research:

| ToB Concept | Adaptation |
|---|---|
| Anti-rationalization Stop hook | Tailored for TRR-specific rationalization patterns (inclusion test hedging, phase gate skipping) |
| PreToolUse blocking hooks | Domain-specific: detection language guard, `[?]` marker commit guard |
| CLAUDE.md hard rules | Failure modes from actual TRR0000 work, not generic coding standards |
| Reviewer enforcement | Structured JSON verdicts with blocking semantics, not advisory-only |
| Session discipline | Phase-boundary scoping, not arbitrary task scoping |
| Bash audit logging | Carried forward as-is — useful for post-session review |
