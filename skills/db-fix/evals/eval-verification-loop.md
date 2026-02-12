# Eval: Database Fix Verification Loop

Verify the compile-test-rescore cycle, regression detection, and fix idempotency for db-fix.

## Test 1: Compile + Test Verification

**Setup**: Scorecard with HIGH issue: missing indexes on foreign key columns (Indexing 3/10). Apply the FK Index fix from `performance-scaling.md` which adds `@@index` directives to the Prisma schema.

**Steps**:
1. Add `@@index([userId])`, `@@index([teamId])` to relevant models in `prisma/schema.prisma`.
2. Run `npx prisma validate` to confirm schema syntax.
3. Run `npx prisma generate` to regenerate the client.
4. Run `npx tsc --noEmit`. Verify zero type errors after client regeneration.
5. Run `pnpm test`. Verify all existing DB query tests still pass.

**Pass**: `prisma validate` exits 0. `tsc --noEmit` exits 0 after `prisma generate`. All tests pass. Migration preview (`prisma migrate dev --create-only`) shows only `CREATE INDEX` statements, no table drops.

**Fail**: Schema validation error, type mismatch from regenerated client, or migration preview includes destructive operations (DROP COLUMN, DROP TABLE).

## Test 2: Re-Score Improvement Verification

**Setup**: Initial db-scoring scorecard: Indexing 3/10, Schema Design 5/10, Security 4/10. Total 48/100 (D+). Apply fixes for FK indexes (Indexing) and `@@unique` constraints on email fields (Schema Design).

**Steps**:
1. Run db-fix for both issues.
2. Invoke `db-scoring` to produce a new scorecard.
3. Compare per-category scores: Indexing, Schema Design must increase.
4. Verify Security, Operations, Query Performance, and all other categories remain at or above pre-fix scores.

**Pass**: Indexing >= 6/10 (was 3). Schema Design >= 7/10 (was 5). No category dropped below its pre-fix score. Total weighted score increased. EXPLAIN on key queries shows index usage.

**Fail**: Any unfixed category score decreased, or EXPLAIN still shows sequential scans on indexed columns.

## Test 3: Regression Detection

**Setup**: Initial scorecard: Schema Design 8/10, Indexing 7/10, Migration & Versioning 7/10. Apply a schema fix that renames a column without a migration rename step, causing `prisma migrate dev` to generate DROP + ADD instead of ALTER RENAME. Migration & Versioning drops from 7/10 to 3/10.

**Steps**:
1. Apply schema fix that renames `userName` to `displayName` without using `@map`.
2. Run `db-scoring` re-score.
3. Verify pipeline detects Migration & Versioning dropped from 7 to 3 (delta -4).
4. Verify pipeline halts and recommends using `@map("userName")` to preserve data.

**Pass**: Pipeline detects the Migration & Versioning regression. Output flags: destructive migration detected, before/after delta shown, recommendation to use `@map` for safe column rename. Pipeline does not continue.

**Fail**: Pipeline ignores the destructive migration and continues, or fails to detect the DROP + ADD pattern in migration SQL.

## Test 4: Fix Idempotency

**Setup**: Scorecard with HIGH issue: missing FK indexes. The `prisma/schema.prisma` already has `@@index([userId])` on all models from a previous fix run.

**Steps**:
1. Run db-fix with the same indexing issue.
2. Check `git diff` after the fix attempt.
3. Run `npx prisma migrate dev --create-only` and verify no new migration is generated.

**Pass**: No files modified (`git diff` is empty). No new migration created ("Already in sync"). Skill reports "already applied" or "no changes needed." No duplicate `@@index` directives.

**Fail**: Duplicate `@@index([userId])` lines added, empty migration file created, or schema validation fails from duplicate directives.
