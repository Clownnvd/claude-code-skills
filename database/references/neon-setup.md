# Neon PostgreSQL Setup

> Sources: Neon docs, Prisma docs, CViet project experience.
> Date: 2026-02-27

---

## Connection String Formats

Neon provides two connection types via the Console Connect button:

**Pooled connection** (for application code):
```
postgresql://[user]:[password]@[endpoint]-pooler.[region].aws.neon.tech/[dbname]?sslmode=require
```
- Contains `-pooler` in hostname
- Routes through PgBouncer (up to 10,000 concurrent connections)
- Transaction mode (pool_mode=transaction)
- Optimal for serverless functions

**Direct connection** (for CLI/migrations):
```
postgresql://[user]:[password]@[endpoint].[region].aws.neon.tech/[dbname]?sslmode=require
```
- No `-pooler` in hostname
- Direct TCP to PostgreSQL
- Required for `prisma migrate` and `prisma db push`

## Environment Variables

```env
# .env
DATABASE_URL="postgresql://user:pass@ep-xxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
DIRECT_URL="postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"
```

## Prisma 6 Configuration (Current CViet Setup)

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")    // Prisma 4.10.0+ feature
}
```

## Prisma 7 Configuration (Neon)

**prisma.config.ts:**
```typescript
import "dotenv/config"
import { defineConfig, env } from "prisma/config"

export default defineConfig({
  schema: "prisma/schema.prisma",
  datasource: {
    url: env("DIRECT_URL"),  // CLI uses direct connection
  },
})
```

**src/lib/db.ts:**
```typescript
import { PrismaClient } from "../generated/prisma"
import { PrismaNeon } from "@prisma/adapter-neon"

// Application uses pooled connection
const adapter = new PrismaNeon({
  connectionString: process.env.DATABASE_URL!,  // Pooled
})

export const db = new PrismaClient({ adapter })
```

## Connection String Parameters

| Parameter | Purpose | Default | Example |
|-----------|---------|---------|---------|
| `sslmode=require` | Enforce SSL (mandatory for Neon) | -- | Always add |
| `connect_timeout` | Initial connection timeout (seconds) | 0 | `15` |
| `connection_limit` | Prisma internal pool size | `num_cpus * 2 + 1` | `20` |
| `pool_timeout` | Wait for pool connection (seconds) | 10 | `15` |
| `pgbouncer=true` | Enable PgBouncer mode | false | Not needed for Neon PgBouncer 1.21.0+ |

## Cold Start Optimization

Neon scales computes to zero after ~5 minutes of inactivity. Cold start latency:

| Scenario | Latency |
|----------|---------|
| Historical (2024) | ~3 seconds |
| Current (2025-2026) | Sub-200ms |
| Warm subsequent queries | Sub-100ms |

**Strategies to minimize cold start impact:**

1. **Use pooled connections** -- PgBouncer maintains warm connections
2. **Increase connect_timeout** -- `?connect_timeout=15` prevents P1001 errors
3. **Keep-alive queries** -- Periodic lightweight query to prevent scale-to-zero
4. **Neon Pro plan** -- Configurable auto-suspend timeout (or never suspend)

## PgBouncer Configuration

Neon uses PgBouncer in transaction mode. Key considerations:

- Named prepared statements: Supported in PgBouncer 1.21.0+ (Neon default)
- Schema migrations via pooled connections: Supported (recent Neon improvement)
- `?pgbouncer=true` flag: No longer required for Neon (but harmless if included)
- `DISCARD ALL` / `DEALLOCATE ALL`: Supported by Neon's PgBouncer

**For older PgBouncer versions:**
```
postgresql://...?pgbouncer=true&sslmode=require
```
