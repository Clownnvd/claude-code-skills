---
name: caching
description: Caching quality system. 3 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score->fix until target). Next.js 16 App Router.
---

# Caching Quality System

One skill, 3 modes. Score caching strategy, fix issues, or run the full loop.

## Modes

| Mode | Use When | Workflow |
|------|----------|----------|
| **score** | Pre-launch audit, after adding/changing routes, after static/dynamic conversion | Gather files -> score 10 categories -> weighted total -> grade + issues |
| **fix** | Scorecard has issues, score below target, CRITICAL/HIGH items found | Parse scorecard -> prioritize by severity*weight -> apply fixes -> verify |
| **loop** | Want hands-off score->fix cycle until target grade reached | Score -> fix -> re-score -> repeat (max 5 iterations, stop on plateau) |

## Mode: Score

Audit caching strategy against 10 weighted categories (0-100 scale, A+ to F grade).

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

### Grade Scale

| Grade | Score | Grade | Score | Grade | Score |
|-------|-------|-------|-------|-------|-------|
| A+ | 97-100 | B+ | 87-89 | C+ | 77-79 |
| A | 93-96 | B | 83-86 | C | 70-76 |
| A- | 90-92 | B- | 80-82 | D | 60-69 |
| | | | | F | <60 |

### Score Workflow
1. Gather files: API routes, pages, proxy, layout, lib/auth, services, hooks
2. Score each category 0-10 using `references/scoring/criteria/` files
3. Calculate weighted total, assign grade
4. List issues with severity (CRITICAL/HIGH/MEDIUM/LOW) and affected files

## Mode: Fix

Parse scorecard, prioritize by severity * weight, apply fixes, verify.

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or data leak | Fix immediately -- blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next -- moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

### Fix Category -> Pattern Reference

| Scorecard Category | Fix Pattern File |
|-------------------|------------------|
| Cache-Control Headers, Revalidation Strategy | `references/fix/fix-patterns/headers-revalidation.md` |
| Static/Dynamic, ISR | `references/fix/fix-patterns/static-dynamic-isr.md` |
| React cache(), `"use cache"` | `references/fix/fix-patterns/react-cache-use-cache.md` |
| CDN, Request Dedup | `references/fix/fix-patterns/cdn-dedup.md` |
| Proxy, Monitoring | `references/fix/fix-patterns/proxy-monitoring.md` |

### Fix Workflow
Load `references/fix/implementation-workflow.md` for 6-step process: parse -> prioritize -> fix -> verify -> re-score.

## Mode: Loop

Auto-iterate score -> fix until target grade reached.
- Default target: B+ (production), A- (enterprise)
- Max 5 iterations
- Stop on plateau (score unchanged after full fix cycle)
- Each iteration: full score -> prioritized fix -> re-score

## Quick Reference -- All Files

### Scoring
- `references/scoring/overview.md` -- Scoring system, output format, quality gates
- `references/scoring/best-practices.md` -- Do/Don't tables for all categories
- `references/scoring/scoring-workflow.md` -- Step-by-step audit process
- `references/scoring/criteria/headers-revalidation.md` -- Cache Headers (15%) + Revalidation (15%)
- `references/scoring/criteria/static-dynamic-isr.md` -- Static/Dynamic (12%) + ISR (8%)
- `references/scoring/criteria/react-cache-use-cache.md` -- React cache() (10%) + "use cache" (10%)
- `references/scoring/criteria/cdn-dedup.md` -- CDN (8%) + Request Dedup (7%)
- `references/scoring/criteria/proxy-monitoring.md` -- Proxy (7%) + Monitoring (8%)

### Fix
- `references/fix/overview.md` -- How fix works, priority order, score targets
- `references/fix/best-practices.md` -- Fix discipline, safe vs dangerous changes
- `references/fix/implementation-workflow.md` -- 6-step process, priority matrix
- `references/fix/verification.md` -- Post-fix checklist, re-scoring protocol, loop mode
- `references/fix/fix-patterns/headers-revalidation.md` -- Cache headers, revalidation paths
- `references/fix/fix-patterns/static-dynamic-isr.md` -- Static page conversion, ISR config
- `references/fix/fix-patterns/react-cache-use-cache.md` -- cache() dedup, "use cache" directive
- `references/fix/fix-patterns/cdn-dedup.md` -- CDN headers, Promise.all dedup
- `references/fix/fix-patterns/proxy-monitoring.md` -- Proxy optimization, debug headers

## Output Templates
- Score: `assets/templates/scorecard.md.template`
- Fix: `assets/templates/fix-report.md.template`
