# Eval: Database Fix Patterns

Verify specific fix patterns from `references/fix-patterns/` produce correct code changes.

## Pattern 1: String-to-Enum Conversion (schema-integrity.md)

**Setup**: `Purchase.paymentMethod` is `String @default("stripe")` instead of an enum. No type safety on values.

**Steps**:
1. Apply String-to-Enum pattern.
2. Verify `enum PaymentMethod { STRIPE SEPAY }` created in schema.prisma.
3. Verify model field changed to `paymentMethod PaymentMethod @default(STRIPE)`.
4. Verify application code updated to use enum or uppercase string literals.

**Pass**: `prisma validate` passes. Application code uses `PaymentMethod.STRIPE` or `"STRIPE"`. Migration SQL contains `CREATE TYPE`. Default value matches enum member.

**Fail**: Schema invalid, or application code still uses lowercase `"stripe"`, or migration drops data.

## Pattern 2: Foreign Key Indexes (performance-scaling.md)

**Setup**: `Purchase.userId` is a foreign key with no `@@index`. Queries by userId do sequential scans.

**Steps**:
1. Apply FK Indexes pattern.
2. Verify `@@index([userId])` added to Purchase model.
3. Verify composite index `@@index([userId, status])` added for common query pattern.
4. Verify migration generated cleanly.

**Pass**: `prisma migrate dev` creates index migration without data changes. `EXPLAIN` on `WHERE userId = ?` shows index scan. Composite index covers `WHERE userId = ? AND status = ?`.

**Fail**: Indexes not added, or index on wrong columns, or migration fails.

## Pattern 3: Sensitive Field Exposure Fix (security.md)

**Setup**: API route calls `prisma.user.findUnique({ where: { id } })` without `select`, exposing password hash and tokens in response.

**Steps**:
1. Apply Sensitive Field Exposure pattern.
2. Verify all user queries have explicit `select` clause.
3. Verify password, accessToken, refreshToken never selected.
4. Verify audit: `grep` for findUnique/findFirst/findMany without select.

**Pass**: Every Prisma query touching User model uses `select`. No sensitive fields in API responses. Audit finds zero unprotected queries.

**Fail**: Some queries still return full model, or select clause incomplete.

## Pattern 4: Connection Pooling (performance-scaling.md)

**Setup**: Single `DATABASE_URL` used for both queries and migrations. No pgbouncer parameter. `DIRECT_URL` not configured.

**Steps**:
1. Apply Connection Pooling pattern.
2. Verify `prisma.config.ts` has separate `url` and `directUrl`.
3. Verify `DATABASE_URL` includes `?pgbouncer=true&sslmode=require`.
4. Verify `DIRECT_URL` includes `?sslmode=require` without pgbouncer.

**Pass**: Pooled URL used for application queries. Direct URL used for migrations. Both enforce SSL. `.env.example` documents both variables.

**Fail**: Only one URL configured, or SSL missing, or pgbouncer on direct URL.
