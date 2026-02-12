# Security Fix — Overview

## Purpose
Systematically fix all issues found by security-scoring. Follows severity * weight priority.

## Priority Matrix

| Severity × Weight | Priority | Timeline |
|-------------------|----------|----------|
| CRITICAL × any | P0 | Fix now, blocks deploy |
| HIGH × >=12% | P1 | Fix now, max score impact |
| HIGH × <12% | P2 | Fix today |
| MEDIUM × any | P3 | Fix this sprint |
| LOW × any | P4 | Backlog |

## Score Targets

| Context | Target | Action if Below |
|---------|--------|-----------------|
| Enterprise | A (93+) | Fix all CRITICAL+HIGH+MEDIUM |
| Production | B+ (87+) | Fix all CRITICAL+HIGH |
| MVP/Demo | C+ (77+) | Fix all CRITICAL |

## Safe vs Dangerous Changes

### Safe (apply freely)
- Adding Zod validation to route that lacks it
- Adding `NO_CACHE_HEADERS` to auth responses
- Adding `.strict()` to Zod schemas
- Adding env vars to `.env.example`
- Updating `poweredByHeader: false`
- Adding CSP directives to proxy

### Dangerous (verify after)
- Changing error response format (breaks client expectations)
- Modifying CSP (can break page rendering)
- Updating dependencies (can break build)
- Changing webhook verification logic (can break payment flow)
- Modifying redirect validation (can break auth flow)

## Loop Mode

When score < target:
1. Run security-scoring → get scorecard
2. Parse issues sorted by priority
3. Fix top priority issues
4. `pnpm typecheck && pnpm test`
5. Re-run security-scoring
6. Repeat until target reached
