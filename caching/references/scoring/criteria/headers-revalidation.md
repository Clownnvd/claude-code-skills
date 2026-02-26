# Criteria: Cache-Control Headers (15%) + Revalidation Strategy (15%)

## 1. Cache-Control Headers (15%)

### Score 9-10: Enterprise-grade
- ALL authenticated API responses include `Cache-Control: private, no-store`
- Centralized `NO_CACHE_HEADERS` constant used everywhere (not inline strings)
- Static assets (images, fonts, JS/CSS) have immutable cache headers
- Public API responses (health, ready) have appropriate `public` cache
- `Vary` header set correctly on responses that vary by auth/cookie
- `export const dynamic = "force-dynamic"` explicit on ALL API routes
- No API route missing cache headers (zero gaps)

### Score 7-8: Production-ready
- Most authenticated responses have no-cache headers
- Central constant exists but not used everywhere
- Some API routes missing explicit cache-control
- `force-dynamic` on most API routes

### Score 5-6: Minimum
- Some cache headers present
- Mix of inline and centralized headers
- Several API routes missing cache-control entirely
- No `Vary` headers

### Score 3-4: Below minimum
- No cache headers on authenticated responses (proxy can cache user data!)
- No centralized cache header utility
- `force-dynamic` missing on auth-dependent routes

### Checklist
- [ ] `NO_CACHE_HEADERS` on every authenticated API response
- [ ] Central `NO_CACHE_HEADERS` constant (not inline)
- [ ] `export const dynamic = "force-dynamic"` on all API routes
- [ ] Static assets have immutable headers
- [ ] Public endpoints have appropriate public cache
- [ ] `Vary` header on responses varying by auth

## 2. Revalidation Strategy (15%)

### Score 9-10: Enterprise-grade
- `revalidatePath()` called after EVERY Prisma mutation (create/update/delete)
- Webhook handlers revalidate affected pages
- Server Actions revalidate the form's source page
- `revalidateTag()` for targeted invalidation of cached queries
- No mutation path that forgets revalidation
- Revalidation targets are specific (not `"/"`)

### Score 7-8: Production-ready
- Most mutations trigger revalidation
- Webhook handlers revalidate
- Some mutations missing revalidation
- `revalidatePath` used but not `revalidateTag`

### Score 5-6: Minimum
- Some mutations have revalidation
- Others rely on client-side refetch
- No tag-based invalidation

### Score 3-4: Below minimum
- No revalidation after mutations
- Client-side refetch is the only strategy
- Stale data served after writes

### Checklist
- [ ] `revalidatePath` after every Prisma write
- [ ] Webhook handlers call `revalidatePath`
- [ ] Server Actions revalidate source page
- [ ] `revalidateTag` for cached query invalidation
- [ ] No mutation misses revalidation
- [ ] Revalidation targets are specific paths
