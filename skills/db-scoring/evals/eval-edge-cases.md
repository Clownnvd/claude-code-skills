# Database Scoring — Edge Cases Eval

Verify correct behavior for database-specific edge cases.

## Test 1: No schema.prisma Found

- Run against a codebase with no Prisma schema
- Verify scoring does not crash
- Verify output notes missing schema and scores Schema Design at 0
- Verify categories not dependent on schema (Monitoring, Backup) can still score

## Test 2: Missing Indexes on Foreign Keys

- Provide schema with relations but no `@@index` on foreign key columns
- Verify Indexing Strategy scores <= 4
- Verify issue lists specific foreign key fields needing indexes
- Verify Query Performance also penalized for full-table scan risk

## Test 3: No Connection Pooling Configured

- Provide database config without connection pooling (no PgBouncer, no Neon pooler)
- Verify Scalability scores <= 3
- Verify Security also checked for direct DB exposure
- Verify fix recommends pooler URL for production

## Test 4: Prisma 7 Without prisma.config.ts

- Provide Prisma 7+ project missing `prisma.config.ts`
- Verify CRITICAL issue flagged per `prisma-patterns.md`
- Verify Migration & Versioning penalized
- Verify Developer Experience also penalized

## Test 5: Raw SQL Queries Without Parameterization

- Provide code using string interpolation in raw SQL queries
- Verify Security scores <= 1 (CRITICAL)
- Verify issue identifies SQL injection vulnerability
- Verify fix recommends `$queryRaw` with template literals

## Test 6: No Migration History

- Provide project with schema but no migration files
- Verify Migration & Versioning scores <= 2
- Verify issue flags risk of schema drift
- Verify fix recommends `prisma migrate dev` workflow

## Test 7: Neon-Specific Edge Cases

- Provide Neon PostgreSQL config without branching or PITR enabled
- Verify Backup & Recovery penalized if no PITR
- Verify Neon-specific adjustments from `neon-patterns.md` apply
- Verify region selection and edge runtime compatibility checked
