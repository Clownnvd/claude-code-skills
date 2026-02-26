# Scalability Review Workflow

## Process

1. **Read** — Load target file(s), identify performance-relevant patterns
2. **Classify** — Which scalability categories apply:
   - Component → Bundle Size, RSC Architecture, Client Perf, Memory
   - API route → API Response Perf, DB Query Perf, Concurrent Processing
   - Page → All categories may apply
   - Config → Edge/CDN, Monitoring, Bundle Size
3. **Score** — Rate each applicable category 0-10
4. **Annotate** — Cite line numbers and issues
5. **Suggest** — Concrete performance fixes
6. **Summarize** — Score, priorities, quick wins

## Common Scalability Issues

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | Barrel re-exports in component imports | Bundle Size | CRITICAL |
| 2 | No dynamic import for heavy lib (Recharts) | Bundle Size | HIGH |
| 3 | N+1 database queries | DB Query Perf | CRITICAL |
| 4 | Large images without next/image | Image Optimization | HIGH |
| 5 | "use client" on data-fetching component | RSC Architecture | HIGH |
| 6 | No pagination on list endpoints | API Response Perf | HIGH |
| 7 | Memory leak (no cleanup in useEffect) | Memory Management | MEDIUM |
| 8 | Sequential fetches that could be parallel | Concurrent Processing | MEDIUM |
