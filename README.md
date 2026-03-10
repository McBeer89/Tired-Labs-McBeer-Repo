# Claude Code Configuration for TIRED Labs TRR Research

Hardened Claude Code configuration for producing Technique Research Reports (TRRs) and Detection Data Models (DDMs) following the [TIRED Labs methodology](https://library.tired-labs.org). Adapted from patterns in [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config), tailored for technique research.

## Quick Start

**Starting a new TRR:**
```
cd /path/to/this/repo
claude
> /trr T1546.003 win
```

**Resuming work:**
```
claude
> pick up where we left off
```
The orchestrator reads the latest session note from `docs/session-notes/` and presents what's next. Or run `/status` to see where things stand.

**Pre-session research** (optional but saves tokens): run the TRR Source Scraper before opening Claude Code, then pass the output path when starting `/trr` or `/scope`.

---

## Setup

### Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- Git
- `jq` (required by hooks — `brew install jq`, `apt install jq`, or `choco install jq`)
- [Arrows.app](https://arrows.app) account (free, web-based — for DDM visualization)

### 1. Clone and Enter the Repo

```bash
git clone <repo-url>
cd tired-labs
```

### 2. Install Global Hooks

The global hooks live in `~/.claude/hooks/` and apply to all Claude Code projects. Create them manually — the scripts are documented in the [Hooks](#hooks) section below.

If you already have a `~/.claude/settings.json`, merge the `hooks` and `permissions` entries from the Settings Architecture section. If not, create one with at minimum:

```json
{
  "alwaysThinkingEnabled": true,
  "cleanupPeriodDays": 365,
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/block-destructive.sh" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/bash-audit-log.sh" }]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/notify-stop.sh" }]
      }
    ]
  },
  "permissions": {
    "deny": [
      "Read(~/.ssh/**)",
      "Read(~/.gnupg/**)",
      "Read(~/.aws/**)",
      "Read(~/.git-credentials)",
      "Edit(~/.bashrc)",
      "Edit(~/.zshrc)",
      "Edit(~/.bash_profile)"
    ]
  }
}
```

### 3. Make Project Hooks Executable

```bash
chmod +x .claude/hooks/trr-prose-guard.sh
```

### 4. Create Project-Level Settings

The project-level `.claude/settings.local.json` is gitignored because it accumulates machine-specific permission allows. Create it with the TRR-specific hooks:

```json
{
  "permissions": {
    "allow": []
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/trr-prose-guard.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review the assistant's final response for signs of rationalizing incomplete work. This is a TRR research workflow where thoroughness is non-negotiable. Reject the response if the assistant exhibits ANY of these patterns:\n\n1. Claiming issues are 'pre-existing' or 'out of scope' to avoid fixing them (unless the item is already documented in the Exclusion Table)\n2. Saying there are 'too many issues' to address all of them\n3. Deferring work to a 'follow-up' that was not requested by the user\n4. Listing problems without fixing them and declaring the phase done\n5. Skipping a STOP checkpoint without presenting findings to the user and waiting for confirmation\n6. Declaring a TRR phase complete when unresolved open question markers remain in TRR files\n7. Saying 'I'll leave this for the next session' for work that belongs in the current phase\n8. Accepting a reviewer FAIL verdict without fixing all critical issues\n9. Presenting a DDM operation without an explicit essential/immutable/observable verdict\n10. Moving to the next phase before the current phase's stop gate has been cleared by the user\n\nIf the response shows any of these patterns, respond with {\"ok\": false, \"reason\": \"You are rationalizing incomplete work. [identify the specific pattern and what needs to be finished]. Go back and complete the work.\"}.\n\nIf the work is genuinely complete, the user explicitly asked to stop, or the assistant is appropriately recommending a session wrap due to context limits, respond with {\"ok\": true}."
          }
        ]
      }
    ]
  }
}
```

If the relative path for `trr-prose-guard.sh` doesn't fire during your first session (test by writing detection language to a TRR file), replace it with the absolute path to `<repo-root>/.claude/hooks/trr-prose-guard.sh`.

### 5. Verify

Open Claude Code in the repo and run `/status`. You should see the repo state and any existing TRR work. The hooks will begin accumulating permission allows in `settings.local.json` as you approve them during use.

---

## What This Does

This configuration turns Claude Code into a gated, multi-agent TRR production pipeline with four layers of enforcement:

**1. Enforcement hooks** — PreToolUse hooks block detection-oriented language in TRR files before they're written, block commits containing `[?]` markers, and prevent destructive bash commands. A prompt-based Stop hook powered by a fast model catches rationalization patterns (declaring incomplete work done, hedging on the inclusion test, blowing past phase gates).

**2. Hard failure-mode rules** — The CLAUDE.md includes explicit "never do this" constraints learned from production TRR work: detection language creep, re-walked shared pipelines, grouped telemetry, bare telemetry labels, prerequisites modeled as inline steps, tool-focused analysis, Phase 1 artifact leakage, and telemetry enablement guidance. Nine documented failure modes, each with specific symptoms and corrections.

**3. Reviewer enforcement** — The reviewer agent returns structured JSON verdicts (`PASS`/`FAIL`/`PASS_WITH_NOTES`) with `blocking: true/false`. Commands check these verdicts and block progression on FAIL. A FAIL means the work doesn't get committed until issues are fixed and the reviewer passes on re-run.

**4. Session lifecycle management** — `/wrap` captures structured handoff notes at phase boundaries. `/insights` analyzes session patterns over time. Auto-wrap fires before context compaction as a safety net. The orchestrator proactively recommends session breaks when context gets heavy.

---

## Project Layout

```
repo-root/
├── CLAUDE.md                              ← Orchestrator instructions (rules, failure modes, session discipline)
├── .claude/
│   ├── agents/
│   │   ├── trr-researcher.md              ← Research with inclusion test tagging
│   │   ├── ddm-builder.md                 ← DDM JSON with per-operation verdicts
│   │   ├── trr-writer.md                  ← Discipline-neutral TRR prose
│   │   ├── coder.md                       ← Scripts, automation, tooling
│   │   └── reviewer.md                    ← Quality gate with JSON verdicts + Bash verification
│   ├── commands/
│   │   ├── trr.md                         ← /trr — full pipeline with enforcement
│   │   ├── scope.md                       ← /scope — Phase 1 scoping
│   │   ├── ddm.md                         ← /ddm — Phases 2-3
│   │   ├── review.md                      ← /review — standalone review
│   │   ├── resolve.md                     ← /resolve — hunt and fix [?] markers
│   │   ├── plan.md                        ← /plan — goal decomposition
│   │   ├── status.md                      ← /status — repo, TRR state, session health
│   │   ├── wrap.md                        ← /wrap — end-of-session handoff
│   │   ├── commit.md                      ← /commit — TRR commit convention
│   │   └── insights.md                    ← /insights — workflow pattern analysis
│   ├── hooks/
│   │   └── trr-prose-guard.sh             ← PreToolUse: blocks detection language in TRR files
│   └── settings.local.json               ← Project-level settings (hooks, permissions) — gitignored
├── docs/
│   ├── session-notes/                     ← /wrap and auto-wrap output
│   ├── insights/                          ← /insights reports
│   └── plans/                             ← /plan output for non-TRR goals
├── Research Start-Up/                     ← Human-oriented AI-assisted research guides (for claude.ai, not Claude Code)
├── WIP TRRs/                              ← Active TRR work
├── Completed TRR Reports/                 ← Finished TRRs
└── tools/
    └── trr-source-scraper/                ← Pre-session automated source gathering
```

### Research Start-Up Directory

The `Research Start-Up/` folder contains guides for the **human-oriented, AI-assisted workflow** — using claude.ai Projects (not Claude Code) for TRR research. This includes the TRR Research Methodology Guide, the AI-Assisted TRR Research Guide, and prompt templates for local models. These documents are for the analyst working interactively with Claude in a browser, not for the automated Claude Code pipeline. Both workflows produce TRRs following the same methodology; they differ in how the human and AI divide the work.

### Gitignored Files

The following are excluded from version control (see `.gitignore`):

- `.claude/settings.local.json` — machine-specific permission allows accumulate per-user
- `.claude/bash-audit.log` — local audit trail, not shared
- `tools/trr-source-scraper/output/` — scraper cache and generated output
- Hardware-specific local model configs in `Research Start-Up/Prompts/`

If cloning fresh, these files won't exist. `settings.local.json` rebuilds as Claude Code prompts you for permissions during use. The scraper output directory is created on first run.

---

## Settings Architecture

Settings are split across two layers that merge at runtime:

**Global** (`~/.claude/settings.json`): Privacy env vars, credential deny rules, shell config protection, `alwaysThinkingEnabled`, `cleanupPeriodDays: 365`, and hooks that apply to all projects — `block-destructive.sh`, `code-quality-check.sh`, `bash-audit-log.sh`, `auto-wrap.sh`, `notify-stop.sh`, and a generic anti-rationalization Stop prompt.

**Project** (`.claude/settings.local.json`): TRR-specific hooks that layer on top of global — `trr-prose-guard.sh` on Write/Edit operations, and a TRR-specific anti-rationalization Stop prompt with 10 domain-specific rejection patterns. Also contains accumulated permission allows for research domains.

The project file is gitignored (machine-specific). The global file lives outside the repo.

---

## Hooks

### Global Hooks (`~/.claude/hooks/`)

| Hook | Event | What It Does |
|------|-------|-------------|
| `block-destructive.sh` | PreToolUse (Bash) | Blocks `rm -rf`, direct push to main/master, and `git commit` when staged files contain `[?]` markers |
| `code-quality-check.sh` | PreToolUse (Write/Edit) | Blocks hardcoded credentials, debug leftovers, and protects sacred files (CLAUDE.md, settings, hooks) |
| `bash-audit-log.sh` | PostToolUse (Bash) | Appends every bash command to `~/.claude/bash-audit.log` with timestamp |
| `auto-wrap.sh` | PreCompact | Safety net — writes a lightweight session note before context compaction. Manual `/wrap` is always preferred. |
| `notify-stop.sh` | Stop | Desktop/terminal notification when Claude needs attention |
| `session-start.sh` | SessionStart | Session initialization |
| Stop prompt (generic) | Stop | Fast-model check for rationalization patterns (generic, all projects) |

### Project Hooks (`.claude/hooks/`)

| Hook | Event | What It Does |
|------|-------|-------------|
| `trr-prose-guard.sh` | PreToolUse (Write/Edit) | Scans TRR markdown for detection language, tool-focused analysis, numbered step lists, bare telemetry labels. Blocks with specific feedback. |
| Stop prompt (TRR-specific) | Stop | 10-pattern TRR rationalization check: inclusion test hedging, phase gate skipping, `[?]` rationalization, reviewer FAIL acceptance, incomplete DDM verdicts |

---

## How It Works

### The Enforcement Chain

```
You type /trr T1505.003 win
  │
  ├→ Step 0: Create directory scaffold, assemble context for researchers
  │
  ├→ Phase 1: 3 researchers run in parallel → scoping document
  │   └→ Commit phase artifacts
  │   └→ STOP gate: presents findings, waits for your OK
  │
  ├→ Phase 2: DDM builder runs → master DDM JSON
  │   └→ trr-prose-guard fires on any TRR file writes
  │   └→ Commit phase artifacts
  │   └→ STOP gate: presents DDM, waits for your OK
  │
  ├→ Phase 3: Researcher + DDM builder → procedures + per-procedure exports
  │   └→ Reviewer runs → structured JSON verdict
  │   └→ If FAIL: fix and re-review (no progression until PASS)
  │   └→ Commit phase artifacts
  │   └→ STOP gate: presents procedures + verdict
  │
  ├→ Phase 4: TRR writer runs → README.md
  │   └→ trr-prose-guard fires on write
  │   └→ Reviewer runs → structured JSON verdict
  │   └→ If FAIL: fix and re-review
  │   └→ Commit phase artifacts
  │   └→ block-destructive hook blocks commit if [?] in staged files
  │
  └→ At every response: Stop hook checks for rationalization
      └→ At session end: /wrap captures handoff note
```

Commits happen inline at each phase gate — there is no separate "commit phase." Each phase's artifacts are committed immediately after they pass review, before the next phase begins.

### What the Stop Hook Catches

The TRR-specific prompt-based Stop hook runs after every Claude response and checks for:

1. Claiming issues are "pre-existing" or "out of scope" without an Exclusion Table entry
2. Saying there are "too many issues" to address
3. Deferring work to a "follow-up" that was not requested
4. Listing problems without fixing them and declaring the phase done
5. Skipping a STOP checkpoint without presenting findings and waiting for confirmation
6. Declaring a phase complete when `[?]` markers remain
7. Saying "I'll leave this for the next session" for current-phase work
8. Accepting a reviewer FAIL without fixing all critical issues
9. Presenting a DDM operation without an explicit essential/immutable/observable verdict
10. Moving to the next phase before the current phase gate is cleared by the user

If any pattern matches, the hook rejects the response with specific fix instructions. Claude must address the issue before the response is accepted.

---

## Commands

| Command | What It Does |
|---------|-------------|
| `/trr <technique>` | Full pipeline: Step 0 setup → Phase 1 scope → Phase 2 DDM → Phase 3 procedures → Phase 4 TRR document |
| `/scope <technique>` | Phase 1 only: scoping document + essential constraints table |
| `/ddm <TRR ID>` | Phases 2-3: DDM construction + procedure identification (requires completed Phase 1) |
| `/resolve <TRR ID>` | Scan TRR folder for `[?]` markers, triage by type, resolve via parallel research |
| `/review [target]` | Run reviewer against TRR document and/or DDM files |
| `/plan <goal>` | Decompose any goal into a researched, actionable plan |
| `/status` | Show repo state, active TRR phase status, DDM inventory, session health |
| `/wrap [summary]` | End-of-session handoff: captures TRR state, subagent returns, decisions, next steps |
| `/commit [context]` | Generate commit message following TRR convention, present for approval, commit |
| `/insights [range]` | Analyze session notes and audit logs for workflow patterns, failure mode frequency, session health |

---

## Agents

| Agent | Model | Tools | Role |
|-------|-------|-------|------|
| trr-researcher | Opus | Read, Glob, Grep, WebSearch, WebFetch | Research with inclusion test tagging, fetch discipline, confidence labels |
| ddm-builder | Opus | Read, Write, Edit, Glob, Grep | DDM JSON with per-operation verdicts, shared/independent pipeline export convention |
| trr-writer | Opus | Read, Write, Edit, Glob, Grep | Discipline-neutral TRR prose, Phase 1 condensation, self-review checklist |
| coder | Sonnet | Read, Write, Edit, Grep, Glob, Bash | Scripts, automation, Source Scraper, DDM tooling |
| reviewer | Opus | Read, Glob, Grep, Bash | Quality gate with JSON verdicts, on-disk verification (JSON validity, file existence) |

The orchestrator (you talking to Claude Code) runs on whatever model you've selected. The four quality-critical agents (researcher, DDM builder, writer, reviewer) run on Opus for reasoning depth. The coder runs on Sonnet — its tasks are structured implementation, not judgment calls.

---

## Session Lifecycle

### Phase Boundaries

Each TRR phase is a natural session boundary. The orchestrator commits at each gate and recommends fresh sessions when context gets heavy:

- Phase 1 (scope) → commit → wrap → optionally new session
- Phase 2 (DDM) → commit → wrap → optionally new session
- Phase 3 (procedures) → commit → wrap → optionally new session
- Phase 4 (TRR doc) → commit → wrap → done

### Session Handoff

`/wrap` writes a structured note to `docs/session-notes/` capturing: what was accomplished, active TRR phase state, subagent returns, decisions made, open questions (using `OPEN:` prefix, not `[?]`), and concrete next steps. The next session reads this note plus current TRR artifacts to resume without re-reading everything.

### Context Awareness

The CLAUDE.md includes proactive wrap triggers — the orchestrator is instructed to recommend wrapping when it detects 3+ subagent round-trips, self-summarization of earlier findings, heavy source fetches, or a second reviewer FAIL in the same session.

### Auto-Wrap Safety Net

The global `auto-wrap.sh` PreCompact hook fires before context compaction and writes a lightweight session note with git state. This is the emergency fallback — it captures state but not intent. Manual `/wrap` is always preferred.

---

## TRR Directory Structure

```
WIP TRRs/
  TRR####/
    win/
      ddms/
        ddm_trr####_win.json          ← Master DDM (all black arrows)
        trr####_win_a.json            ← Procedure A export (red arrows on active path)
        trr####_win_b.json            ← Procedure B export
        trr####_win_a.png             ← Arrows.app render
        trr####_win_b.png
      images/                         ← Supplementary screenshots and diagrams
      Supporting Docs/                ← Phase 1 research, procedure notes (not in final TRR)
      Procedure Lab/                  ← Lab recreation notes
      README.md                       ← The TRR document
```

### Per-Procedure DDM Export Convention

Per-procedure exports follow a shared vs. independent pipeline rule:

- **Shared pipeline**: When procedures branch from a common pipeline (e.g., A and B diverge after "Execute Code"), each export contains the **entire DDM** with the active path in red and inactive paths in black. The reader needs the full picture to see the divergence point.
- **Independent pipeline**: When a procedure has its own completely separate operation chain with no shared operations, its export contains **only that procedure's nodes and relationships**. Including the unrelated pipeline would be visual noise.
- **Mixed**: A single TRR can have both. Shared-pipeline procedures get full DDM exports; independent procedures get isolated exports.

---

## Commit Convention

```
TRR####: Phase 1 -- Initial overview and technical background
TRR####: Phase 2 -- DDM draft with telemetry map
TRR####: Phase 3 -- Procedures identified (WIN.A, WIN.B), DDM validated
TRR####: Phase 4 -- TRR document complete
TRR####: Derivative -- Detection methods document
TRR####: Fix -- Post-review corrections
tools: [description]
docs: session notes / insights / methodology
```

Commits happen at each phase gate, never batched. The `block-destructive.sh` hook prevents commits with `[?]` markers in staged files.
