# Criteria: Proxy Caching (7%) + Cache Monitoring & Debug (8%)

## 9. Proxy Caching (7%)

### Score 9-10: Enterprise-grade
- Proxy is lightweight (no DB queries, no heavy computation)
- Static assets (`_next/static`, images, fonts) bypass proxy
- Auth check in proxy uses JWT/cookie validation (not DB lookup)
- `matcher` config excludes static files and public assets
- Proxy returns early for public routes
- No `fetch()` calls in proxy

### Score 7-8: Production-ready
- Proxy is mostly lightweight
- Static assets mostly bypassed
- Auth check is cookie-based
- Some unnecessary proxy execution

### Score 5-6: Minimum
- Proxy runs on all routes including static
- Some heavy operations in proxy
- No matcher config optimization

### Score 3-4: Below minimum
- DB queries in proxy
- Proxy runs on every request (no matcher)
- Heavy auth lookup per request
- External API calls in proxy

### Checklist
- [ ] No DB queries in proxy
- [ ] Static assets excluded via `matcher`
- [ ] Auth check is cookie/JWT based (no DB)
- [ ] Early return for public routes
- [ ] No external API calls in proxy

## 10. Cache Monitoring & Debug (8%)

### Score 9-10: Enterprise-grade
- Cache hit/miss observable in development
- `x-cache-status` or similar debug header in dev mode
- Error logging when cache operations fail
- Revalidation events logged (which path/tag, when)
- Cache behavior documented for team
- Build output shows static vs dynamic route classification

### Score 7-8: Production-ready
- Some cache observability exists
- Errors logged for cache failures
- Build output reviewed for static/dynamic
- Dev tools show caching behavior

### Score 5-6: Minimum
- Limited cache visibility
- No debug headers
- Build output not reviewed
- Cache behavior is trial-and-error

### Score 3-4: Below minimum
- Zero cache observability
- No logging of cache events
- Unknown which routes are static/dynamic
- Cache bugs discovered only in production

### N/A Adjustment
For small projects without complex caching:
- Score based on build output review + basic logging
- Minimum: check `pnpm build` output for static/dynamic routes

### Checklist
- [ ] Cache hit/miss visible in dev
- [ ] Error logging for cache failures
- [ ] Build output reviewed (static vs dynamic)
- [ ] Revalidation events logged
- [ ] Cache strategy documented
