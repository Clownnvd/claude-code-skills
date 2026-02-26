---
name: agent-orchestrator
description: Build multi-agent systems where an orchestrator spawns specialist worker agents in parallel waves. Use when: complex projects need parallel execution, tasks require different skills/tools, work can be decomposed into independent subtasks.
triggers: ["orchestrator", "multi-agent", "spawn agents", "parallel agents", "agent workers", "divide tasks", "agent pipeline"]
---

# Agent Orchestrator

Orchestrator → Worker Agents pattern. Decomposes complex tasks → spawns specialist agents in parallel waves → collects results.

## Quick Start

```bash
# Run orchestrator for a project
python scripts/orchestrator.py "Build complete SaaS app with auth, UI, and API"

# With custom waves (JSON plan file)
python scripts/orchestrator.py --plan .tmp/agents/plan.json
```

## Architecture

```
User task
    ↓
[Orchestrator] — reads CLAUDE.md + project context
    ↓ plans dependency graph
Wave 1 (parallel): [db-agent] [ui-agent]       ← no deps
Wave 2 (parallel): [auth-agent]                 ← needs db-agent
Wave 3 (sequential): [api-agent] [test-agent]  ← needs all
    ↓
.tmp/agents/{name}/output.md  ← shared memory between agents
```

## How Agents Communicate

Agents are isolated processes. They share state via files only:

| File | Purpose |
|------|---------|
| `.tmp/agents/plan.json` | Orchestrator plan (waves + tasks) |
| `.tmp/agents/{name}/output.md` | Each agent's output |
| `.tmp/agents/{name}/files.json` | Files created by agent |
| `.tmp/agents/summary.md` | Final orchestrator summary |

## Spawning Agents

Each worker is a `claude --print` subprocess with a skill loaded:

```python
# Spawn with skill
spawn_agent("ui-agent", task="Build sidebar", skill="claude-ui")

# Spawn without skill
spawn_agent("cleanup-agent", task="Remove unused imports")

# Parallel wave
run_wave(["db-agent", "ui-agent"])  # Both run simultaneously

# Sequential
run_wave(["auth-agent"])  # Waits for previous wave
```

## Agent Types (Common)

| Agent | Skill | Responsibility |
|-------|-------|---------------|
| db-agent | database | Schema, migrations, seed data |
| auth-agent | auth | Login, OAuth, sessions |
| ui-agent | claude-ui / ultimateuiux | Components, pages |
| api-agent | api | Routes, middleware, validation |
| test-agent | — | Test cases, validation |
| infra-agent | infrastructure | CI/CD, Docker, env |

## Scripts

- `scripts/orchestrator.py` — Main orchestration engine
- `scripts/spawn_agent.py` — Single agent runner (used internally)

## References

- `references/patterns.md` — Execution patterns, edge cases, anti-patterns
