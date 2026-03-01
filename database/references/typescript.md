# TypeScript Patterns

> Prisma + TypeScript patterns for Json fields, relations, transactions, error handling, and client extensions.
> Sources: Prisma docs, CViet project experience.
> Date: 2026-02-27

---

## Json Field Typing

**Pattern 1: Double-cast (simple, no dependencies)**
```typescript
type CVData = {
  personal: { name: string; email: string; phone: string; location: string;
              linkedin?: string; website?: string; summary: string }
  experience: Array<{ company: string; role: string; startDate: string;
                      endDate?: string; current: boolean; bullets: string[] }>
  education: Array<{ school: string; degree: string; field: string;
                     startDate: string; endDate: string; gpa?: string }>
  skills: Array<{ category: string; items: string[] }>
  languages: Array<{ name: string; level: string }>
  certifications: Array<{ name: string; issuer: string; date: string; url?: string }>
}

// Reading
const cv = await db.cv.findUnique({ where: { id } })
const data = cv?.data as unknown as CVData

// Writing
await db.cv.update({
  where: { id },
  data: { data: newCvData as unknown as Prisma.InputJsonValue },
})
```

**Pattern 2: prisma-json-types-generator (compile-time safety)**
```bash
pnpm add -D prisma-json-types-generator
```
```prisma
generator client {
  provider = "prisma-client"
  output   = "../src/generated/prisma"
}

generator json {
  provider = "prisma-json-types-generator"
}

model CV {
  id   String @id @default(cuid())
  /// [CVData]
  data Json
}
```
```typescript
// src/types/prisma-json.d.ts
declare global {
  namespace PrismaJson {
    type CVData = import("@/types/cv").CVData
  }
}
export {}
```

**Pattern 3: Zod runtime validation**
```typescript
import { z } from "zod"

const cvDataSchema = z.object({
  personal: z.object({
    name: z.string(),
    email: z.string().email(),
    phone: z.string(),
    location: z.string(),
    linkedin: z.string().optional(),
    website: z.string().url().optional(),
    summary: z.string(),
  }),
  experience: z.array(z.object({
    company: z.string(),
    role: z.string(),
    startDate: z.string(),
    endDate: z.string().optional(),
    current: z.boolean(),
    bullets: z.array(z.string()),
  })),
  // ... etc
})

type CVData = z.infer<typeof cvDataSchema>

// Validate on read
const cv = await db.cv.findUnique({ where: { id } })
const parsed = cvDataSchema.safeParse(cv?.data)
if (!parsed.success) throw new Error("Invalid CV data")
const data: CVData = parsed.data

// Validate on write
const validated = cvDataSchema.parse(incomingData)
await db.cv.update({ where: { id }, data: { data: validated } })
```

## Relation Queries

```typescript
// Include related data
const user = await db.user.findUnique({
  where: { id: userId },
  include: {
    cvs: true,
    sessions: true,
    accounts: true,
  },
})

// Select specific fields (more efficient)
const user = await db.user.findUnique({
  where: { id: userId },
  select: {
    id: true,
    name: true,
    email: true,
    plan: true,
    cvs: {
      select: { id: true, title: true, template: true, updatedAt: true },
      orderBy: { updatedAt: "desc" },
    },
  },
})

// Nested filtering
const users = await db.user.findMany({
  where: {
    cvs: {
      some: { template: "modern" },
    },
  },
  include: { cvs: true },
})

// Count relations
const usersWithCvCount = await db.user.findMany({
  include: {
    _count: { select: { cvs: true } },
  },
})
// Access: user._count.cvs
```

## Transactions

```typescript
// Batch transaction (all-or-nothing)
const [user, cv] = await db.$transaction([
  db.user.update({ where: { id: userId }, data: { aiUsageThisMonth: { increment: 1 } } }),
  db.cv.update({ where: { id: cvId }, data: { data: newData } }),
])

// Interactive transaction (with logic)
const result = await db.$transaction(async (tx) => {
  const user = await tx.user.findUnique({ where: { id: userId } })
  if (!user) throw new Error("User not found")

  if (user.plan === "FREE" && user.aiUsageThisMonth >= 3) {
    throw new Error("AI usage limit reached")
  }

  await tx.user.update({
    where: { id: userId },
    data: { aiUsageThisMonth: { increment: 1 } },
  })

  return { success: true, remaining: 3 - user.aiUsageThisMonth - 1 }
}, {
  maxWait: 5000,   // Max wait to acquire transaction
  timeout: 10000,  // Max transaction run time
})

// Nested write (automatic transaction)
const userWithCv = await db.user.create({
  data: {
    email: "user@example.com",
    name: "New User",
    cvs: {
      create: {
        title: "My First CV",
        data: defaultCvData,
      },
    },
  },
  include: { cvs: true },
})
```

## Error Handling

```typescript
import { Prisma } from "@prisma/client"  // Prisma 6
// import { Prisma } from "../generated/prisma"  // Prisma 7

try {
  await db.user.create({ data: { email: "dup@example.com" } })
} catch (e) {
  if (e instanceof Prisma.PrismaClientKnownRequestError) {
    switch (e.code) {
      case "P2002":
        // Unique constraint violation
        const target = (e.meta?.target as string[])?.join(", ")
        return { error: `Duplicate value for: ${target}` }
      case "P2003":
        return { error: "Referenced record does not exist" }
      case "P2025":
        return { error: "Record not found" }
      default:
        return { error: `Database error: ${e.code}` }
    }
  }
  if (e instanceof Prisma.PrismaClientValidationError) {
    return { error: "Invalid data provided" }
  }
  throw e
}
```

## Client Extensions

```typescript
// Soft delete extension
const db = new PrismaClient().$extends({
  query: {
    cv: {
      async delete({ args, query }) {
        // Convert delete to soft delete
        return db.cv.update({
          where: args.where,
          data: { deletedAt: new Date() },
        })
      },
      async findMany({ args, query }) {
        // Exclude soft-deleted by default
        args.where = { ...args.where, deletedAt: null }
        return query(args)
      },
    },
  },
})

// Logging extension
const db = new PrismaClient().$extends({
  query: {
    $allModels: {
      async $allOperations({ model, operation, args, query }) {
        const start = Date.now()
        const result = await query(args)
        const duration = Date.now() - start
        if (duration > 1000) {
          console.warn(`Slow query: ${model}.${operation} took ${duration}ms`)
        }
        return result
      },
    },
  },
})

// Computed fields extension
const db = new PrismaClient().$extends({
  result: {
    user: {
      displayName: {
        needs: { name: true, email: true },
        compute(user) {
          return user.name || user.email.split("@")[0]
        },
      },
    },
  },
})
```
