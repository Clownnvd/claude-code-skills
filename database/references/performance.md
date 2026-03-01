# Performance Optimization

> Connection pooling, query optimization, pagination, batch operations, indexes, and query logging.
> Sources: Prisma docs, Neon docs, CViet project experience.
> Date: 2026-02-27

---

## Connection Pooling

**Prisma 6 (internal pool):**
```env
DATABASE_URL="postgresql://...?connection_limit=10&pool_timeout=10"
```

**Prisma 7 (driver adapter pool):**
```typescript
import pg from "pg"

const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,              // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
})

const adapter = new PrismaPg({ pool })
const prisma = new PrismaClient({ adapter })
```

**Neon serverless adapter:**
```typescript
import { PrismaNeon } from "@prisma/adapter-neon"

const adapter = new PrismaNeon({
  connectionString: process.env.DATABASE_URL!,
  // Neon handles pooling at infrastructure level
})
```

## Query Optimization

**Avoid N+1 queries:**
```typescript
// BAD: N+1 (1 query for users + N queries for CVs)
const users = await db.user.findMany()
for (const user of users) {
  const cvs = await db.cv.findMany({ where: { userId: user.id } })
}

// GOOD: Single query with include
const users = await db.user.findMany({
  include: { cvs: true },
})

// BETTER: Select only needed fields
const users = await db.user.findMany({
  select: {
    id: true,
    name: true,
    cvs: {
      select: { id: true, title: true },
    },
  },
})
```

**Use relationLoadStrategy for joins:**
```typescript
// Uses LEFT JOIN instead of separate queries
const users = await db.user.findMany({
  relationLoadStrategy: "join",  // Default is "query" (separate queries)
  include: { cvs: true },
})
```

**Pagination:**
```typescript
// Offset-based (simple, for small datasets)
const cvs = await db.cv.findMany({
  where: { userId },
  skip: page * pageSize,
  take: pageSize,
  orderBy: { updatedAt: "desc" },
})

// Cursor-based (better for large datasets)
const cvs = await db.cv.findMany({
  where: { userId },
  take: pageSize,
  cursor: lastCvId ? { id: lastCvId } : undefined,
  skip: lastCvId ? 1 : 0,
  orderBy: { updatedAt: "desc" },
})
```

**Batch operations:**
```typescript
// BAD: Loop of individual creates
for (const item of items) {
  await db.cv.create({ data: item })
}

// GOOD: Batch create
await db.cv.createMany({ data: items })

// GOOD: Batch create and return
const created = await db.cv.createManyAndReturn({ data: items })
```

**Index strategy for common queries:**
```prisma
model CV {
  id        String   @id @default(cuid())
  userId    String
  template  String
  language  String
  updatedAt DateTime @updatedAt

  // Index for "get user's CVs sorted by date"
  @@index([userId, updatedAt(sort: Desc)])

  // Index for "filter by template"
  @@index([userId, template])
}
```

## Query Logging (Development)

```typescript
const db = new PrismaClient({
  log: [
    { level: "query", emit: "event" },
    { level: "error", emit: "stdout" },
    { level: "warn", emit: "stdout" },
  ],
})

db.$on("query", (e) => {
  if (e.duration > 100) {
    console.warn(`Slow query (${e.duration}ms): ${e.query}`)
  }
})
```
