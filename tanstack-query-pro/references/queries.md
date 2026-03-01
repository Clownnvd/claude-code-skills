# Query Patterns

---

## 4.1 useQuery -- Basic Data Fetching

```tsx
"use client"
import { useQuery } from "@tanstack/react-query"

function CVList() {
  const {
    data,           // TData | undefined
    error,          // Error | null
    isLoading,      // true on first load (no cached data)
    isPending,      // true when status === "pending" (renamed from isLoading in v5)
    isFetching,     // true whenever a fetch is in-flight (including background)
    isError,        // true when status === "error"
    isSuccess,      // true when status === "success"
    isStale,        // true when data is older than staleTime
    refetch,        // Manually trigger refetch
    isPlaceholderData, // true when showing placeholder data
  } = useQuery({
    queryKey: ["cvs"],           // Unique cache key (array)
    queryFn: fetchCVs,           // Promise-returning function
    staleTime: 5 * 60 * 1000,   // 5 minutes fresh
    gcTime: 10 * 60 * 1000,     // 10 minutes in cache after inactive
    retry: 2,                    // Retry failed requests 2 times
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    enabled: true,               // Set false to disable auto-fetching
    refetchOnWindowFocus: true,
    refetchOnMount: true,
    refetchOnReconnect: true,
    refetchInterval: false,      // Set ms for polling
    select: (data) => data,      // Transform data before returning
    placeholderData: undefined,  // Show while loading (not cached)
    initialData: undefined,      // Pre-populate cache (counts as "fetched")
  })
}
```

## 4.2 useSuspenseQuery -- Suspense Integration

```tsx
"use client"
import { useSuspenseQuery } from "@tanstack/react-query"

function CVDetail({ id }: { id: string }) {
  // data is ALWAYS defined (never undefined)
  // status is ALWAYS "success"
  // No need to check isLoading/isError -- handled by Suspense + ErrorBoundary
  const { data: cv } = useSuspenseQuery({
    queryKey: ["cvs", id],
    queryFn: () => fetch(`/api/cv/${id}`).then(r => r.json()),
  })

  return <div>{cv.title}</div>
}

// Usage with Suspense boundary:
import { Suspense } from "react"
import { ErrorBoundary } from "react-error-boundary"

function CVPage({ id }: { id: string }) {
  return (
    <ErrorBoundary fallback={<div>Error loading CV</div>}>
      <Suspense fallback={<CVSkeleton />}>
        <CVDetail id={id} />
      </Suspense>
    </ErrorBoundary>
  )
}
```

**Key differences from useQuery**:
- `data` is always defined (type `TData`, not `TData | undefined`)
- `status` is always `"success"`
- `isLoading`/`isPending` are always `false`
- Errors throw to nearest `ErrorBoundary`
- Loading states handled by nearest `Suspense` boundary
- No `enabled` option -- use `skipToken` for conditional queries
- No `placeholderData` option

## 4.3 Query Key Factory Pattern

```tsx
// src/lib/query-keys.ts
export const cvKeys = {
  all:      ["cvs"] as const,
  lists:    () => [...cvKeys.all, "list"] as const,
  list:     (filters: CVFilters) => [...cvKeys.lists(), filters] as const,
  details:  () => [...cvKeys.all, "detail"] as const,
  detail:   (id: string) => [...cvKeys.details(), id] as const,
}

// Usage:
queryClient.invalidateQueries({ queryKey: cvKeys.all })       // Invalidate ALL cv queries
queryClient.invalidateQueries({ queryKey: cvKeys.lists() })    // Invalidate only lists
queryClient.invalidateQueries({ queryKey: cvKeys.detail(id) }) // Invalidate one detail
```

## 4.4 queryOptions Helper (Type-Safe Sharing)

```tsx
import { queryOptions } from "@tanstack/react-query"

// Define once, use everywhere
export function cvDetailOptions(id: string) {
  return queryOptions({
    queryKey: cvKeys.detail(id),
    queryFn: () => fetch(`/api/cv/${id}`).then(r => r.json()) as Promise<CV>,
    staleTime: 5 * 60 * 1000,
  })
}

// In component:
const { data } = useQuery(cvDetailOptions(id))

// In server prefetch:
await queryClient.prefetchQuery(cvDetailOptions(id))

// For type-safe cache read:
const cv = queryClient.getQueryData(cvDetailOptions(id).queryKey)
// cv is typed as CV | undefined
```

## 4.5 Conditional Queries with skipToken

```tsx
import { useQuery, skipToken } from "@tanstack/react-query"

function CVDetail({ id }: { id: string | undefined }) {
  const { data } = useQuery({
    queryKey: ["cvs", id],
    queryFn: id ? () => fetchCV(id) : skipToken,
    // When skipToken is passed, the query is disabled
    // TypeScript knows data could be undefined
  })
}
```

**Why `skipToken` over `enabled: false`**:
- `skipToken` provides full TypeScript inference
- The queryFn type narrows correctly based on the condition
- No risk of calling queryFn with undefined parameters

## 4.6 Parallel Queries

```tsx
import { useQueries, useSuspenseQueries } from "@tanstack/react-query"

function Dashboard() {
  const results = useQueries({
    queries: [
      { queryKey: ["cvs"], queryFn: fetchCVs },
      { queryKey: ["user-plan"], queryFn: fetchUserPlan },
      { queryKey: ["ai-usage"], queryFn: fetchAIUsage },
    ],
  })

  const [cvsResult, planResult, usageResult] = results
  // Each result has its own status, data, error, etc.
}
```

## 4.7 Dependent Queries

```tsx
function CVWithTemplate({ cvId }: { cvId: string }) {
  // First query: fetch the CV
  const { data: cv } = useQuery({
    queryKey: ["cvs", cvId],
    queryFn: () => fetchCV(cvId),
  })

  // Second query: depends on first query's result
  const { data: template } = useQuery({
    queryKey: ["templates", cv?.template],
    queryFn: () => fetchTemplate(cv!.template),
    enabled: !!cv?.template, // Only runs when cv.template is available
  })
}
```
