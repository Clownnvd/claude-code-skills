# Edge & CDN Optimization (8%) + Memory & Resource Management (8%)

## Category 7: Edge & CDN Optimization (8%)

### Criteria (10 items, each worth 1 point)

1. **Static generation where possible** — Public pages without user data are statically generated at build time
2. **ISR for semi-static content** — Pages with infrequently changing data use `revalidate` instead of full SSR
3. **No force-dynamic on public pages** — `export const dynamic = 'force-dynamic'` only on pages requiring per-request data
4. **Lightweight middleware** — Middleware performs only routing/redirects/auth checks, no heavy computation or DB calls
5. **Static asset bypass** — Middleware matcher excludes static files (`/((?!api|_next/static|_next/image|favicon.ico).*)`)
6. **CDN-friendly cache headers** — Static assets served with long `Cache-Control` (immutable), API responses with appropriate `s-maxage`
7. **Edge-compatible middleware** — Middleware uses only Edge Runtime compatible APIs (no Node.js-only modules)
8. **No middleware on every request** — Middleware config.matcher limits which routes are processed
9. **Proper revalidation** — `revalidatePath`/`revalidateTag` used after mutations to invalidate cached pages
10. **Edge middleware for auth** — Auth checks happen at edge (middleware) not in individual page components

### Deduction Examples
- `-3` `force-dynamic` on public landing page
- `-2` Heavy database query in middleware
- `-2` No middleware matcher (runs on every request including static assets)
- `-1` Missing revalidation after data mutations

### Small App Adjustment
If app has <10 pages and <5 API routes, Edge/CDN weight (8%) redistributes: +4% to Bundle, +4% to RSC.

---

## Category 8: Memory & Resource Management (8%)

### Criteria (10 items, each worth 1 point)

1. **Database connection cleanup** — Prisma client properly managed (singleton pattern, `$disconnect` in tests/scripts)
2. **AbortController on external calls** — Fetch calls to external APIs use AbortController with timeout
3. **Bounded in-memory caches** — Any Map/Set used as cache has eviction policy (max size, TTL)
4. **Event listener cleanup** — Components with `addEventListener` also `removeEventListener` in cleanup/unmount
5. **No global mutable state** — No module-level `let` variables that accumulate data across requests
6. **Stream large responses** — Endpoints returning large data use streaming (ReadableStream) instead of buffering entire response
7. **Proper async cleanup** — `finally` blocks close resources (file handles, streams, connections)
8. **No memory leaks in closures** — setInterval/setTimeout cleared on unmount, no stale closure references
9. **Connection pool sizing** — Database connection pool sized appropriately for serverless (not too many idle connections)
10. **Request-scoped resources** — Resources allocated per-request are cleaned up after response sent

### Deduction Examples
- `-3` Growing Map/Set without eviction (memory leak over time)
- `-2` Missing AbortController on external API calls
- `-2` Database connections not properly pooled
- `-1` Event listeners not cleaned up on unmount
