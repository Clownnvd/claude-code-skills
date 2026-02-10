---
name: caching-fix
description: Take caching-scoring feedback (scorecard + issues list) and implement all fixes systematically. Prioritize by severity, apply code changes, verify, and re-score. Next.js App Router patterns.
---

# Caching Strategy Fix

Take a caching-scoring scorecard and systematically implement all fixes. Prioritize by severity * weight, apply code changes, verify, and re-score.

## When to Use

- After running `caching-scoring` and receiving a scorecard with issues
- When caching scores below target (< B+ for production, < A- for enterprise)
- To systematically fix all CRITICAL -> HIGH -> MEDIUM -> LOW items
- Before deploying code that failed a caching quality gate

## Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or data leak | Fix immediately — blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next — moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

## Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Cache-Control Headers, Revalidation Strategy | `references/fix-patterns/headers-revalidation.md` |
| Static/Dynamic, ISR | `references/fix-patterns/static-dynamic-isr.md` |
| React cache(), `"use cache"` | `references/fix-patterns/react-cache-use-cache.md` |
| CDN, Request Dedup | `references/fix-patterns/cdn-dedup.md` |
| Proxy, Monitoring | `references/fix-patterns/proxy-monitoring.md` |

## Implementation

Load `references/implementation-workflow.md` for step-by-step process (parse -> prioritize -> fix -> verify -> re-score).

## Quick Reference

### Overview & Best Practices
- `references/overview.md` — How caching-fix works, priority order, score targets
- `references/best-practices.md` — Fix discipline, safe vs dangerous changes

### Workflow
- `references/implementation-workflow.md` — 6-step process, priority matrix
- `references/verification.md` — Post-fix checklist, re-scoring protocol, loop mode

### Fix Patterns (5 files covering 10 categories)
- `references/fix-patterns/headers-revalidation.md` — Cache headers, revalidation paths
- `references/fix-patterns/static-dynamic-isr.md` — Static page conversion, ISR config
- `references/fix-patterns/react-cache-use-cache.md` — cache() dedup, `"use cache"` directive
- `references/fix-patterns/cdn-dedup.md` — CDN headers, Promise.all dedup
- `references/fix-patterns/proxy-monitoring.md` — Proxy optimization, debug headers
