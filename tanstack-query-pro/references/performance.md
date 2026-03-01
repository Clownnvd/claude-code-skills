# Performance Patterns

---

## 8.1 select -- Transform & Reduce Data

The `select` option transforms data BEFORE it reaches the component. If the selected result is referentially equal to the previous result, the component does NOT re-render.

```tsx
// Only get CV count -- component won't re-render when CV data changes, only when count changes
const { data: cvCount } = useQuery({
  queryKey: ["cvs"],
  queryFn: fetchCVs,
  select: (cvs) => cvs.length,
})

// Filter CVs by template
const { data: classicCVs } = useQuery({
  queryKey: ["cvs"],
  queryFn: fetchCVs,
  select: (cvs) => cvs.filter(cv => cv.template === "classic"),
})

// IMPORTANT: memoize the select function if it creates new references
const selectClassicCVs = useCallback(
  (cvs: CV[]) => cvs.filter(cv => cv.template === "classic"),
  []
)
```

## 8.2 placeholderData (Replaces keepPreviousData)

```tsx
import { keepPreviousData } from "@tanstack/react-query"

// Keep showing old page data while new page loads
const { data, isPlaceholderData } = useQuery({
  queryKey: ["cvs", page],
  queryFn: () => fetchCVs(page),
  placeholderData: keepPreviousData,  // Built-in identity function
})

// Custom placeholder: use cached data from related query
const { data } = useQuery({
  queryKey: ["cvs", filters],
  queryFn: () => fetchCVs(filters),
  placeholderData: () => queryClient.getQueryData(["cvs"]),  // Fall back to unfiltered list
})
```

## 8.3 Prefetching on Hover/Focus

```tsx
function CVLink({ cv }: { cv: CV }) {
  const queryClient = useQueryClient()

  const prefetchCV = () => {
    queryClient.prefetchQuery({
      queryKey: ["cvs", cv.id],
      queryFn: () => fetchCV(cv.id),
      staleTime: 5 * 60 * 1000,  // Don't prefetch if already fresh
    })
  }

  return (
    <Link
      href={`/cv/${cv.id}`}
      onMouseEnter={prefetchCV}
      onFocus={prefetchCV}
    >
      {cv.title}
    </Link>
  )
}
```

## 8.4 Structural Sharing

TanStack Query uses structural sharing by default -- if the refetched data is deeply equal to the cached data, the same reference is returned, preventing unnecessary re-renders.

```tsx
// This works automatically for JSON-serializable data.
// For non-serializable data, disable it:
useQuery({
  queryKey: ["data"],
  queryFn: fetchData,
  structuralSharing: false,  // Disable for Map/Set/Date objects
})
```

## 8.5 Query Cancellation

```tsx
const { data } = useQuery({
  queryKey: ["cvs", search],
  queryFn: async ({ signal }) => {
    // signal is AbortSignal -- auto-cancelled when query key changes
    const res = await fetch(`/api/cv?search=${search}`, { signal })
    return res.json()
  },
})
```
