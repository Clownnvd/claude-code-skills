# Orchestration Patterns

## Wave Execution (Core Pattern)

```
Wave 1: [A] [B] [C]   ← parallel, no deps
Wave 2: [D]           ← sequential, needs A+B
Wave 3: [E] [F]       ← parallel, both need D
```

Rule: If X depends on Y, X must be in a later wave than Y.

## Shared Memory via Files

Agents communicate ONLY through files — never direct calls:

```
.tmp/agents/
  db-agent/output.md       ← "Created schema: users, posts, sessions"
  auth-agent/output.md     ← reads db-agent output, builds on top
  summary.md               ← orchestrator final report
```

Agent reads context: set `"reads": ["db-agent"]` in plan — orchestrator injects content.

## Common Agent Sets

### Full-Stack SaaS
```json
{
  "waves": [
    ["db-agent"],
    ["auth-agent", "ui-agent"],
    ["api-agent"],
    ["test-agent"]
  ]
}
```

### UI Clone (WAT)
```json
{
  "waves": [
    ["capture-agent"],
    ["analyze-agent"],
    ["build-shared-agent"],
    ["build-screens-agent"],
    ["diff-agent"]
  ]
}
```

### Code Audit
```json
{
  "waves": [
    ["security-agent", "api-agent", "auth-agent"],
    ["fix-agent"],
    ["test-agent"]
  ]
}
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Agent calls another agent directly | Creates coupling, hard to debug | Use files for communication |
| All agents in one wave | Sequential deps cause incorrect results | Map dependencies first |
| Orchestrator writes code | Orchestrator should plan+validate only | Delegate all code to workers |
| Agent does 3+ things | Hard to debug, output too large | One responsibility per agent |
| No reads config | Agent reinvents wheel | Always declare `"reads"` deps |

## Handling Failures

- Orchestrator logs each agent status (done/error)
- Failed agents don't block independent waves
- `summary.md` lists which agents failed
- Re-run specific wave: use `--plan .tmp/agents/plan.json` and skip completed waves

## Scaling

- 4 workers default (ThreadPoolExecutor max_workers=4)
- Increase for IO-bound tasks (more parallel agents)
- Decrease for CPU-bound tasks or API rate limits
- Each `claude --print` call uses 1 API key — watch rate limits

## Tips

- Keep agent tasks focused: "Build sidebar component" NOT "Build entire frontend"
- Name agents descriptively: "prisma-schema-agent" not "agent1"
- Orchestrator reads CLAUDE.md automatically — agents inherit project context
- Use `--plan` flag to re-run without re-planning
