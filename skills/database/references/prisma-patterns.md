# Prisma-Specific Scoring Adjustments

## Prisma 7 Config (Critical)

| Check | Score Impact | Details |
|-------|-------------|---------|
| Datasource URL in `prisma.config.ts` | +1 Schema Design | Prisma 7 moved datasource config out of `schema.prisma` |
| Datasource URL still in `schema.prisma` | -2 Schema Design | Deprecated pattern, breaks in Prisma 7 |
| `prisma generate` in build script | +1 DevEx | Types always fresh after schema changes |
| `prisma generate` missing from build | -1 DevEx | Types can drift from schema |

## Schema Patterns

### Good Patterns (+1 each)

```prisma
// Proper ID strategy
model User {
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  email     String   @unique
  // ...
}

// Explicit cascade rules
model Purchase {
  userId String
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  @@index([userId])
}

// Enum for fixed values
enum PurchaseStatus {
  PENDING
  COMPLETED
  REFUNDED
}
```

### Anti-Patterns (-1 each)

```prisma
// BAD: Auto-increment ID
model User {
  id Int @id @default(autoincrement())
}

// BAD: No timestamps
model Purchase {
  id     String @id
  amount Float
  // Missing createdAt, updatedAt
}

// BAD: String where enum fits
model Purchase {
  status String // Should be PurchaseStatus enum
}

// BAD: No index on foreign key
model Purchase {
  userId String
  user   User @relation(fields: [userId], references: [id])
  // Missing @@index([userId])
}
```

## Query Patterns

### Good (+1 Query Performance)

```typescript
// Select only needed fields
const user = await prisma.user.findUnique({
  where: { id: userId },
  select: { id: true, email: true, name: true }
})

// Batch include (not N+1)
const users = await prisma.user.findMany({
  include: { purchases: true },
  take: 20
})

// Transaction for multi-step
await prisma.$transaction([
  prisma.purchase.create({ data: purchaseData }),
  prisma.user.update({ where: { id: userId }, data: { role: 'BUYER' } })
])
```

### Anti-Patterns (-1 Query Performance)

```typescript
// BAD: N+1 query
const users = await prisma.user.findMany()
for (const user of users) {
  const purchases = await prisma.purchase.findMany({
    where: { userId: user.id }
  })
}

// BAD: Select everything
const user = await prisma.user.findUnique({
  where: { id: userId }
  // No select — returns all fields including passwordHash
})

// BAD: No pagination
const allPurchases = await prisma.purchase.findMany()
// Could return 100k rows
```

## Migration Patterns

### Good (+1 Migration)

```bash
# Development
prisma migrate dev --name add_purchase_status

# Production (CI/CD)
prisma migrate deploy
```

### Anti-Patterns (-1 Migration)

```bash
# BAD: Push in production
prisma db push  # Skips migration history

# BAD: Reset in production
prisma migrate reset  # Drops all data
```

## Connection Configuration

### Serverless (Vercel, Cloudflare)

```typescript
// prisma.config.ts — Prisma 7
import { defineConfig } from '@prisma/config'

export default defineConfig({
  datasource: {
    url: process.env.DATABASE_URL,          // Pooled (pgbouncer)
    directUrl: process.env.DIRECT_URL,      // Direct (migrations)
  }
})
```

| Check | Score Impact |
|-------|-------------|
| Pooled + Direct URLs configured | +1 Scalability |
| Only one URL for both queries and migrations | -1 Scalability |
| Prisma client singleton pattern | +1 Query Performance |
| New PrismaClient() per request | -1 Query Performance |
