# Quick Reference Cards

> CLI commands, error codes, connection string template, and Prisma 7 upgrade file list.
> Date: 2026-02-27

---

## Prisma CLI Commands

```bash
prisma generate          # Generate client from schema
prisma db push           # Push schema to DB (no migration file)
prisma db pull           # Introspect DB into schema
prisma db seed           # Run seed script
prisma migrate dev       # Create + apply migration (dev)
prisma migrate deploy    # Apply pending migrations (prod)
prisma migrate status    # Check migration status
prisma migrate resolve   # Resolve failed migration
prisma studio            # Open data browser
prisma validate          # Validate schema
prisma format            # Format schema file
```

## Prisma Error Code Quick Reference

| Code | Category | Brief Description |
|------|----------|-------------------|
| P1000 | Connection | Authentication failed |
| P1001 | Connection | Can't reach database |
| P1002 | Connection | Timeout |
| P1003 | Connection | Database doesn't exist |
| P1008 | Connection | Operations timed out |
| P1010 | Connection | Access denied |
| P1011 | Connection | TLS error |
| P1012 | Schema | Validation error |
| P1013 | Connection | Invalid connection string |
| P1014 | Schema | Underlying table missing |
| P1017 | Connection | Server closed connection |
| P2000 | Query | Value too long |
| P2001 | Query | Record not found (where) |
| P2002 | Query | Unique constraint violation |
| P2003 | Query | Foreign key constraint failed |
| P2011 | Query | Null constraint violation |
| P2014 | Query | Required relation violation |
| P2024 | Query | Connection pool timeout |
| P2025 | Query | Required record not found |
| P2034 | Query | Transaction write conflict |
| P3005 | Migration | Non-empty database |
| P3009 | Migration | Failed migrations blocking |
| P3014 | Migration | Shadow DB creation failed |
| P3019 | Migration | Provider mismatch |

## Connection String Template (Neon)

```
postgresql://USER:PASSWORD@ENDPOINT-pooler.REGION.aws.neon.tech/DATABASE?sslmode=require&connect_timeout=15
```

## Files Modified During Prisma 7 Upgrade

```
prisma/schema.prisma       -> Change generator, add output
prisma.config.ts           -> NEW FILE (required)
src/lib/db.ts              -> Add driver adapter, change import
src/lib/auth.ts            -> Change PrismaClient import
src/**/*.ts                -> Change all "@prisma/client" imports
package.json               -> Update dependencies, add adapter
.env                       -> Add DIRECT_URL if using migrations
```
