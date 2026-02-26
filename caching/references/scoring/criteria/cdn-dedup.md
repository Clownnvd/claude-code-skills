# Criteria: CDN & Edge Caching (8%) + Request Deduplication (7%)

## 7. CDN & Edge Caching (8%)

### Score 9-10: Enterprise-grade
- Static assets served with long-lived cache + immutable
- `s-maxage` on CDN-cacheable public API responses
- `Vary` header on responses that change by auth/locale
- Public pages cacheable at CDN layer
- API responses for anonymous users CDN-cacheable
- No authenticated data leaked to CDN cache

### Score 7-8: Production-ready
- Static assets properly cached
- Public pages CDN-friendly
- Some missing `Vary` headers
- Auth data not leaked

### Score 5-6: Minimum
- Basic CDN caching via framework defaults
- No explicit CDN configuration
- Static assets cached but no strategy for dynamic content

### Score 3-4: Below minimum
- No CDN awareness
- All responses bypass CDN
- Static assets not cached properly

### N/A Adjustment
If deploying without CDN (dev/staging):
- Score based on CDN-readiness (headers, vary, no auth leak)
- Redistribute to Headers (18%) if truly N/A

### Checklist
- [ ] Static assets: `immutable, max-age=31536000`
- [ ] Public API: `s-maxage` where appropriate
- [ ] `Vary` on auth/locale-dependent responses
- [ ] No auth data in CDN cache

## 8. Request Deduplication (7%)

### Score 9-10: Enterprise-grade
- `Promise.all` for parallel independent fetches in Server Components
- No sequential awaits for independent data (no waterfalls)
- Shared data loaded once in layout, passed down via props/context
- No duplicate `fetch()` calls to same endpoint in component tree
- React's built-in fetch dedup leveraged (same URL = one request)

### Score 7-8: Production-ready
- `Promise.all` used in most places with parallel data needs
- Some sequential awaits but non-critical
- No obvious duplicate fetches

### Score 5-6: Minimum
- Some parallel fetches, some sequential
- Layout and page fetch same data separately
- No systematic dedup strategy

### Score 3-4: Below minimum
- Sequential awaits everywhere (waterfall pattern)
- Same data fetched multiple times in same request
- No `Promise.all` usage

### Checklist
- [ ] `Promise.all` for independent parallel fetches
- [ ] No sequential awaits for unrelated data
- [ ] No duplicate fetches in component tree
- [ ] Layout data shared via props (not re-fetched)
