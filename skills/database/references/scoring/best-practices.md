# Best Practices for Database Design

## Schema Design

### Do
- Use `cuid()` or `uuid()` for primary keys — globally unique, non-sequential
- Add `createdAt` and `updatedAt` to every model
- Use enums for fields with fixed value sets (status, role, type)
- Add `@unique` on business identifiers (email, stripePaymentId, slug)
- Use `@@index` on all foreign keys and frequently filtered columns
- Set explicit `onDelete` cascade rules on every relation
- Keep models focused — max 15-20 fields per model

### Don't
- Don't use auto-increment Int IDs — they leak entity count and are guessable
- Don't use `String` where `Enum`, `Boolean`, `Int`, or `DateTime` fits
- Don't make fields nullable without clear business reason
- Don't skip timestamps — they're essential for debugging and auditing
- Don't store derived/computed data unless for performance (document why)

## Security

### Do
- Store connection strings in env vars, validate at startup with Zod
- Use SSL for all database connections (`?sslmode=require`)
- Create separate database users per environment with minimal privileges
- Use parameterized queries only (Prisma ORM handles this automatically)
- Exclude sensitive fields from API responses (`select` specific fields)
- Log security events (failed auth, permission denied) without PII

### Don't
- Don't hardcode credentials in any file (schema, config, code)
- Don't use `$queryRawUnsafe` with user input
- Don't return full models including `passwordHash` or `tokens`
- Don't use the same database credentials for dev and production
- Don't store credit card numbers — use Stripe/payment provider IDs only

## Performance

### Do
- Index every foreign key and every field used in `WHERE`/`ORDER BY`
- Use `select` to fetch only needed columns
- Use `include` with `take` limits — never unbounded
- Wrap multi-step writes in `$transaction`
- Use cursor-based pagination for large datasets
- Configure connection pooling (PgBouncer or Neon pooler)
- Match database region to deployment region

### Don't
- Don't run `findMany()` without `take` on user-facing endpoints
- Don't fetch relations inside loops (N+1 problem)
- Don't put external API calls inside database transactions
- Don't index low-cardinality columns (booleans, tiny enums)
- Don't create more than 5 indexes on write-heavy tables

## Migrations

### Do
- Use `prisma migrate dev` locally, `prisma migrate deploy` in CI/CD
- Make each migration a single focused change
- Commit migrations to git, never edit them after creation
- Test destructive migrations on a branch/copy of production data
- Create a seed script that's idempotent and uses realistic data

### Don't
- Don't use `prisma db push` in production (skips migration history)
- Don't edit existing migration files — create new ones
- Don't run `prisma migrate reset` in production (drops all data)
- Don't skip rollback planning for destructive schema changes

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| No index on FK | Slow JOINs, full table scans | Add `@@index([foreignKeyField])` |
| Datasource URL in schema.prisma | Prisma 7 warnings/breaks | Move to `prisma.config.ts` |
| No connection pooling | "Too many connections" errors | Add `?pgbouncer=true` to URL |
| N+1 queries | Page loads slow, many DB calls | Use `include` instead of loop queries |
| Missing env validation | App crashes with cryptic error | Zod validate all DB env vars at startup |
| Shared dev database | Migration conflicts between devs | Use Neon branches per developer |
| No PITR awareness | Data loss on bad migration | Enable Neon PITR, branch before risky changes |
| Full model in API | Password hash leaked to client | Use `select` for specific fields |

## Pre-Deploy Checklist

- [ ] All foreign keys indexed
- [ ] Connection pooling configured (pooled + direct URLs)
- [ ] SSL enabled on connection string
- [ ] Env vars validated with Zod at startup
- [ ] `.env` in `.gitignore`, `.env.example` committed
- [ ] Migrations tested on staging or branch copy
- [ ] Seed script works after `prisma migrate reset`
- [ ] No `console.log` in production query paths
- [ ] Sensitive fields excluded from API responses
- [ ] Backup/PITR verified and retention period set
