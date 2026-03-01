# Caching Strategies

---

## 7.1 Key Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `staleTime` | `0` | How long data is "fresh" (no refetch). Set higher to reduce requests. |
| `gcTime` | `5 * 60 * 1000` (5 min) | How long inactive data stays in memory before GC. |
| `retry` | `3` (client) / `0` (server) | Number of retry attempts on failure. |
| `retryDelay` | Exponential backoff | `(attempt) => Math.min(1000 * 2 ** attempt, 30000)` |
| `refetchOnWindowFocus` | `true` | Refetch stale queries when window regains focus. |
| `refetchOnMount` | `true` | Refetch stale queries when component mounts. |
| `refetchOnReconnect` | `true` | Refetch stale queries on network reconnect. |
| `refetchInterval` | `false` | Poll interval in ms. Set to enable polling. |

## 7.2 Recommended Strategies by Data Type

```tsx
// Static reference data (templates, plan features) -- cache aggressively
const { data: templates } = useQuery({
  queryKey: ["templates"],
  queryFn: fetchTemplates,
  staleTime: Infinity,    // Never stale -- only manual invalidation
  gcTime: Infinity,       // Never garbage collected
})

// User-specific dashboard data -- moderate freshness
const { data: cvs } = useQuery({
  queryKey: ["cvs"],
  queryFn: fetchCVs,
  staleTime: 60 * 1000,  // Fresh for 1 minute
  gcTime: 5 * 60 * 1000, // Keep in cache 5 minutes
})

// Real-time data (AI generation status) -- always fresh
const { data: status } = useQuery({
  queryKey: ["ai-status", jobId],
  queryFn: () => fetchAIStatus(jobId),
  staleTime: 0,                 // Always stale
  refetchInterval: 2000,        // Poll every 2 seconds
  refetchIntervalInBackground: false,  // Stop polling when tab hidden
})

// Frequently changing data (billing) -- fresh on mount
const { data: usage } = useQuery({
  queryKey: ["ai-usage"],
  queryFn: fetchAIUsage,
  staleTime: 0,                  // Always refetch on mount
  refetchOnWindowFocus: true,    // Refetch when user returns
})
```

## 7.3 Global Defaults

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,     // 1 minute default
      gcTime: 5 * 60 * 1000,    // 5 minutes default
      retry: 1,
      refetchOnWindowFocus: true,
    },
    mutations: {
      retry: 0,  // Don't retry mutations by default
      onError: (error) => {
        console.error("Mutation error:", error)
        // Global error toast
      },
    },
  },
})
```

## 7.4 Cache Lifecycle

```
Query created -> FRESH (staleTime countdown starts)
                    |
                    v (staleTime expires)
                  STALE (background refetch on mount/focus/reconnect)
                    |
                    v (component unmounts, query becomes inactive)
                INACTIVE (gcTime countdown starts)
                    |
                    v (gcTime expires)
                GARBAGE COLLECTED (removed from cache)
```
