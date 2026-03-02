# Agent Orchestra

A lightweight multi-agent system using Claude Code's native subagent spawning. No frameworks, no daemons — just Claude Code doing what it already knows how to do, with custom agents and commands to guide it.

## What This Is

When you open this project in Claude Code, it gets:

- **3 custom subagents** (researcher, coder, reviewer) that it can spawn on demand
- **5 slash commands** (`/plan`, `/research`, `/build`, `/review`, `/status`) that orchestrate multi-agent workflows
- **A CLAUDE.md** that teaches it to think like an orchestrator — decompose goals, parallelize work, and always review before finishing

You talk to Claude Code. Claude Code spawns subagents to do the work. Each subagent runs in its own context window and reports back. You stay in control with Claude Code's normal approval flow.

## Quick Start

```bash
# Clone the repo
git clone <your-repo-url> agent-orchestra
cd agent-orchestra

# Open in Claude Code (terminal or VS Code)
claude

# Try a command
> /plan Build a Python CLI tool that monitors disk usage and sends alerts
```

That's it. No dependencies. No setup. Claude Code reads the `.claude/` directory automatically.

## Commands

| Command | What it does |
|---------|-------------|
| `/plan <goal>` | Spawns researchers in parallel to investigate, then creates an actionable plan |
| `/research <topic>` | Deep-dives a topic with multiple researcher subagents in parallel |
| `/build <task>` | Full pipeline: research → implement → review |
| `/review [files]` | Spawns parallel reviewers for correctness + quality |
| `/status` | Shows git state, recent work, and outputs |

## Subagents

| Agent | Model | Tools | Role |
|-------|-------|-------|------|
| `researcher` | Sonnet | Read-only + web search | Gathers info, explores code, compares options |
| `coder` | Sonnet | Full file + bash access | Writes code, scripts, automation |
| `reviewer` | Sonnet | Read + bash (for tests) | Finds bugs, runs tests, quality checks |

Claude Code (the orchestrator) runs on whatever model you've selected — Opus for complex planning, Sonnet for routine work.

## How It Works

```
You: "/build a REST API for task management"
 │
 └→ Claude Code (orchestrator)
      ├→ spawns researcher → explores codebase, checks conventions
      │   └→ returns: "project uses FastAPI, pytest, follows X pattern"
      │
      ├→ spawns coder → builds the API following conventions
      │   └→ returns: "created api.py, models.py, ran successfully"
      │
      ├→ spawns coder → writes tests in parallel
      │   └→ returns: "created test_api.py, 12 tests passing"
      │
      └→ spawns reviewer → checks everything
          └→ returns: "PASS — 2 suggestions for improvement"
```

All subagents run in their own context windows. The orchestrator keeps a clean high-level view.

## Multi-PC Usage

This is a git repo. From any machine with Claude Code:

```bash
git pull    # Get latest outputs and plans
claude      # Open Claude Code, it reads .claude/ automatically
# Do work...
git add -A && git commit -m "completed research on X" && git push
```

## Using Cline for Grunt Work

Not everything needs Claude. For repetitive or low-reasoning tasks:

1. Claude Code will sometimes flag tasks as "Cline-suitable"
2. Switch to Cline in VS Code, point it at the task
3. Cline uses your local Qwen 30B — free, fast, and good enough for boilerplate

The `.clinerules` file gives Cline its instructions.

## Project Structure

```
agent-orchestra/
├── CLAUDE.md                    ← Orchestrator personality + instructions
├── .clinerules                  ← Cline worker instructions
├── .claude/
│   ├── agents/
│   │   ├── researcher.md        ← Research subagent definition
│   │   ├── coder.md             ← Coding subagent definition
│   │   └── reviewer.md          ← Review subagent definition
│   └── commands/
│       ├── plan.md              ← /plan command
│       ├── research.md          ← /research command
│       ├── build.md             ← /build command
│       ├── review.md            ← /review command
│       └── status.md            ← /status command
├── outputs/                     ← All deliverables land here
├── docs/                        ← Project documentation
└── README.md
```

## Tips

- **Start with `/plan`** for any non-trivial goal. It forces research before action.
- **Use `/research` liberally.** It's cheap (subagents use Sonnet) and prevents wrong turns.
- **Parallel is the point.** When you see Claude spawn 3 subagents at once, that's the magic — all running simultaneously.
- **You approve everything.** Claude Code's approval flow means you see every file write and bash command. Turn on `--dangerously-skip-permissions` only when you trust the workflow.
