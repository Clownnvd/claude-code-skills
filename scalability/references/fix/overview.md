# Scalability Fix — Overview

## Purpose
Systematically implement all fixes from a scalability-scoring scorecard. Prioritize by severity * weight to maximize score improvement per fix.

## Score Targets

| Context | Target | Action |
|---------|--------|--------|
| Production | >= 87 (B+) | Fix CRITICAL + HIGH |
| Enterprise | >= 90 (A-) | Fix all CRITICAL + HIGH + MEDIUM |
| Perfect | 100 (A+) | Fix everything including LOW |

## Priority Matrix

Impact = severity_weight * category_weight

| Severity | Bundle(15) | Images(12) | RSC(12) | DB(12) | API(10) | Client(10) | Edge(8) | Memory(8) | Concur(7) | Monitor(6) |
|----------|-----------|-----------|---------|--------|---------|-----------|---------|-----------|-----------|-----------|
| CRITICAL | 45 | 36 | 36 | 36 | 30 | 30 | 24 | 24 | 21 | 18 |
| HIGH | 30 | 24 | 24 | 24 | 20 | 20 | 16 | 16 | 14 | 12 |
| MEDIUM | 15 | 12 | 12 | 12 | 10 | 10 | 8 | 8 | 7 | 6 |

Fix highest impact number first.

## Safe vs Dangerous Changes

### Safe (apply freely)
- Adding `next/dynamic` for code splitting
- Adding `select` to Prisma queries
- Adding `@@index` to schema
- Adding Suspense boundaries
- Adding `priority` to above-fold images
- Adding `sizes` to responsive images
- Adding Promise.all for independent fetches

### Dangerous (test thoroughly)
- Changing page from client to server component (may break interactivity)
- Adding ISR/revalidation (may serve stale data)
- Modifying proxy matcher (may break auth)
- Changing database connection pool size
- Adding streaming to API responses (may break existing consumers)

## Loop Mode
After applying all fixes: `tsc` + `pnpm test` + re-run `scalability-scoring`. If score < target, repeat with remaining issues. Max 5 iterations.
