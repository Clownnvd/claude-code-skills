# Scalability Best Practices

## 1. Bundle Size & Code Splitting

| Do | Don't |
|----|-------|
| Dynamic import heavy libraries (`dynamic()`) | Import entire libraries at top level |
| Tree-shake with named imports | Barrel re-exports (`export * from`) |
| Lazy load below-fold components | Load everything upfront |
| Use `next/dynamic` for client-only libs | Import client libs in Server Components |
| Keep page JS under 100KB gzipped | Ignore bundle size growth |

## 2. Image & Asset Optimization

| Do | Don't |
|----|-------|
| Use `next/image` for all images | Raw `<img>` tags |
| Set explicit `width`/`height` | Missing dimensions (CLS) |
| Use `priority` for above-fold images | Lazy-load hero images |
| Serve WebP/AVIF via Next.js | Serve unoptimized PNG/JPG |
| Use `sizes` prop for responsive | Fixed-size images on all screens |

## 3. Server Component Architecture

| Do | Don't |
|----|-------|
| Default to Server Components | Add `'use client'` everywhere |
| Push `'use client'` to leaf nodes | Mark entire pages as client |
| Use Suspense for streaming | Block render on data fetch |
| Pass serializable props to client | Pass functions to client components |
| Colocate data fetching with display | Fetch in parent, prop-drill to child |

## 4. Database Query Performance

| Do | Don't |
|----|-------|
| Use `select` to limit fields | Fetch entire rows |
| Add `@@index` on query fields | Query without indexes |
| Use connection pooling (pgbouncer) | New connection per query |
| Batch related queries (`Promise.all`) | Sequential dependent queries |
| Use `findUnique` for PK lookups | `findFirst` for unique fields |

## 5. API Response Performance

| Do | Don't |
|----|-------|
| Return only needed fields | Return full database objects |
| Paginate list endpoints | Return unbounded arrays |
| Compress responses (gzip/brotli) | Uncompressed large payloads |
| Use appropriate HTTP status codes | Always 200 with error in body |
| Set response size limits | Accept unlimited request bodies |

## 6. Client-Side Performance

| Do | Don't |
|----|-------|
| Minimize `'use client'` surface area | Wrap entire pages in client boundary |
| Use `React.memo` for expensive renders | Memoize everything (over-optimization) |
| Debounce frequent events | Direct state updates on every keystroke |
| Use CSS for animations | JS-driven layout animations |
| Avoid layout thrashing | Read+write DOM in loops |

## 7. Edge & CDN Optimization

| Do | Don't |
|----|-------|
| Static generate where possible | `force-dynamic` on public pages |
| Use ISR for semi-static content | Full SSR for unchanging content |
| Keep proxy lightweight | Heavy computation in proxy |
| Bypass proxy for static assets | Process every request through proxy |
| Set `s-maxage` for CDN caching | No CDN cache headers |

## 8. Memory & Resource Management

| Do | Don't |
|----|-------|
| Close DB connections in cleanup | Leak connection handles |
| Use AbortController for timeouts | Unbounded external requests |
| Bound in-memory caches | Unlimited Map/Set growth |
| Clean up event listeners | Add listeners without removal |
| Use streaming for large responses | Buffer entire response in memory |

## 9. Concurrent & Parallel Processing

| Do | Don't |
|----|-------|
| `Promise.all` for independent fetches | Sequential `await` chains |
| Streaming responses for large data | Wait for all data before responding |
| Parallel DB queries where possible | Sequential queries that could be parallel |
| Use `Promise.allSettled` when partial OK | `Promise.all` when one failure is acceptable |

## 10. Performance Monitoring & Budgets

| Do | Don't |
|----|-------|
| Track Web Vitals (LCP, FID, CLS) | No performance metrics |
| Set bundle size budgets | Ignore bundle growth |
| Monitor API response times | No latency tracking |
| Profile slow pages | Guess at bottlenecks |
| Lighthouse CI in pipeline | Manual-only performance testing |
