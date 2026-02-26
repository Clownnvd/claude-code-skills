# API Migrate Workflow

## Process

1. **Detect Versions** — Identify current and target versions of Next.js, middleware, validation libraries
2. **Map Breaking Changes** — Cross-reference version changelogs against 10 api categories:

## Next.js Migration Map

| From → To | Category Affected | Breaking Change | Migration Action |
|-----------|------------------|-----------------|-----------------|
| 14 → 15 | Response Design | `NextResponse` API changes | Update response construction |
| 15 → 16 | Performance | `dynamicIO` default | Add `"use cache"` or explicit `dynamic` |
| 15 → 16 | Security | Proxy replaces middleware for auth | Migrate auth from `middleware.ts` to `proxy.ts` |
| Any | Input Validation | Zod major version | Update schema syntax if Zod v4 |
| Any | Auth & AuthZ | Clerk v5 → v6 | Update `auth()` imports and API |
| Any | Rate Limiting | Upstash SDK changes | Update ratelimit constructor |

3. **Apply Migrations** — For each breaking change:
   - Read affected files
   - Apply migration pattern
   - Preserve existing quality (don't regress scores)
4. **Verify** — Run typecheck + tests, spot-check affected routes
5. **Re-score** — Ensure no category regressed after migration

## Safety Rules

- Never remove auth checks during migration
- Never weaken validation during migration
- Test each migrated route individually
- Keep old patterns as comments only if rollback needed
