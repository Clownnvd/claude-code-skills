---
name: dataflow-scoring
description: Audit data flow patterns against 10 enterprise criteria (RSC, Prisma, API routes, caching, state, types, errors, forms, DTOs, loading). Next.js App Router + React 19 + Prisma.
---

# Data Flow Scoring

Audit data flow quality against 10 weighted categories. Produces scorecard with grade (A+ to F), per-category scores, issues list with severity, and fix recommendations.

## When to Use

- Before production launch — verify data flow quality
- After major refactoring — detect regressions
- During code review — objective quality gate
- As input to `dataflow-fix` skill

## Scoring Categories

| # | Category | Weight | Key Signals |
|---|----------|--------|-------------|
| 1 | Server Component Data Fetching | 15% | RSC async, no client useEffect for initial data |
| 2 | Server/Client Composition | 10% | `"use client"` at leaf level, serializable props |
| 3 | Prisma Query Optimization | 12% | `select`, `findUnique`, indexes, singleton, pooling |
| 4 | API Route Design | 15% | Validation, auth, rate limit, CSRF, response envelope |
| 5 | State Management | 8% | Minimal client state, server-first |
| 6 | Caching & Revalidation | 10% | Cache headers, `unstable_cache`, revalidation |
| 7 | Type Safety Across Boundaries | 10% | Zod schemas, shared types, `ApiResponse<T>` |
| 8 | Error Propagation | 8% | `error.tsx`, error boundaries, safe error messages |
| 9 | Form Handling | 7% | Validation, loading states, CSRF, error display |
| 10 | Data Transformation (DTOs) | 5% | No Prisma leak, date serialization, field filtering |

## Audit Process

1. **Gather files**: pages, API routes, hooks, services, validations, types, middleware, schema.prisma
2. **Score each category** 0-10 using criteria in `references/criteria/` files
3. **Calculate weighted total** (0-100)
4. **Assign grade** using scale in `references/overview.md`
5. **List issues** with severity (CRITICAL/HIGH/MEDIUM/LOW) and affected files

## Grade Scale

| Grade | Score | Meaning |
|-------|-------|---------|
| A+ | 97-100 | Exceptional |
| A | 93-96 | Enterprise-grade |
| A- | 90-92 | Near-enterprise |
| B+ | 87-89 | Professional |
| B | 83-86 | Production-ready |
| B- | 80-82 | Acceptable |
| C+ | 77-79 | Needs improvement |
| C | 70-76 | Minimum viable |
| D | 60-69 | Below standard |
| F | <60 | Critical issues |

## Quick Reference

### Criteria (5 files covering 10 categories)
- `references/criteria/rsc-composition.md` — Server Component Fetching (15%) + Server/Client Composition (10%)
- `references/criteria/prisma-api.md` — Prisma Optimization (12%) + API Route Design (15%)
- `references/criteria/state-cache.md` — State Management (8%) + Caching (10%)
- `references/criteria/types-errors.md` — Type Safety (10%) + Error Propagation (8%)
- `references/criteria/forms-dtos.md` — Form Handling (7%) + DTOs (5%)

### Reference
- `references/overview.md` — Scoring system, output format, quality gates
- `references/scoring-workflow.md` — Step-by-step audit process
- `references/best-practices.md` — Do/Don't tables for all categories
