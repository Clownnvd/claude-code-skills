# Best Practices for Database Fixes

## Fix Discipline

### Do
- Read the file completely before editing — understand surrounding code
- Fix one issue at a time — commit each fix separately when possible
- Run `pnpm typecheck` after every schema change
- Run `prisma generate` after every schema.prisma edit
- Create migration after schema changes: `prisma migrate dev --name <desc>`
- Test seed script still works after schema changes
- Update `.env.example` when adding new env vars
- Update `src/lib/env.ts` when adding new env vars

### Don't
- Don't batch unrelated fixes into one giant edit
- Don't edit migration files after they're committed
- Don't run `prisma db push` in production (skips history)
- Don't run `prisma migrate reset` in production (drops data)
- Don't add indexes on low-cardinality columns (booleans, tiny enums)
- Don't create more than 5 indexes on write-heavy tables
- Don't add `select` to internal service calls that need all fields
- Don't wrap non-fatal side effects in transactions

## Schema Change Safety

### Safe Changes (no data loss)
| Change | Risk | Procedure |
|--------|------|-----------|
| Add nullable column | None | migrate dev |
| Add new model | None | migrate dev |
| Add new enum value | None | migrate dev |
| Add index | Brief lock on large tables | migrate dev, test on branch first |
| Add unique constraint | Fails if duplicates exist | Check data first, then migrate |

### Dangerous Changes (potential data loss)
| Change | Risk | Procedure |
|--------|------|-----------|
| Drop column | Data loss | Backup → migrate → verify |
| Drop table | Data loss | Backup → ensure no references → migrate |
| Rename column | App breaks until deploy | Two-step: add new → copy data → remove old |
| Change type | Data truncation | Test on branch with real data first |
| Make nullable → required | Fails if nulls exist | Fill defaults → then migrate |

## Migration Fix Patterns

### Schema drift recovery
```bash
# 1. See what's different
npx prisma migrate diff --from-migrations --to-schema-datamodel

# 2. Generate corrective migration
npx prisma migrate dev --name sync_drift

# 3. Verify
npx prisma migrate status
```

### Enum changes
```prisma
// Adding value: safe
enum PaymentMethod { STRIPE SEPAY PAYPAL }

// Removing value: dangerous — check no rows use it first
// Renaming value: two-step migration required
```

## Query Fix Patterns

### When to add select
- API routes returning data to client: ALWAYS
- Internal service calls: only if performance matters
- Webhook handlers: only for fields needed in logic

### When NOT to add index
- Column with < 10 distinct values (boolean, small enum)
- Table with < 1000 rows (full scan is fast)
- Column only used in INSERT, never in WHERE/ORDER BY
- Table is write-heavy (> 80% writes) and already has 5+ indexes

## Env Var Sync Checklist

When adding a new env var, update ALL of these:
1. `.env.example` — with placeholder/example value
2. `src/lib/env.ts` — Zod schema validation
3. `src/env.d.ts` — TypeScript type (if exists)
4. `vitest.config.ts` — test environment (if needed)
5. Deployment platform (Vercel/Railway env settings)

## Common Fix Mistakes

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Edit old migration file | Checksum mismatch, migrate fails | Create new migration instead |
| Add index without checking table size | Long migration lock | Check row count first |
| Change column type without data check | Data truncation | Query `SELECT DISTINCT` first |
| Add NOT NULL without default | Migration fails on existing rows | Add default OR backfill first |
| Remove field from schema but not from queries | Runtime error | Search codebase for field name |
| Add enum value in schema but not in code | Unhandled case | Search for switch/if on enum |
| Fix monitoring but forget to test log output | Logs PII in production | Review log config per environment |

## Fix Verification Order

Always verify in this order:
1. `prisma generate` — types regenerated
2. `pnpm typecheck` — catches type mismatches from schema changes
3. `pnpm test` — catches logic regressions
4. `pnpm build` — catches build-time issues
5. Manual test — critical paths (auth, payment, webhook)
