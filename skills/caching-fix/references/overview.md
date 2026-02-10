# Caching Strategy Fix — Overview

## Purpose
Systematically fix caching issues identified by caching-scoring. Prioritize by impact (severity * weight), apply fixes, verify, re-score.

## Priority Order (fix in this order)
1. **Cache-Control Headers (15%)** — highest weight, security-critical
2. **Revalidation Strategy (15%)** — highest weight, data freshness
3. **Static/Dynamic Classification (12%)** — high weight, performance
4. **React cache() (10%)** — medium weight, request efficiency
5. **`"use cache"` Directive (10%)** — medium weight, query performance
6. **Cache Monitoring (8%)** — medium weight, observability
7. **CDN & Edge (8%)** — medium weight, distribution
8. **ISR (8%)** — medium weight, content freshness
9. **Request Dedup (7%)** — lower weight, efficiency
10. **Proxy (7%)** — lower weight, request pipeline

## Safe vs Dangerous Changes

### Safe (low risk)
- Adding `NO_CACHE_HEADERS` to API responses
- Adding `export const dynamic = "force-dynamic"` to API routes
- Adding `revalidatePath` after mutations
- Wrapping function with `cache()`
- Adding `Vary` headers to responses
- Moving auth check from server to client in header

### Dangerous (verify carefully)
- Removing `force-dynamic` (may serve stale auth data)
- Adding `"use cache"` to auth-dependent queries
- Changing proxy matcher config
- Adding ISR to pages that need real-time data
- CDN configuration changes (may cache private data)

## Score Targets

| Target | Score | When |
|--------|-------|------|
| Minimum viable | 70+ (C) | Internal/prototype |
| Production-ready | 80+ (B-) | Public launch |
| Professional | 85+ (B+) | Premium product |
| Enterprise | 90+ (A-) | Enterprise/showcase |

## Loop Mode
When "fix until 100" requested:
1. Parse scorecard -> fix remaining -> verify -> re-score
2. Max 5 iterations
3. Stop if delta = 0 for 2 consecutive iterations
4. Final output: full before/after comparison
