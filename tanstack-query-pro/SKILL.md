---
name: tanstack-query-pro
description: "TanStack Query v5 for Next.js 16 App Router. SSR prefetch/dehydrate, mutations, optimistic updates, infinite queries, 18 documented errors. Triggers: tanstack query, react query, useQuery, useMutation, prefetch, dehydrate, data fetching, cache invalidation."
---

# TanStack Query Pro -- Data Fetching for Next.js 16

## When to Use

Trigger on any mention of: tanstack query, react query, useQuery, useMutation, useSuspenseQuery, prefetch, dehydrate, HydrationBoundary, cache invalidation, optimistic updates, infinite scroll, staleTime, gcTime.

## Reference Files

Load the relevant reference file(s) based on what the user needs:

| File | Description |
|------|-------------|
| `references/setup.md` | Version compatibility (TQ v5.90+ / React 19 / Next.js 16), v4-to-v5 breaking changes (14 entries), migration codemod, installation, QueryClientProvider with `useState` pattern, DevTools setup |
| `references/ssr-patterns.md` | 3 SSR approaches: Prefetch+Dehydrate (recommended), StreamedHydration, Streaming Prefetch (v5.40+). When-to-use decision table |
| `references/queries.md` | useQuery, useSuspenseQuery, queryOptions helper, skipToken, query key factory, parallel queries, dependent queries |
| `references/mutations.md` | useMutation, mutate vs mutateAsync, optimistic updates (UI-based and cache-based), invalidation strategies (5 methods) |
| `references/infinite-queries.md` | useInfiniteQuery, Intersection Observer auto-load, traditional page-number pagination, keepPreviousData |
| `references/caching.md` | staleTime/gcTime strategies by data type, global defaults, cache lifecycle diagram (FRESH -> STALE -> INACTIVE -> GC) |
| `references/performance.md` | select transforms, placeholderData, hover/focus prefetching, structural sharing, query cancellation with AbortSignal |
| `references/typescript.md` | Type inference patterns, custom error types, queryOptions for type-safe sharing, skipToken conditional queries, mutation type safety |
| `references/testing.md` | Test wrapper/utilities, renderHook for hooks, mutation testing, component testing with renderWithQuery |
| `references/errors.md` | 18 documented errors (TQ-001 through TQ-018) with exact messages, causes, and fixes |
| `references/cviet-patterns.md` | CViet project setup (as-is), expanded query key factory, AI enhancement caching, dashboard SSR prefetch, CV auto-save with debounce, billing/plan hooks |
| `references/quick-reference.md` | Query status flags table, hook quick reference, QueryClient methods, common import patterns, all sources |

## Error Quick Lookup

| ID | Error | Fix |
|----|-------|-----|
| TQ-001 | No QueryClient set | Wrap in QueryClientProvider, use `useState` for client |
| TQ-002 | Missing queryFn | Always provide queryFn to useQuery |
| TQ-003 | Hydration mismatch | Ensure same data on server/client with dehydrate |
| TQ-004 | Query data undefined | queryFn must return a value, check `res.ok` and throw |
| TQ-005 | Stale data after mutation | `queryClient.invalidateQueries({ queryKey })` |
| TQ-006 | Infinite re-renders | Move queryFn outside component, stable queryKey |
| TQ-007 | undefined.length in infinite | Use distinct keys for useQuery vs useInfiniteQuery |
| TQ-008 | Data disappears on nav | Create QueryClient in `useState`, raise gcTime |
| TQ-009 | gcTime 0 hydration error | Use `gcTime: 2000` minimum |
| TQ-010 | fetch no throw on 4xx/5xx | Custom fetch wrapper that throws on error status |
| TQ-011 | QueryKey type error | Use `as const` on query key arrays |
| TQ-012 | Rendered more hooks | Use `enabled` or `skipToken`, never conditional hooks |
| TQ-013 | Refetch overwrites optimistic | Cancel queries in `onMutate` before setting cache |
| TQ-014 | Suspense hydration error | Prefetch on server or use ReactQueryStreamedHydration |
| TQ-015 | Module-level QueryClient | Create inside `useState` callback, not module scope |
| TQ-016 | DevTools missing in prod | Intentional; import from devtools/production if needed |
| TQ-017 | isLoading always false | Renamed in v5: use `isPending` instead |
| TQ-018 | cacheTime not valid | Renamed in v5: use `gcTime` instead |

## Key Patterns

### SSR Prefetch (Recommended)
```tsx
// Server Component
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query'

export default async function DashboardPage() {
  const queryClient = new QueryClient()
  await queryClient.prefetchQuery({ queryKey: ['cvs'], queryFn: fetchCVs })
  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <CVList />
    </HydrationBoundary>
  )
}
```

### Query Key Factory
```tsx
export const cvKeys = {
  all: ['cvs'] as const,
  lists: () => [...cvKeys.all, 'list'] as const,
  detail: (id: string) => [...cvKeys.all, 'detail', id] as const,
}
```

### Optimistic Update (Cache-Based)
```tsx
onMutate: async (newData) => {
  await queryClient.cancelQueries({ queryKey: ['cvs'] })
  const previous = queryClient.getQueryData(['cvs'])
  queryClient.setQueryData(['cvs'], (old) => /* update */)
  return { previous }
},
onError: (err, vars, ctx) => queryClient.setQueryData(['cvs'], ctx.previous),
onSettled: () => queryClient.invalidateQueries({ queryKey: ['cvs'] }),
```
