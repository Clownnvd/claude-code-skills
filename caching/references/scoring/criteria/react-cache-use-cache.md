# Criteria: React cache() Deduplication (10%) + `"use cache"` Directive (10%)

## 5. React `cache()` Deduplication (10%)

### Score 9-10: Enterprise-grade
- `cache()` wraps `getServerSession` / auth lookup (most called function)
- No duplicate DB lookups within single request
- Shared data loader functions use `cache()` for request-level dedup
- `cache()` used on functions called from multiple Server Components in same tree
- Per-request scope understood (not cross-request cache)

### Score 7-8: Production-ready
- `cache()` on auth/session function
- Most frequently called functions deduplicated
- Some duplicate calls exist but non-critical

### Score 5-6: Minimum
- No `cache()` usage but auth called multiple times per request
- Duplicate DB lookups exist
- No request-level deduplication strategy

### Score 3-4: Below minimum
- Multiple identical DB queries per request
- Auth checked separately in layout + page + component
- No awareness of request-level caching

### Checklist
- [ ] `cache()` on getServerSession / auth lookup
- [ ] No duplicate DB calls per request
- [ ] Shared loaders use `cache()`
- [ ] Per-request scope (not long-lived cache)

## 6. `"use cache"` Directive (10%)

### Score 9-10: Enterprise-grade
- `"use cache"` directive on expensive or frequently-read async functions
- `cacheTag()` values are meaningful and specific (e.g., `"products"`, `"user-123"`)
- `revalidateTag` called after writes to invalidate cached queries
- `cacheLife()` configured appropriately per function (e.g., `'hours'`, `'days'`)
- Auth-dependent data NOT cached with `"use cache"`
- Cache scope is clear (function-level, not module-level for user data)

### Score 7-8: Production-ready
- Some use of `"use cache"` for expensive queries
- Tags exist but not always invalidated
- Most appropriate queries are cached

### Score 5-6: Minimum
- No `"use cache"` usage
- All queries hit DB every time
- No query-level caching strategy

### Score 3-4: Below minimum
- N/A or no caching, AND expensive queries exist
- Repeated full-table scans

### N/A Adjustment
If the app is small (< 10 queries) and all are user-specific:
- `"use cache"` may not be applicable
- Score based on awareness: does the code have a place to add it?
- If truly N/A: redistribute 10% to ReactCache (15%) + Headers (20%)

### Checklist
- [ ] `"use cache"` on expensive queries
- [ ] Meaningful `cacheTag()` per cached function
- [ ] `revalidateTag` after mutations
- [ ] `cacheLife()` configured per function
- [ ] No auth data in `"use cache"` functions
