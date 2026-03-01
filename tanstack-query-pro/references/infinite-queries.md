# Infinite Queries & Pagination

---

## 6.1 useInfiniteQuery

```tsx
"use client"
import { useInfiniteQuery } from "@tanstack/react-query"

interface CVPage {
  cvs: CV[]
  nextCursor: string | null
  totalCount: number
}

function CVInfiniteList() {
  const {
    data,
    fetchNextPage,
    fetchPreviousPage,
    hasNextPage,
    hasPreviousPage,
    isFetchingNextPage,
    isFetchingPreviousPage,
    isLoading,
    isError,
    error,
  } = useInfiniteQuery({
    queryKey: ["cvs", "infinite"],
    queryFn: async ({ pageParam }): Promise<CVPage> => {
      const res = await fetch(`/api/cv?cursor=${pageParam}&limit=12`)
      return res.json()
    },
    initialPageParam: "",           // First page has no cursor
    getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
    // Return undefined to signal no more pages
    // null/undefined = hasNextPage becomes false

    // Optional: bi-directional
    getPreviousPageParam: (firstPage) => firstPage.previousCursor ?? undefined,

    // Optional: limit cached pages (v5 feature)
    maxPages: 5,  // Only keep 5 pages in cache; refetch only those 5 on stale
  })

  // data.pages is an array of page results
  // data.pageParams is an array of page params used
  const allCVs = data?.pages.flatMap(page => page.cvs) ?? []

  return (
    <div>
      {allCVs.map(cv => <CVCard key={cv.id} cv={cv} />)}

      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? "Loading..." : hasNextPage ? "Load More" : "No more CVs"}
      </button>
    </div>
  )
}
```

## 6.2 Intersection Observer for Auto-Load

```tsx
import { useRef, useEffect } from "react"

function useIntersectionObserver(
  callback: () => void,
  options?: IntersectionObserverInit
) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) callback()
    }, options)

    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [callback, options])

  return ref
}

// Usage in component:
function CVInfiniteScroll() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteQuery({...})

  const loadMoreRef = useIntersectionObserver(
    () => { if (hasNextPage && !isFetchingNextPage) fetchNextPage() },
    { threshold: 0.5 }
  )

  return (
    <div>
      {data?.pages.flatMap(p => p.cvs).map(cv => <CVCard key={cv.id} cv={cv} />)}
      <div ref={loadMoreRef} className="h-10" />  {/* Sentinel element */}
    </div>
  )
}
```

## 6.3 Traditional Pagination (Page Numbers)

```tsx
function CVPaginatedList() {
  const [page, setPage] = useState(1)

  const { data, isPending, isPlaceholderData } = useQuery({
    queryKey: ["cvs", "page", page],
    queryFn: () => fetch(`/api/cv?page=${page}&limit=12`).then(r => r.json()),
    placeholderData: keepPreviousData,  // Show old data while new page loads
  })

  return (
    <div style={{ opacity: isPlaceholderData ? 0.5 : 1 }}>
      {data?.cvs.map(cv => <CVCard key={cv.id} cv={cv} />)}

      <div className="flex gap-2">
        <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>
          Previous
        </button>
        <span>Page {page}</span>
        <button
          onClick={() => setPage(p => p + 1)}
          disabled={isPlaceholderData || !data?.hasMore}
        >
          Next
        </button>
      </div>
    </div>
  )
}
```
