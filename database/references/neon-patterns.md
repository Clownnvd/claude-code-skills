# Neon PostgreSQL — Specific Scoring Adjustments

## Connection Setup (Critical)

| Check | Score Impact | Details |
|-------|-------------|---------|
| Pooled endpoint for queries | +1 Scalability | `postgresql://...@ep-xxx.ap-southeast-1.aws.neon.tech/db?sslmode=require&pgbouncer=true` |
| Direct endpoint for migrations | +1 Migration | `postgresql://...@ep-xxx.ap-southeast-1.aws.neon.tech/db?sslmode=require` |
| Missing `?sslmode=require` | -1 Security | Neon requires SSL |
| Missing `?pgbouncer=true` on pooled URL | -1 Scalability | Not using connection pooler |

## Neon Branching

### Good Patterns (+1 each)

| Pattern | Category | Description |
|---------|----------|-------------|
| Preview branches | Migration | Create Neon branch per PR for isolated testing |
| Dev branch per developer | DevEx | Each dev gets own branch, not shared dev DB |
| Branch from production | Backup | Test migrations on real data copy before deploy |
| Auto-delete stale branches | Operations | Clean up branches older than 7 days |

### Anti-Patterns (-1 each)

| Pattern | Category | Description |
|---------|----------|-------------|
| All devs share one branch | DevEx | Migration conflicts, data collisions |
| Migrations tested only on empty DB | Migration | Misses real data edge cases |
| Never clean up branches | Operations | Cost grows unbounded |

## Neon Auto-Suspend

| Check | Score Impact | Details |
|-------|-------------|---------|
| Auto-suspend configured (5-10 min) | +1 Scalability | Saves cost, no issue for most apps |
| Cold start handling in app | +1 Query Performance | First query after suspend may be slower (~500ms) |
| Auto-suspend disabled without reason | -1 Scalability | Paying for idle compute |

## Neon-Specific Backup

| Check | Score Impact | Details |
|-------|-------------|---------|
| PITR enabled (Point-in-Time Recovery) | +1 Backup | Neon supports PITR on all plans |
| PITR retention period configured | +1 Backup | Free: 24h, Pro: 7 days, configurable |
| Branch-based backup before risky migration | +1 Backup | Create branch snapshot pre-migration |
| No awareness of Neon PITR | -1 Backup | Missing free backup feature |

## Neon + Prisma Integration

### Recommended Setup (Prisma 7)

```typescript
// prisma.config.ts
import { defineConfig } from '@prisma/config'

export default defineConfig({
  datasource: {
    // Pooled for all queries (pgbouncer)
    url: process.env.DATABASE_URL,
    // Direct for migrations (no pgbouncer)
    directUrl: process.env.DIRECT_URL,
  }
})
```

```env
# .env.example
DATABASE_URL="postgresql://user:pass@ep-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&pgbouncer=true"
DIRECT_URL="postgresql://user:pass@ep-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
```

### @neondatabase/serverless (Edge Runtime)

| Check | Score Impact | Details |
|-------|-------------|---------|
| Using `@neondatabase/serverless` adapter | +1 Scalability | Required for Vercel Edge Functions |
| WebSocket driver configured | +1 Query Performance | Faster than HTTP for multiple queries |
| Using standard `pg` driver on edge | -1 Scalability | Won't work on edge runtime |

```typescript
// Only needed if deploying to Edge Runtime
import { neon } from '@neondatabase/serverless'
import { PrismaNeon } from '@prisma/adapter-neon'
import { PrismaClient } from '@prisma/client'

const sql = neon(process.env.DATABASE_URL)
const adapter = new PrismaNeon(sql)
const prisma = new PrismaClient({ adapter })
```

## Region Selection

| Check | Score Impact | Details |
|-------|-------------|---------|
| DB region matches deployment region | +1 Query Performance | e.g., both in ap-southeast-1 |
| DB in different region than app | -1 Query Performance | +50-200ms latency per query |

## Neon Monitoring

| Metric | Where | Score Impact |
|--------|-------|-------------|
| Active connections | Neon Dashboard | +1 Monitoring if tracked |
| Compute hours | Neon Dashboard | +1 Monitoring if alerts set |
| Branch storage | Neon Dashboard | +1 if regularly reviewed |
| Query performance | `pg_stat_statements` | +1 if slow queries identified |
