# Next.js 16 Specific Patterns

> Server Components, Server Actions, Route Handlers, use cache, singleton pattern, proxy.ts runtime.
> Sources: Next.js docs, Prisma docs, CViet project experience.
> Date: 2026-02-27

---

## Server Components + Prisma (Read)

```typescript
// app/(app)/dashboard/page.tsx — Server Component (default)
import { db } from "@/lib/db"
import { getSession } from "@/lib/auth-helpers"

export default async function DashboardPage() {
  const session = await getSession()
  if (!session) redirect("/login")

  const cvs = await db.cv.findMany({
    where: { userId: session.user.id },
    orderBy: { updatedAt: "desc" },
    select: {
      id: true,
      title: true,
      template: true,
      language: true,
      updatedAt: true,
    },
  })

  return <CVList cvs={cvs} />
}
```

## Server Actions + Prisma (Write)

```typescript
// app/(app)/cv/[id]/actions.ts
"use server"

import { db } from "@/lib/db"
import { getSession } from "@/lib/auth-helpers"
import { revalidatePath } from "next/cache"

export async function updateCV(cvId: string, data: CVData) {
  const session = await getSession()
  if (!session) throw new Error("Unauthorized")

  // Verify ownership
  const cv = await db.cv.findFirst({
    where: { id: cvId, userId: session.user.id },
  })
  if (!cv) throw new Error("CV not found")

  await db.cv.update({
    where: { id: cvId },
    data: { data: data as unknown as Prisma.InputJsonValue },
  })

  revalidatePath(`/cv/${cvId}`)
  return { success: true }
}

export async function deleteCV(cvId: string) {
  const session = await getSession()
  if (!session) throw new Error("Unauthorized")

  await db.cv.delete({
    where: { id: cvId, userId: session.user.id },
  })

  revalidatePath("/dashboard")
  return { success: true }
}
```

## Route Handlers + Prisma

```typescript
// app/api/cv/[id]/route.ts
import { db } from "@/lib/db"
import { NextRequest, NextResponse } from "next/server"
import { getSession } from "@/lib/auth-helpers"

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params  // Must await in Next.js 16
  const session = await getSession()
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }

  const cv = await db.cv.findFirst({
    where: { id, userId: session.user.id },
  })

  if (!cv) {
    return NextResponse.json({ error: "Not found" }, { status: 404 })
  }

  return NextResponse.json(cv)
}
```

## use cache + Prisma

```typescript
// Caching expensive queries (Next.js 16)
import { db } from "@/lib/db"

async function getTemplateCount() {
  "use cache"
  // This result gets cached across requests
  const count = await db.cv.groupBy({
    by: ["template"],
    _count: true,
  })
  return count
}

// IMPORTANT: Cannot use cookies/headers inside 'use cache'
// Extract auth info BEFORE the cached function
export default async function StatsPage() {
  const session = await getSession()  // Extracts cookies outside cache
  if (!session) redirect("/login")

  const stats = await getTemplateCount()  // Cached query
  return <Stats data={stats} />
}
```

## Prisma Singleton for Development Hot Reload

This is critical for Next.js development to prevent connection pool exhaustion:

```typescript
// src/lib/db.ts — works for both Prisma 6 and 7

// --- Prisma 6 (current CViet) ---
import { PrismaClient } from "@prisma/client"

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const db =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["query", "error", "warn"] : ["error"],
  })

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = db


// --- Prisma 7 (future upgrade) ---
import { PrismaClient } from "../generated/prisma"
import { PrismaNeon } from "@prisma/adapter-neon"

const adapter = new PrismaNeon({
  connectionString: process.env.DATABASE_URL!,
})

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const db =
  globalForPrisma.prisma ?? new PrismaClient({ adapter })

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = db
```

## proxy.ts Runtime Configuration

```typescript
// src/proxy.ts — Must use Node.js runtime for Prisma
export const runtime = "nodejs"  // NOT "edge"

export function proxy(request: Request) {
  // Can use Prisma here because we're on Node.js runtime
  // Edge runtime cannot make TCP connections to PostgreSQL
}
```
