# Caching

> Source: https://nextjs.org/docs/app/guides/caching (v16.1.6)

## Four Caching Mechanisms

| Mechanism            | What              | Where  | Duration                        | Purpose                              |
|----------------------|-------------------|--------|---------------------------------|--------------------------------------|
| Request Memoization  | Function returns  | Server | Per-request lifecycle           | Dedupe fetches in component tree     |
| Data Cache           | Fetch data        | Server | Persistent (revalidatable)      | Cache across requests/deployments    |
| Full Route Cache     | HTML + RSC payload| Server | Persistent (revalidatable)      | Avoid re-rendering static routes     |
| Router Cache         | RSC payload       | Client | Session / time-based            | Instant client-side navigation       |

## Rendering Strategies

| Strategy | When rendered | Cached in Full Route Cache | Triggers |
|----------|--------------|---------------------------|----------|
| Static   | Build time   | Yes                       | Default behavior |
| Dynamic  | Request time | No                        | `cookies`, `headers`, `searchParams`, `connection`, `unstable_noStore`, `fetch` with `no-store` |

## Request Memoization

- Automatic for `fetch` GET requests in React component tree
- Same URL + options = single execution
- Does NOT apply in Route Handlers
- Lasts one render pass, then cleared

## Data Cache

```typescript
// Opt into caching
fetch('https://...', { cache: 'force-cache' })

// Opt out of caching
fetch('https://...', { cache: 'no-store' })

// Time-based revalidation (seconds)
fetch('https://...', { next: { revalidate: 3600 } })

// Tag-based caching
fetch('https://...', { next: { tags: ['posts'] } })
```

### Revalidation

| Method                | Trigger                | Router Cache Effect         |
|-----------------------|------------------------|-----------------------------|
| Time-based            | `next: { revalidate }` | Stale-while-revalidate      |
| `revalidateTag(tag)`  | Server Action / Route  | Invalidates (SA only for Router Cache) |
| `revalidatePath(path)`| Server Action / Route  | Invalidates (SA only for Router Cache) |

## Full Route Cache

- Static routes cached at build time (HTML + RSC payload)
- Invalidated by revalidating Data Cache or redeploying
- Opt out: dynamic APIs, `dynamic = 'force-dynamic'`, `revalidate = 0`

## Router Cache (Client-side)

- Layouts and loading states cached on navigation
- Pages NOT cached by default (reused on back/forward only)
- Cleared on page refresh

| Prefetch Mode                  | Dynamic Pages | Static Pages |
|--------------------------------|---------------|--------------|
| Default (`prefetch={null}`)    | Not cached    | 5 minutes    |
| Full (`prefetch={true}`)       | 5 minutes     | 5 minutes    |

### Invalidation

- `revalidatePath` / `revalidateTag` in Server Actions
- `cookies.set` / `cookies.delete` in Server Actions
- `router.refresh` (clears Router Cache, does NOT affect Data/Full Route Cache)

## API Effects on Caches

| API                          | Router | Full Route | Data   | Memo  |
|------------------------------|--------|------------|--------|-------|
| `<Link prefetch>`           | Cache  |            |        |       |
| `router.refresh`            | Reval  |            |        |       |
| `fetch` `force-cache`       |        |            | Cache  | Cache |
| `fetch` `no-store`          |        |            | Opt out|       |
| `next: { revalidate: N }`   |        | Reval      | Reval  |       |
| `next: { tags: [...] }`     |        | Cache      | Cache  |       |
| `revalidateTag`             | Reval* | Reval      | Reval  |       |
| `revalidatePath`            | Reval* | Reval      | Reval  |       |
| `cookies`                   | Reval* | Opt out    |        |       |
| `headers` / `searchParams`  |        | Opt out    |        |       |
| `React.cache`               |        |            |        | Cache |

*Only via Server Actions

## Cache Interactions

- Data Cache opt-out invalidates Full Route Cache
- Full Route Cache opt-out does NOT affect Data Cache
- `revalidatePath`/`revalidateTag` in Route Handlers do NOT invalidate Router Cache immediately

## Memoize Non-fetch Functions

```typescript
import { cache } from 'react'
import db from '@/lib/db'

export const getItem = cache(async (id: string) => {
  return await db.item.findUnique({ id })
})
```

## Quick Reference

| Task                         | Solution                                              |
|------------------------------|-------------------------------------------------------|
| Cache fetch data             | `{ cache: 'force-cache' }` or static rendering       |
| Revalidate by time           | `{ next: { revalidate: 3600 } }`                     |
| Revalidate by event          | `revalidateTag('tag')` / `revalidatePath('/')`        |
| Skip all caching             | `dynamic = 'force-dynamic'`                           |
| Dedupe DB calls              | `React.cache(fn)`                                     |
| Force static generation      | `dynamic = 'force-static'`                            |
| Disable dynamic params       | `dynamicParams = false`                               |
