# Next.js 16 App Router SSR Patterns

---

## 3.1 Approach A: Prefetch + Dehydrate (Recommended)

The standard pattern: prefetch in a Server Component, pass dehydrated state to client.

**Server Component (page.tsx)**:

```tsx
// src/app/(app)/dashboard/page.tsx  -- Server Component
import { dehydrate, HydrationBoundary, QueryClient } from "@tanstack/react-query"
import { DashboardContent } from "./dashboard-content"

// Direct DB/API call (server-only)
async function getCVs(userId: string) {
  // Can use Prisma directly here -- no fetch() needed
  return prisma.cv.findMany({ where: { userId }, orderBy: { updatedAt: "desc" } })
}

export default async function DashboardPage() {
  const session = await auth()  // Better Auth server-side
  const queryClient = new QueryClient()

  await queryClient.prefetchQuery({
    queryKey: ["cvs"],
    queryFn: () => getCVs(session.user.id),
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <DashboardContent />
    </HydrationBoundary>
  )
}
```

**Client Component**:

```tsx
// src/app/(app)/dashboard/dashboard-content.tsx
"use client"
import { useQuery } from "@tanstack/react-query"

export function DashboardContent() {
  // Data is available IMMEDIATELY from dehydrated state -- no loading flash
  const { data: cvs = [] } = useQuery({
    queryKey: ["cvs"],
    queryFn: () => fetch("/api/cv").then(r => r.json()),
  })

  return <div>{/* render cvs */}</div>
}
```

**How it works**:
1. Server Component prefetches data and creates a dehydrated snapshot
2. `HydrationBoundary` injects the snapshot into `QueryClient` on the client
3. Client component's `useQuery` finds data already in cache -- no re-fetch
4. After `staleTime` expires, background refetch keeps data fresh

## 3.2 Approach B: Streaming with Suspense (No Manual Prefetch)

Uses `@tanstack/react-query-next-experimental` to auto-stream data from server to client.

**Provider Setup**:

```tsx
"use client"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { ReactQueryStreamedHydration } from "@tanstack/react-query-next-experimental"
import { useState } from "react"

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())

  return (
    <QueryClientProvider client={queryClient}>
      <ReactQueryStreamedHydration>
        {children}
      </ReactQueryStreamedHydration>
    </QueryClientProvider>
  )
}
```

**Client Component with useSuspenseQuery**:

```tsx
"use client"
import { useSuspenseQuery } from "@tanstack/react-query"

function CVList() {
  // This fires on the server during SSR, streams result to client
  const { data: cvs } = useSuspenseQuery({
    queryKey: ["cvs"],
    queryFn: () => fetch("/api/cv").then(r => r.json()),
  })

  return <div>{cvs.map(cv => <CVCard key={cv.id} cv={cv} />)}</div>
}

// Wrap with Suspense boundary
export function DashboardContent() {
  return (
    <Suspense fallback={<CVListSkeleton />}>
      <CVList />
    </Suspense>
  )
}
```

**Benefits**: No manual prefetching, still gets SSR + streaming. The `useSuspenseQuery` call initiates the fetch on the server during SSR, and the result streams to the client as the Suspense boundary resolves.

**Trade-off**: Less control over what gets prefetched; slightly more complex debugging.

## 3.3 Approach C: Streaming Prefetch (v5.40.0+)

As of v5.40.0, you do NOT need to `await` all prefetches. Pending queries can be dehydrated and streamed.

```tsx
// Server Component -- no await needed
export default async function DashboardPage() {
  const queryClient = new QueryClient()

  // Fire-and-forget prefetch -- streams when ready
  queryClient.prefetchQuery({
    queryKey: ["cvs"],
    queryFn: () => getCVs(userId),
  })

  // This one we await because it's critical for layout
  await queryClient.prefetchQuery({
    queryKey: ["user-plan"],
    queryFn: () => getUserPlan(userId),
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <DashboardContent />
    </HydrationBoundary>
  )
}
```

## 3.4 When to Use Each Approach

| Approach | Best For | CViet Use Case |
|----------|----------|----------------|
| **A: Prefetch + Dehydrate** | Pages with known data needs, SEO-critical content | Dashboard CV list, landing page |
| **B: Streaming Suspense** | Dynamic client components, real-time data | AI panel responses, live preview |
| **C: Streaming Prefetch** | Mix of critical + non-critical data | Dashboard (plan = critical, CVs = stream) |
