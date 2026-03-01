# Migration Strategies

> db push vs migrate, development workflow, CI/CD builds, production commands, destructive changes.
> Sources: Prisma docs, CViet project experience.
> Date: 2026-02-27

---

## db push vs migrate: When to Use Each

| Aspect | `db push` | `migrate dev` / `migrate deploy` |
|--------|-----------|----------------------------------|
| Purpose | Prototyping | Production migrations |
| History | No migration files | Creates migration SQL files |
| Data loss | May drop tables/columns | Warns before destructive changes |
| Rollback | Not possible | Can mark as rolled back |
| Team collaboration | Poor (no shareable history) | Good (committed migration files) |
| CI/CD | Not suitable | Use `migrate deploy` |
| Best for | Early development, schema exploration | Staging, production, teams |

## Development Workflow

```bash
# Phase 1: Prototyping (use db push)
npx prisma db push              # Quick schema sync
npx prisma generate             # Regenerate client
npx prisma studio               # View data

# Phase 2: Ready for production (switch to migrate)
npx prisma migrate dev --name init    # Create first migration
npx prisma migrate dev --name add_cv  # Subsequent changes

# Phase 3: Deploy
npx prisma migrate deploy        # Apply pending migrations (production)
```

## CI/CD Build Without Database

Many CI environments don't have database access. Prisma generate only needs the schema file, not a running database.

```json
// package.json
{
  "scripts": {
    "postinstall": "prisma generate",
    "build": "prisma generate && next build"
  }
}
```

For platforms (Vercel) that cache node_modules:
```json
{
  "scripts": {
    "build": "prisma generate && next build",
    "vercel-build": "prisma generate && next build"
  }
}
```

**Fake DATABASE_URL for CI/CD:**
```bash
# prisma generate doesn't connect to DB, but prisma.config.ts may validate the env var
DATABASE_URL="postgresql://fake:fake@localhost/fake" pnpm build
```

## Production Migration Commands

```bash
# Apply all pending migrations
npx prisma migrate deploy

# Check migration status
npx prisma migrate status

# Mark failed migration as resolved
npx prisma migrate resolve --applied "migration_name"
npx prisma migrate resolve --rolled-back "migration_name"

# Baseline existing database
npx prisma migrate diff --from-empty --to-config-datasource --script > prisma/migrations/0_init/migration.sql
npx prisma migrate resolve --applied 0_init
```

## Handling Destructive Changes

```bash
# Rename column (instead of drop + create)
npx prisma migrate dev --name rename_column --create-only
# Edit the generated SQL:
# ALTER TABLE "User" RENAME COLUMN "name" TO "fullName";
npx prisma migrate dev  # Apply the edited migration
```
