# Caching Best Practices

## 1. Cache-Control Headers

| Do | Don't |
|----|-------|
| `Cache-Control: private, no-store` on auth responses | Allow proxy to cache user data |
| `Cache-Control: public, max-age=31536000, immutable` on static assets | No cache headers on any response |
| `stale-while-revalidate` on semi-static data | `no-cache` everywhere (defeats purpose) |
| Centralized `NO_CACHE_HEADERS` constant | Inline header strings per route |

## 2. Revalidation Strategy

| Do | Don't |
|----|-------|
| `revalidatePath()` after every Prisma mutation | Rely on client refetch after mutation |
| `revalidateTag()` for targeted invalidation | `revalidatePath("/")` invalidating everything |
| Revalidate in webhook handlers | Forget revalidation in background jobs |
| Revalidate the specific path affected | Over-revalidate unrelated pages |

## 3. Static vs Dynamic

| Do | Don't |
|----|-------|
| Keep landing/marketing pages static | `force-dynamic` on public pages |
| Use client-side auth check for header UI | Server session read making page dynamic |
| `export const dynamic = "force-dynamic"` on API routes | Implicit dynamic via cookies() |
| Static generation for blog/docs | Dynamic rendering for SEO pages |

## 4. ISR Configuration

| Do | Don't |
|----|-------|
| `revalidate = 3600` on public content pages | No revalidation (stale forever or always fresh) |
| On-demand revalidation via webhook | Only time-based revalidation |
| `stale-while-revalidate` for good UX | Full page blocking on revalidation |

## 5. React cache()

| Do | Don't |
|----|-------|
| `cache()` on `getServerSession` | Multiple session DB lookups per request |
| `cache()` on shared data loaders | `cache()` on one-off queries |
| Single `cache()` per unique data source | Nested `cache()` wrappers |

## 6. unstable_cache

| Do | Don't |
|----|-------|
| Tag-based caching for product listings | `unstable_cache` on user-specific data |
| `revalidateTag` after writes | No invalidation strategy |
| Short TTL for semi-dynamic data | Long TTL without invalidation |

## 7. CDN & Edge

| Do | Don't |
|----|-------|
| `s-maxage` for CDN-cacheable responses | CDN caching authenticated data |
| Edge middleware for routing/redirects | Heavy DB queries in middleware |
| Static assets served from CDN | API responses through CDN without vary headers |

## 8. Request Deduplication

| Do | Don't |
|----|-------|
| `Promise.all` for parallel fetches | Sequential awaits for independent data |
| React dedup for same fetch URL | Multiple `fetch()` to same endpoint in tree |
| Shared data loader functions | Each component fetching its own data |

## 9. Middleware Caching

| Do | Don't |
|----|-------|
| Lightweight auth check (JWT verify) | Full DB session lookup in middleware |
| Skip middleware for static assets | Middleware runs on every request |
| Return early for public routes | Complex logic before route matching |

## 10. Cache Monitoring

| Do | Don't |
|----|-------|
| Log cache hit/miss in development | No visibility into cache behavior |
| `x-cache-status` header in dev mode | Cache debugging only in production |
| Monitor cache invalidation events | Silent invalidation failures |
