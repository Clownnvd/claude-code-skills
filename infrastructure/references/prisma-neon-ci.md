# Prisma + Neon CI Patterns

> Part of: CI/CD & Deployment Reference -- Next.js 16 + Prisma + Neon (CViet)
> Stack: Next.js 16.1.6 (App Router, Webpack mode) | Prisma 6 + Neon PostgreSQL | pnpm | TypeScript

---

## 6.1 Build vs Runtime Database Access

| Phase | Database Needed? | Which URL? | Command |
|-------|-----------------|------------|---------|
| `prisma generate` | No (reads schema only) | Fake URL works | `pnpm db:generate` |
| `next build` | No (uses generated client types) | Fake URL works | `pnpm build` |
| `prisma migrate deploy` | Yes (modifies schema) | Real production URL | Post-deploy step |
| `prisma db push` | Yes (direct push) | Real URL | Dev only, never in CI |
| Runtime (Server Components) | Yes | Real URL | Via `DATABASE_URL` env var |

## 6.2 Fake Database URL Pattern

For CI builds, use a syntactically valid but non-existent PostgreSQL URL:

```bash
DATABASE_URL="postgresql://fake:fake@localhost:5432/fake"
```

This works because:
1. `prisma generate` only reads `schema.prisma` -- it does not connect to the database
2. `next build` only needs the generated Prisma Client types -- it does not execute queries
3. The URL just needs to pass the Prisma connection string parser validation

## 6.3 Neon Connection Strings

Neon provides two connection endpoints:

```env
# Pooled connection (for application -- goes through PgBouncer)
DATABASE_URL="postgresql://user:pass@ep-xxx-yyy-123.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Direct connection (for Prisma Migrate -- bypasses pooler)
DIRECT_DATABASE_URL="postgresql://user:pass@ep-xxx-yyy-123.us-east-2.aws.neon.tech/neondb?sslmode=require"
```

**Prisma schema for Neon with pooling:**

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_DATABASE_URL")
}
```

The `directUrl` is used by `prisma migrate` and `prisma db push` (which need a direct TCP connection), while `url` is used by the Prisma Client at runtime (which can use connection pooling).

**Note:** If you are NOT using Neon's connection pooler, both URLs can be the same.

## 6.4 Neon Database Branching

Neon branches are copy-on-write snapshots of your database:

```
main (Neon branch) ─────────────────────── production
    ├── preview/42 (branch) ─────────────── PR #42 preview
    ├── preview/43 (branch) ─────────────── PR #43 preview
    └── staging (branch) ────────────────── staging env
```

**Benefits:**
- Instant creation (~1 second, not a full copy)
- Contains production data for realistic testing
- Automatic cleanup when PR is merged/closed
- Each branch has its own connection string

## 6.5 Migration Workflow

```
Developer machine:
  prisma migrate dev          # Create migration files

CI/CD pipeline:
  prisma generate             # Generate client (no DB needed)
  next build                  # Build app (no DB needed)
  prisma migrate deploy       # Apply pending migrations (needs real DB)

Production:
  Application starts with real DATABASE_URL
```

**IMPORTANT:** Never use `prisma migrate dev` in CI/CD or production. It is interactive and will reset data if it detects drift. Always use `prisma migrate deploy`.

## 6.6 CViet Current Setup (db push, no migrations)

CViet currently uses `prisma db push` (schema-first, no migration files). To adopt migrations:

```bash
# One-time: baseline existing database
pnpm prisma migrate diff \
  --from-empty \
  --to-schema-datamodel prisma/schema.prisma \
  --script > prisma/migrations/0_init/migration.sql

# Mark baseline as applied
pnpm prisma migrate resolve --applied 0_init

# Future changes: create migration
pnpm prisma migrate dev --name add_new_field
```

---

> **Sources:**
> - [Prisma Migrate Deploy](https://www.prisma.io/docs/orm/prisma-client/deployment/deploy-database-changes-with-prisma-migrate)
> - [Prisma + Neon Migrations Guide](https://neon.com/docs/guides/prisma-migrations)
> - [Neon Database Branching with GitHub Actions](https://neon.com/docs/guides/branching-github-actions)
