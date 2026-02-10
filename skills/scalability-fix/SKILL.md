---
name: scalability-fix
description: Take scalability-scoring feedback and implement all fixes systematically. Prioritize by severity, apply code changes, verify, and re-score. Next.js App Router patterns.
---

# Scalability & Performance Fix

Take a scalability-scoring scorecard and systematically implement all fixes. Prioritize by severity * weight, apply code changes, verify, and re-score.

## When to Use

- After running `scalability-scoring` and receiving a scorecard with issues
- When scalability scores below target (< B+ for production, < A- for enterprise)
- To systematically fix all CRITICAL -> HIGH -> MEDIUM -> LOW items
- Before deploying code that failed a performance quality gate

## Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or user-visible perf | Fix immediately — blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next — moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

## Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Bundle Size, Image Optimization | `references/fix-patterns/bundle-images.md` |
| RSC Architecture, DB Performance | `references/fix-patterns/rsc-dbperf.md` |
| API Performance, Client Performance | `references/fix-patterns/api-client.md` |
| Edge/CDN, Memory Management | `references/fix-patterns/edge-memory.md` |
| Concurrency, Monitoring | `references/fix-patterns/concurrency-monitoring.md` |

## Implementation

Load `references/implementation-workflow.md` for step-by-step process (parse -> prioritize -> fix -> verify -> re-score).

## Quick Reference

### Overview & Best Practices
- `references/overview.md` — How scalability-fix works, priority order, score targets
- `references/best-practices.md` — Fix discipline, safe vs dangerous changes

### Workflow
- `references/implementation-workflow.md` — 6-step process, priority matrix
- `references/verification.md` — Post-fix checklist, re-scoring protocol, loop mode

### Fix Patterns (5 files covering 10 categories)
- `references/fix-patterns/bundle-images.md` — Dynamic imports, image optimization
- `references/fix-patterns/rsc-dbperf.md` — Server Components, query optimization
- `references/fix-patterns/api-client.md` — Response optimization, client performance
- `references/fix-patterns/edge-memory.md` — Edge config, resource cleanup
- `references/fix-patterns/concurrency-monitoring.md` — Parallel processing, observability
