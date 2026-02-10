# Infrastructure Fix — Best Practices

## Fix Discipline

| Do | Don't |
|----|-------|
| Fix one category at a time | Scatter changes across all categories |
| Verify after each fix | Batch all fixes then check |
| Keep existing tests passing | Break tests to add infra |
| Use platform-native features | Over-engineer custom solutions |
| Document what's automated vs manual | Leave undocumented gaps |

## CI/CD Fixes

| Do | Don't |
|----|-------|
| Test workflow on feature branch first | Push directly to main |
| Use official GitHub Actions | Use random third-party actions |
| Pin action versions (`@v4`) | Use `@latest` or `@main` |
| Cache dependency store (pnpm store) | Cache node_modules directly |
| Set reasonable timeouts (10-15 min) | No timeout or 60+ min timeout |

## Docker Fixes

| Do | Don't |
|----|-------|
| Use Alpine or distroless base | Use full Ubuntu/Debian |
| Copy package.json before source | Copy everything at once |
| Use `.dockerignore` | Rely on build context exclusion |
| Pin exact base image version | Use `node:latest` |
| Run as non-root USER | Skip USER directive |

## Environment Fixes

| Do | Don't |
|----|-------|
| Validate with Zod at startup | Access raw process.env |
| Keep .env.example in sync | Let it drift from actual vars |
| Use platform secret store | Store secrets in .env on server |
| Fail loud on missing vars | Silently use undefined |

## Monitoring Fixes

| Do | Don't |
|----|-------|
| Return JSON from health endpoints | Return plain text "OK" |
| Check DB in readiness probe | Only check app process |
| Use structured JSON logging | Use console.log strings |
| Log request metadata (method, path, status, ms) | Log only errors |

## Integration Fixes

| Do | Don't |
|----|-------|
| Add timeout to every external call | Leave unbounded fetches |
| Verify webhook signatures first | Process before verifying |
| Log integration failures with context | Silent catch blocks |
| Handle degraded mode gracefully | Hard crash on API down |

## Common Mistakes

1. **CI pipeline too slow** — Parallel jobs, not sequential steps
2. **Docker image too large** — Multi-stage build, Alpine base
3. **Health endpoint lies** — Must check actual dependencies
4. **Monitoring without alerting** — Logs nobody reads are useless
5. **Backup without restore testing** — Untested backups may be corrupted
6. **Secrets in CI logs** — Mask sensitive env vars in output
