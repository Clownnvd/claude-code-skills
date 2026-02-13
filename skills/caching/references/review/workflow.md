# Caching Review Workflow

## Process

1. **Read** — Load target file(s), identify caching-related code (headers, revalidation, directives)
2. **Classify** — Determine which caching categories apply:
   - API route → Headers, Revalidation, Dynamic classification, Monitoring
   - Page component → Static/Dynamic, ISR, "use cache", CDN
   - Data loader → cache(), Request Dedup, Revalidation
   - Proxy/middleware → Proxy, CDN, Headers
3. **Score** — Rate each applicable category 0-10
4. **Annotate** — Cite line numbers, explain issues
5. **Suggest** — Concrete fixes
6. **Summarize** — Score, priorities, quick wins

## Common Caching Issues

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | Auth response cached | Cache-Control Headers | CRITICAL |
| 2 | No revalidation after mutation | Revalidation Strategy | CRITICAL |
| 3 | Missing `dynamic` export | Static/Dynamic | HIGH |
| 4 | No `cache()` on repeated lookups | React cache() | MEDIUM |
| 5 | Missing `Vary` header | CDN & Edge | MEDIUM |
| 6 | No cache monitoring | Cache Monitoring | LOW |
