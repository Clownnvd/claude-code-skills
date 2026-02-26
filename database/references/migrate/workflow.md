# Database Migrate Workflow

## Process

1. **Detect Versions** — Identify Prisma version, PostgreSQL version, hosting provider
2. **Map Breaking Changes**:

| From → To | Category Affected | Breaking Change | Migration Action |
|-----------|------------------|-----------------|-----------------|
| Prisma 5 → 6 | Schema Design | New relation mode defaults | Review relation config |
| Prisma 6 → 7 | Migration | `prisma.config.ts` required | Create config file |
| Prisma 6 → 7 | Query Performance | New query engine | Test query performance |
| Neon v1 → v2 | Scalability | Pooling config changes | Update connection string |
| PG 15 → 16 | Security | New auth methods | Update connection config |
| Any | Migration | Schema drift | Run `prisma migrate diff` |

3. **Apply Migrations** — Preserve data integrity, use transaction-safe migrations
4. **Verify** — Run `prisma validate`, test queries, check migration status
5. **Re-score** — Ensure no database quality regression

## Safety Rules

- ALWAYS backup before schema migration
- Use `prisma migrate dev` in development, `prisma migrate deploy` in production
- Never drop columns without data migration plan
- Test all queries after Prisma major version upgrade
