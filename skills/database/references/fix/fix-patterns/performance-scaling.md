# Fix Patterns: Indexing + Query Performance + Scalability

## Missing Indexes

### Foreign key indexes
```prisma
// Before: no index on FK
model Purchase {
  userId String
  user   User @relation(fields: [userId], references: [id], onDelete: Cascade)
}

// After: add @@index
model Purchase {
  userId String
  user   User @relation(fields: [userId], references: [id], onDelete: Cascade)
  @@index([userId])
}
```

### Composite indexes for common query patterns
```prisma
// If frequently querying: WHERE userId = ? AND status = ?
model Purchase {
  userId String
  status PurchaseStatus
  // Single-column indexes (already exist)
  @@index([userId])
  @@index([status])
  // Add composite for the common pair
  @@index([userId, status])
}
```

### Index audit — check every WHERE/ORDER BY
```
# Find all prisma where clauses
grep -r "where:" src/ --include="*.ts" -A 3
```
Every field used in `where` should have an index.

## N+1 Query Fix

### Problem: Queries inside loops
```typescript
// Before: N+1 — 1 query for users + N queries for purchases
const users = await prisma.user.findMany()
for (const user of users) {
  const purchases = await prisma.purchase.findMany({
    where: { userId: user.id }
  })
}
```

### Fix: Use include or select with relation
```typescript
// After: 1 query with included relation
const users = await prisma.user.findMany({
  include: {
    purchases: {
      select: { id: true, status: true, amount: true }
    }
  },
  take: 20
})
```

## Unbounded Queries

### Problem: findMany without limit
```typescript
// Before: could return 100k rows
const allPurchases = await prisma.purchase.findMany()
```

### Fix: Always add take (or cursor pagination)
```typescript
// Offset pagination (simple)
const purchases = await prisma.purchase.findMany({
  take: 20,
  skip: page * 20,
  orderBy: { createdAt: "desc" }
})

// Cursor pagination (efficient for large datasets)
const purchases = await prisma.purchase.findMany({
  take: 20,
  cursor: lastId ? { id: lastId } : undefined,
  orderBy: { createdAt: "desc" }
})
```

## Select Optimization

### Problem: Fetching all fields
```typescript
// Before: returns passwordHash, tokens, etc.
const user = await prisma.user.findUnique({
  where: { id: userId }
})
```

### Fix: Select only needed fields
```typescript
const user = await prisma.user.findUnique({
  where: { id: userId },
  select: {
    id: true,
    email: true,
    name: true,
    image: true,
  }
})
```

## Transaction for Multi-Step Writes

### Problem: Multiple writes without transaction
```typescript
// Before: if second write fails, first is orphaned
await prisma.purchase.create({ data: purchaseData })
await prisma.user.update({ where: { id: userId }, data: { role: "BUYER" } })
```

### Fix: Wrap in $transaction
```typescript
await prisma.$transaction([
  prisma.purchase.create({ data: purchaseData }),
  prisma.user.update({ where: { id: userId }, data: { role: "BUYER" } }),
])
```

**Exception**: Non-fatal side effects (GitHub invite) should NOT be in the transaction.

## Connection Pooling

### Problem: Single URL for everything
```typescript
// prisma.config.ts
export default defineConfig({
  datasource: {
    url: process.env.DATABASE_URL, // same URL for queries + migrations
  }
})
```

### Fix: Separate pooled + direct URLs
```typescript
export default defineConfig({
  datasource: {
    url: process.env.DATABASE_URL,      // pooled (pgbouncer)
    directUrl: process.env.DIRECT_URL,  // direct (migrations)
  }
})
```

```env
DATABASE_URL=postgresql://...?sslmode=require&pgbouncer=true
DIRECT_URL=postgresql://...?sslmode=require
```

## Prisma Client Singleton

### Problem: New PrismaClient per request
```typescript
// Before: connection leak in development
export function getDb() {
  return new PrismaClient()
}
```

### Fix: Global singleton pattern
```typescript
import { PrismaClient } from "@prisma/client"

const globalForPrisma = global as unknown as { prisma: PrismaClient }

const prisma = globalForPrisma.prisma || new PrismaClient()

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma

export default prisma
```

## Edge Runtime Compatibility

### Problem: Standard pg driver on Vercel Edge
```typescript
// Won't work on edge runtime
import { PrismaClient } from "@prisma/client"
const prisma = new PrismaClient()
```

### Fix: Use @neondatabase/serverless adapter
```typescript
import { neon } from "@neondatabase/serverless"
import { PrismaNeon } from "@prisma/adapter-neon"
import { PrismaClient } from "@prisma/client"

const sql = neon(process.env.DATABASE_URL!)
const adapter = new PrismaNeon(sql)
const prisma = new PrismaClient({ adapter })
```

Only needed if deploying to Vercel Edge Functions. Standard Node.js runtime works with PrismaPg.
