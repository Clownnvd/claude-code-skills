---
name: dataflow-fix
description: Take dataflow-scoring feedback (scorecard + issues list) and implement all fixes systematically. Prioritize by severity, apply code changes, verify, and re-score. Next.js App Router + React 19 + Prisma.
---

# Data Flow Fix

Take a dataflow-scoring scorecard and systematically implement all fixes. Prioritize by severity + weight, apply code changes, verify, and re-score.

## When to Use

- After running `dataflow-scoring` and receiving a scorecard with issues
- When data flow scores below target (< B+ for production, < A- for enterprise)
- To systematically fix all CRITICAL -> HIGH -> MEDIUM -> LOW items
- Before deploying data flow that failed a quality gate

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
| Server Component Fetching, Server/Client Composition | `references/fix-patterns/rsc-composition.md` |
| Prisma Optimization, API Route Design | `references/fix-patterns/prisma-api.md` |
| State Management, Caching & Revalidation | `references/fix-patterns/state-cache.md` |
| Type Safety, Error Propagation | `references/fix-patterns/types-errors.md` |
| Form Handling, Data Transformation | `references/fix-patterns/forms-dtos.md` |

## Implementation

Load `references/implementation-workflow.md` for step-by-step process (parse -> prioritize -> fix -> verify -> re-score).

## Quick Reference

### Overview & Best Practices
- `references/overview.md` — How dataflow-fix works, priority order, score targets
- `references/best-practices.md` — Fix discipline, safe vs dangerous changes

### Workflow
- `references/implementation-workflow.md` — 6-step process, priority matrix
- `references/verification.md` — Post-fix checklist, re-scoring protocol, loop mode

### Fix Patterns (5 files covering 10 categories)
- `references/fix-patterns/rsc-composition.md` — RSC fetching, "use client" optimization
- `references/fix-patterns/prisma-api.md` — Query select, indexes, API pipeline
- `references/fix-patterns/state-cache.md` — Server-first state, caching headers
- `references/fix-patterns/types-errors.md` — Zod schemas, error boundaries
- `references/fix-patterns/forms-dtos.md` — Form validation, DTO patterns
