# Common Errors & Fixes

---

### TQ-001: "No QueryClient set, use QueryClientProvider to set one"

**Cause**: Using TanStack Query hooks outside of `QueryClientProvider`.

**Fix**: Ensure `QueryClientProvider` wraps the component tree in `layout.tsx`.

```tsx
// src/app/layout.tsx
import { QueryProvider } from "@/providers/query-provider"

export default function RootLayout({ children }) {
  return (
    <html><body>
      <QueryProvider>{children}</QueryProvider>
    </body></html>
  )
}
```

---

### TQ-002: "Missing queryFn for queryKey"

**Cause**: `useQuery` called without a `queryFn` and no `defaultOptions.queryFn` set on `QueryClient`.

**Fix**: Always provide `queryFn` to `useQuery`:

```tsx
// BAD
useQuery({ queryKey: ["cvs"] })

// GOOD
useQuery({ queryKey: ["cvs"], queryFn: fetchCVs })
```

---

### TQ-003: Hydration Mismatch (SSR)

**Cause**: Server-rendered HTML differs from client render. Common when `useSuspenseQuery` data was not prefetched on the server.

**Fix**: Ensure the same query is prefetched on the server:

```tsx
// Server Component
await queryClient.prefetchQuery({
  queryKey: ["cvs"],
  queryFn: getCVs,
})

// Client Component -- must use SAME queryKey
const { data } = useSuspenseQuery({
  queryKey: ["cvs"],
  queryFn: fetchCVs,
})
```

---

### TQ-004: "query data cannot be undefined"

**Cause**: `queryFn` returned `undefined` instead of data or `null`.

**Fix**: Always return a value:

```tsx
// BAD
queryFn: async () => {
  const res = await fetch("/api/cv")
  // fetch doesn't throw on 4xx/5xx
}

// GOOD
queryFn: async () => {
  const res = await fetch("/api/cv")
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()  // Returns parsed data, never undefined
}
```

---

### TQ-005: Stale Data After Mutation

**Cause**: Forgot to invalidate queries after a mutation.

**Fix**: Always invalidate related queries in `onSuccess` or `onSettled`:

```tsx
useMutation({
  mutationFn: updateCV,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["cvs"] })
  },
})
```

---

### TQ-006: Infinite Re-renders / Maximum Update Depth Exceeded

**Cause**: Creating new object/array references in `queryFn` or `select` on every render.

**Fix**: Memoize or move functions outside the component:

```tsx
// BAD -- new function reference every render
<Component select={(data) => data.filter(x => x.active)} />

// GOOD -- stable reference
const selectActive = useCallback((data: CV[]) => data.filter(x => x.active), [])
useQuery({ queryKey: ["cvs"], queryFn: fetchCVs, select: selectActive })

// BEST -- define outside component
const selectActive = (data: CV[]) => data.filter(x => x.active)
```

---

### TQ-007: "Cannot read properties of undefined (reading 'length')" in Infinite Queries

**Cause**: Mixing `useQuery` and `useInfiniteQuery` with the same query key, or `getNextPageParam` receiving undefined data.

**Fix**: Use distinct keys and guard against undefined:

```tsx
// Ensure different keys for different query types
useQuery({ queryKey: ["cvs", "list"] })
useInfiniteQuery({ queryKey: ["cvs", "infinite"] })

// Guard in getNextPageParam
getNextPageParam: (lastPage) => lastPage?.nextCursor ?? undefined
```

---

### TQ-008: Data Disappears After Navigation

**Cause**: `gcTime` too low, or QueryClient not persisted across navigations.

**Fix**: Ensure QueryClient is created in `useState` (not re-created on each render) and `gcTime` is reasonable:

```tsx
// GOOD -- stable client
const [queryClient] = useState(() => new QueryClient({
  defaultOptions: { queries: { gcTime: 5 * 60 * 1000 } }
}))

// BAD -- new client every render, loses all cache
const queryClient = new QueryClient()
```

---

### TQ-009: gcTime of 0 Causes Hydration Error

**Cause**: Setting `gcTime: 0` removes data from cache before React hydration completes.

**Fix**: Use `gcTime: 2000` minimum if you need short cache:

```tsx
// BAD
{ gcTime: 0 }

// GOOD -- minimum 2 seconds for hydration
{ gcTime: 2 * 1000 }
```

---

### TQ-010: fetch Doesn't Throw on Error Status Codes

**Cause**: Native `fetch()` only rejects on network errors, not HTTP 4xx/5xx.

**Fix**: Check `res.ok` and throw:

```tsx
queryFn: async () => {
  const res = await fetch("/api/cv")
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.message || `HTTP error ${res.status}`)
  }
  return res.json()
}
```

---

### TQ-011: TypeScript Error "Argument of type '...' is not assignable to parameter of type 'QueryKey'"

**Cause**: Query key not typed as `readonly` array.

**Fix**: Use `as const`:

```tsx
// BAD
queryKey: ["cvs", id]  // string[] -- not assignable to QueryKey

// GOOD
queryKey: ["cvs", id] as const
```

---

### TQ-012: "Rendered more hooks than during the previous render"

**Cause**: Conditional hook call (e.g., `if (id) useQuery({...})`).

**Fix**: Use `enabled` or `skipToken`:

```tsx
// BAD
if (id) {
  const { data } = useQuery({ queryKey: ["cvs", id], queryFn: () => fetchCV(id) })
}

// GOOD
const { data } = useQuery({
  queryKey: ["cvs", id ?? ""],
  queryFn: id ? () => fetchCV(id) : skipToken,
})
```

---

### TQ-013: Background Refetch Overwrites Optimistic Update

**Cause**: A refetch triggered by window focus or mount overwrites the optimistic cache update before the mutation completes.

**Fix**: Cancel outgoing queries in `onMutate`:

```tsx
onMutate: async (newData) => {
  await queryClient.cancelQueries({ queryKey: ["cvs"] })
  // ... set optimistic data
}
```

---

### TQ-014: "This Suspense boundary received an update before it finished hydrating"

**Cause**: Using `useSuspenseQuery` without proper server-side prefetching or `ReactQueryStreamedHydration`.

**Fix**: Either prefetch on server with `HydrationBoundary`, or use `ReactQueryStreamedHydration` from `@tanstack/react-query-next-experimental`.

---

### TQ-015: Module-Level QueryClient Shares State Between Users (SSR)

**Cause**: Creating QueryClient at module level in a Server Component or provider.

**Fix**: Always create inside `useState` or per-request:

```tsx
// BAD -- shared across all requests
const queryClient = new QueryClient()
export function Provider({ children }) { ... }

// GOOD -- per-component instance
export function Provider({ children }) {
  const [queryClient] = useState(() => new QueryClient())
  ...
}
```

---

### TQ-016: DevTools Not Showing in Production

**Cause**: DevTools are automatically excluded from production builds.

**Fix**: This is intentional. If you need production debugging:

```tsx
// Use production devtools explicitly
import { ReactQueryDevtools } from "@tanstack/react-query-devtools/production"
```

---

### TQ-017: "isLoading" Always False (v5 Migration)

**Cause**: `isLoading` was renamed to `isPending` in v5. The old `isLoading` now means `isPending && isFetching` (first load only, with no cached data).

**Fix**: Use the correct flag:

```tsx
// v4 -> v5 mapping:
// isLoading (v4) -> isPending (v5)       // Status is "pending"
// isLoading (v5) = isPending && isFetching  // First load, no cached data
// isInitialLoading (v4) -> isLoading (v5)   // Same meaning, different name
```

---

### TQ-018: "cacheTime is not a valid option"

**Cause**: `cacheTime` was renamed to `gcTime` in v5.

**Fix**: Replace all occurrences:

```tsx
// BAD (v4)
useQuery({ queryKey: ["cvs"], queryFn: fetchCVs, cacheTime: 5000 })

// GOOD (v5)
useQuery({ queryKey: ["cvs"], queryFn: fetchCVs, gcTime: 5000 })
```
