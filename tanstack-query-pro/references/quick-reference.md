# Quick Reference Cards

---

## Query Status Flags (v5)

| Flag | Meaning |
|------|---------|
| `isPending` | Status is `"pending"` -- no data yet, might have cached data from before |
| `isLoading` | `isPending && isFetching` -- first load, truly no data |
| `isFetching` | Any fetch in-flight (initial or background) |
| `isSuccess` | Status is `"success"` -- data available |
| `isError` | Status is `"error"` -- error occurred |
| `isStale` | Data older than `staleTime` |
| `isPlaceholderData` | Showing placeholder/previous data |
| `isFetched` | Query has been fetched at least once |
| `isRefetching` | `isFetching && !isPending` -- background refetch |

## Hook Quick Reference

| Hook | Purpose |
|------|---------|
| `useQuery` | Fetch & cache data |
| `useSuspenseQuery` | Fetch with Suspense (data always defined) |
| `useQueries` | Multiple parallel queries |
| `useSuspenseQueries` | Multiple parallel Suspense queries |
| `useInfiniteQuery` | Paginated / infinite scroll |
| `useSuspenseInfiniteQuery` | Infinite scroll with Suspense |
| `useMutation` | Create / Update / Delete operations |
| `useQueryClient` | Access QueryClient for cache operations |
| `useIsFetching` | Count of in-flight queries |
| `useIsMutating` | Count of in-flight mutations |
| `useMutationState` | Get mutation state shared across components |
| `usePrefetchQuery` | Declarative prefetching |

## QueryClient Methods

| Method | Description |
|--------|-------------|
| `invalidateQueries({ queryKey })` | Mark queries stale + trigger refetch |
| `refetchQueries({ queryKey })` | Force refetch (even if not stale) |
| `cancelQueries({ queryKey })` | Cancel in-flight queries |
| `removeQueries({ queryKey })` | Remove from cache entirely |
| `resetQueries({ queryKey })` | Reset to initial state |
| `setQueryData(key, data)` | Directly set cache data |
| `getQueryData(key)` | Read from cache |
| `prefetchQuery(options)` | Pre-populate cache |
| `fetchQuery(options)` | Fetch and return data (throws on error) |
| `ensureQueryData(options)` | Like fetchQuery but returns cache if fresh |
| `clear()` | Clear entire cache |

## Common Import Patterns

```tsx
// Core hooks
import {
  useQuery,
  useSuspenseQuery,
  useInfiniteQuery,
  useMutation,
  useQueryClient,
  useQueries,
  useMutationState,
  skipToken,
  keepPreviousData,
  queryOptions,
} from "@tanstack/react-query"

// Provider
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

// Hydration (SSR)
import { dehydrate, HydrationBoundary, QueryClient } from "@tanstack/react-query"

// DevTools
import { ReactQueryDevtools } from "@tanstack/react-query-devtools"

// Experimental streaming
import { ReactQueryStreamedHydration } from "@tanstack/react-query-next-experimental"
```

---

## Sources

- [TanStack Query React Overview](https://tanstack.com/query/latest/docs/framework/react/overview)
- [Advanced Server Rendering Guide](https://tanstack.com/query/latest/docs/framework/react/guides/advanced-ssr)
- [Migrating to v5](https://tanstack.com/query/v5/docs/react/guides/migrating-to-v5)
- [Announcing TanStack Query v5](https://tanstack.com/blog/announcing-tanstack-query-v5)
- [Important Defaults](https://tanstack.com/query/v5/docs/react/guides/important-defaults)
- [Suspense Guide](https://tanstack.com/query/v5/docs/framework/react/guides/suspense)
- [Optimistic Updates](https://tanstack.com/query/v5/docs/react/guides/optimistic-updates)
- [Infinite Queries](https://tanstack.com/query/v5/docs/framework/react/guides/infinite-queries)
- [TypeScript Guide](https://tanstack.com/query/v5/docs/framework/react/typescript)
- [Query Options](https://tanstack.com/query/v5/docs/framework/react/guides/query-options)
- [DevTools](https://tanstack.com/query/v5/docs/react/devtools)
- [Testing Guide](https://tanstack.com/query/v4/docs/framework/react/guides/testing)
- [Server Rendering & Hydration](https://tanstack.com/query/v5/docs/react/guides/ssr)
- [TanStack Query Next.js App Prefetching Example](https://tanstack.com/query/latest/docs/framework/react/examples/nextjs-app-prefetching)
- [Next.js Suspense Streaming Example](https://tanstack.com/query/v5/docs/framework/react/examples/nextjs-suspense-streaming)
- [Combining RSC with React Query (Frontend Masters)](https://frontendmasters.com/blog/combining-react-server-components-with-react-query-for-easy-data-management/)
- [Integrate TanStack Query with Next.js App Router (Storieasy)](https://www.storieasy.com/blog/integrate-tanstack-query-with-next-js-app-router-2025-ultimate-guide)
- [Testing React Query (TkDodo)](https://tkdodo.eu/blog/testing-react-query)
- [GitHub Discussion #5725 - RSC Compatibility](https://github.com/TanStack/query/discussions/5725)
- [GitHub Discussion #6267 - Hydration Boundary](https://github.com/TanStack/query/discussions/6267)
- [GitHub Issue #9399 - Hydration Error with Loading State](https://github.com/TanStack/query/issues/9399)
- [GitHub Issue #9642 - Race Condition Streaming](https://github.com/TanStack/query/issues/9642)
