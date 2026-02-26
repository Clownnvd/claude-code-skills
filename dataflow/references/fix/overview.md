# Data Flow Fix — Overview

## Purpose
Systematically fix data flow issues identified by dataflow-scoring. Prioritize by impact (severity * weight), apply fixes, verify, re-score.

## Priority Order (fix in this order)
1. **API Route Design (15%)** — most weight, security-critical
2. **Server Component Fetching (15%)** — most weight, architecture
3. **Prisma Optimization (12%)** — high weight, performance
4. **Caching (10%)** — medium weight, performance
5. **Type Safety (10%)** — medium weight, correctness
6. **Server/Client Composition (10%)** — medium weight, bundle size
7. **Error Propagation (8%)** — lower weight, resilience
8. **State Management (8%)** — lower weight, UX
9. **Form Handling (7%)** — lower weight, UX
10. **DTOs (5%)** — lowest weight, code quality

## Safe vs Dangerous Changes

### Safe (low risk)
- Adding `select` to Prisma queries
- Adding `loading.tsx` / `error.tsx` files
- Adding `NO_CACHE_HEADERS` to API responses
- Adding Zod validation to API routes
- Moving `"use client"` down the component tree
- Adding `@@index` to Prisma schema
- Adding `.toISOString()` to date fields

### Dangerous (verify carefully)
- Converting client components to server components (may break interactivity)
- Changing API response shapes (breaks existing clients)
- Adding `force-dynamic` or removing it (changes caching behavior)
- Modifying Prisma schema (requires migration)
- Changing form submission pattern (API route <-> Server Action)

## Score Targets

| Target | Score | When |
|--------|-------|------|
| Minimum viable | 73+ (C) | Internal/prototype |
| Production-ready | 87+ (B+) | Public launch |
| Enterprise | 90+ (A-) | Enterprise/showcase |

## Loop Mode
When "fix until 100" requested:
1. Parse scorecard -> fix remaining -> verify -> re-score
2. Max 5 iterations
3. Stop if delta = 0 for 2 consecutive iterations
4. Final output: full before/after comparison
