# Fix Patterns: Migration + Monitoring + Backup + DevEx

## Migration Sync

### Problem: Schema drift — schema.prisma differs from migration history
```
# Symptom: prisma migrate dev creates unexpected migration
# Or: production DB has tables/columns not in migrations
```

### Fix: Create corrective migration
```bash
# 1. Check current drift
npx prisma migrate diff --from-migrations --to-schema-datamodel

# 2. Create migration to sync
npx prisma migrate dev --name sync_schema_with_migrations

# 3. Review generated SQL
cat prisma/migrations/<timestamp>_sync_schema_with_migrations/migration.sql

# 4. If migration drops data, create branch backup first (Neon)
```

### Old tables/enums in migration history
If migration history contains tables that no longer exist (e.g., `subscription`), this is normal — migration history is append-only. Future migrations will contain DROP statements.

## prisma generate in Build

### Problem: Types can drift from schema
```json
// package.json — no prisma generate
{
  "scripts": {
    "build": "next build"
  }
}
```

### Fix: Add to build script
```json
{
  "scripts": {
    "build": "prisma generate && next build",
    "postinstall": "prisma generate"
  }
}
```

`postinstall` ensures types regenerate after `npm install` / `pnpm install`.

## Seed Script Quality

### Problem: Unrealistic test data
```typescript
// Before
const users = [
  { email: "test@test.com", name: "Test" },
  { email: "foo@bar.com", name: "Foo" },
]
```

### Fix: Realistic, diverse seed data
```typescript
const users = [
  { email: "sarah.chen@example.com", name: "Sarah Chen" },
  { email: "marcus.johnson@example.com", name: "Marcus Johnson" },
  { email: "yuki.tanaka@example.com", name: "Yuki Tanaka" },
]
```

### Seed must be idempotent
```typescript
// Use upsert, not create
await prisma.user.upsert({
  where: { email: user.email },
  update: { name: user.name },
  create: { email: user.email, name: user.name },
})
```

## Query Logging

### Problem: No visibility into database queries
```typescript
// Before: no logging configured
const prisma = new PrismaClient()
```

### Fix: Add environment-aware logging
```typescript
const prisma = new PrismaClient({
  log:
    process.env.NODE_ENV === "development"
      ? [
          { emit: "stdout", level: "query" },
          { emit: "stdout", level: "warn" },
          { emit: "stdout", level: "error" },
        ]
      : [
          { emit: "stdout", level: "warn" },
          { emit: "stdout", level: "error" },
        ],
})
```

**Note**: With PrismaPg adapter, log config may need adjustment. Test after adding.

### Slow query detection
```typescript
// Add event listener for slow queries
prisma.$on("query", (e) => {
  if (e.duration > 1000) {
    console.warn(`Slow query (${e.duration}ms): ${e.query}`)
  }
})
```

## Backup Documentation

### Problem: No documented backup strategy
No RTO/RPO defined, no recovery testing evidence.

### Fix: Document in README or CONTRIBUTING.md
```markdown
## Backup & Recovery

### Provider: Neon PostgreSQL
- **PITR**: Enabled (Point-in-Time Recovery)
- **Retention**: Free plan 24h, Pro plan 7 days
- **RTO**: < 5 minutes (Neon branch restore)
- **RPO**: < 1 minute (continuous WAL archiving)

### Pre-Migration Backup
Before running destructive migrations:
1. Create Neon branch from production
2. Test migration on branch
3. If successful, apply to production
4. Keep branch for 7 days as rollback point

### Recovery Testing
- Last tested: [date]
- Procedure: Create branch → verify data → promote if needed
```

### Branch-before-migrate pattern
```bash
# Using Neon CLI
neon branches create --name pre-migration-backup
# Run migration on main
npx prisma migrate deploy
# If something goes wrong
neon branches restore pre-migration-backup
```

## Schema Documentation

### Problem: No comments on non-obvious fields
```prisma
model Purchase {
  amount Int  // What unit? Cents? Dollars?
}
```

### Fix: Add triple-slash doc comments
```prisma
model Purchase {
  /// Amount in smallest currency unit (cents for USD, dong for VND)
  amount Int
  /// Unique code for SePay QR matching (format: KT-{cuid})
  paymentCode String? @unique
}
```

## Local Dev Workflow

### Problem: Complex setup after git clone
No documentation on how to get database running locally.

### Fix: Add to README
```markdown
## Quick Start

1. Clone and install
   ```bash
   git clone <repo> && cd king-template && pnpm install
   ```

2. Set up environment
   ```bash
   cp .env.example .env.local
   # Fill in DATABASE_URL and DIRECT_URL from Neon dashboard
   ```

3. Run migrations and seed
   ```bash
   npx prisma migrate dev
   # Seed runs automatically via prisma.config.ts
   ```

4. Start development
   ```bash
   pnpm dev
   ```
```

## ER Diagram

### Problem: No visual schema documentation

### Fix: Add text-based ER diagram to README or schema file
```
User 1──* Session
User 1──* Account
User 1──* Purchase
Purchase *──1 User

WebhookEvent (standalone)
EmailLog (standalone)
Verification (standalone)
```

Or use `prisma-erd-generator`:
```bash
npm install -D prisma-erd-generator @mermaid-js/mermaid-cli
```
```prisma
generator erd {
  provider = "prisma-erd-generator"
  output   = "docs/erd.svg"
}
```
