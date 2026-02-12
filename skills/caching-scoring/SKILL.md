---
name: caching-scoring
description: Audit caching strategy against 10 enterprise criteria (cache headers, revalidation, static/dynamic, ISR, React cache, "use cache", CDN, request dedup, proxy, monitoring). Next.js 16 App Router.
---

# Caching Strategy Scoring

Audit caching quality against 10 weighted categories. Produces scorecard with grade (A+ to F), per-category scores, issues list with severity, and fix recommendations.

## When to Use

- Before production launch — verify caching strategy
- After adding/changing API routes — check cache headers
- After converting pages to/from dynamic — verify ISR/static
- As input to `caching-fix` skill

## Scoring Categories

| # | Category | Weight | Key Signals |
|---|----------|--------|-------------|
| 1 | Cache-Control Headers | 15% | `NO_CACHE_HEADERS` on auth responses, public cache for static assets |
| 2 | Revalidation Strategy | 15% | `revalidatePath`/`revalidateTag` after every mutation |
| 3 | Static vs Dynamic Classification | 12% | `force-dynamic` only where needed, static pages stay static |
| 4 | ISR Configuration | 8% | `revalidate` on public pages, stale-while-revalidate |
| 5 | React `cache()` Deduplication | 10% | `cache()` on session/auth, no duplicate DB calls per request |
| 6 | `"use cache"` Directive | 10% | Tag-based cache for expensive queries, proper invalidation |
| 7 | CDN & Edge Caching | 8% | `stale-while-revalidate`, `s-maxage`, Vercel edge config |
| 8 | Request Deduplication | 7% | No duplicate fetches, `Promise.all` for parallel data |
| 9 | Proxy Caching | 7% | No heavy operations in proxy, static asset bypass |
| 10 | Cache Monitoring & Debug | 8% | `x-cache` headers in dev, cache hit/miss observability |

## Audit Process

1. **Gather files**: API routes, pages, proxy, layout, lib/auth, services, hooks
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
- `references/criteria/headers-revalidation.md` — Cache Headers (15%) + Revalidation (15%)
- `references/criteria/static-dynamic-isr.md` — Static/Dynamic (12%) + ISR (8%)
- `references/criteria/react-cache-use-cache.md` — React cache() (10%) + "use cache" (10%)
- `references/criteria/cdn-dedup.md` — CDN (8%) + Request Dedup (7%)
- `references/criteria/proxy-monitoring.md` — Proxy (7%) + Monitoring (8%)

### Reference
- `references/overview.md` — Scoring system, output format, quality gates
- `references/scoring-workflow.md` — Step-by-step audit process
- `references/best-practices.md` — Do/Don't tables for all categories

## Output Templates

Use `assets/templates/scorecard.md.template` as the output format when generating scorecards. Fill `{{VARIABLE}}` placeholders with actual values.
