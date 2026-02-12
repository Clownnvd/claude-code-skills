---
name: scalability-scoring
description: Audit scalability & performance against 10 enterprise criteria (bundle size, images, RSC, DB queries, API perf, client rendering, edge/CDN, memory, concurrency, monitoring). Next.js App Router.
---

# Scalability & Performance Scoring

Audit scalability and performance against 10 weighted categories. Produces scorecard with grade (A+ to F), per-category scores, issues list with severity, and fix recommendations.

## When to Use

- Before production launch — verify performance posture
- After adding new pages, components, or API routes
- When page load times or bundle size increase
- As input to `scalability-fix` skill

## Scoring Categories

| # | Category | Weight | Key Signals |
|---|----------|--------|-------------|
| 1 | Bundle Size & Code Splitting | 15% | Dynamic imports, tree shaking, no barrel re-exports, lazy components |
| 2 | Image & Asset Optimization | 12% | next/image, WebP/AVIF, lazy loading, responsive sizes |
| 3 | Server Component Architecture | 12% | RSC by default, minimal 'use client', streaming, Suspense |
| 4 | Database Query Performance | 12% | No N+1, connection pooling, indexed queries, select fields |
| 5 | API Response Performance | 10% | Small payloads, pagination, no over-fetching, compression |
| 6 | Client-Side Performance | 10% | Minimal re-renders, memoization where needed, no layout thrash |
| 7 | Edge & CDN Optimization | 8% | Static generation, ISR, proxy configuration, CDN-friendly headers |
| 8 | Memory & Resource Management | 8% | No leaks, connection cleanup, bounded caches, AbortController |
| 9 | Concurrent & Parallel Processing | 7% | Promise.all for independent fetches, streaming responses |
| 10 | Performance Monitoring & Budgets | 6% | Web Vitals tracking, bundle budget, lighthouse CI |

## Audit Process

1. **Gather files**: pages, components, API routes, proxy, DB queries, package.json, next.config
2. **Score each category** 0-10 using criteria in `references/criteria/` files
3. **Calculate weighted total** (0-100)
4. **Assign grade** using scale below
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
- `references/criteria/bundle-images.md` — Bundle Size (15%) + Images (12%)
- `references/criteria/rsc-dbperf.md` — Server Components (12%) + DB Perf (12%)
- `references/criteria/api-client.md` — API Perf (10%) + Client Perf (10%)
- `references/criteria/edge-memory.md` — Edge/CDN (8%) + Memory (8%)
- `references/criteria/concurrency-monitoring.md` — Concurrency (7%) + Monitoring (6%)

### Reference
- `references/overview.md` — Scoring system, output format, files to audit
- `references/scoring-workflow.md` — Step-by-step audit process
- `references/best-practices.md` — Do/Don't tables for all categories

## Output Templates

Use `assets/templates/scorecard.md.template` as the output format when generating scorecards. Fill `{{VARIABLE}}` placeholders with actual values.
