---
name: dataflow
description: Data flow quality system. 3 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score then fix until target).
---

# Data Flow Quality System

One skill, 3 modes. Score data flow quality, fix issues, or run the full loop.

## Modes

| Mode | Trigger | What it does |
|------|---------|--------------|
| **score** | "score dataflow", "dataflow audit" | Run 10-category audit, produce scorecard with grade A+ to F |
| **fix** | "fix dataflow", provide a scorecard | Parse scorecard, prioritize by severity x weight, apply fixes, verify |
| **loop** | "dataflow loop", "score and fix until B+" | Score -> fix -> re-score, repeat until target grade reached |

## Mode: Score

Audit data flow quality against 10 weighted categories. Produces scorecard with grade, per-category scores, issues list with severity, and fix recommendations.

### Scoring Categories

| # | Category | Weight | Key Signals |
|---|----------|--------|-------------|
| 1 | Server Component Data Fetching | 15% | RSC async, no client useEffect for initial data |
| 2 | Server/Client Composition | 10% | "use client" at leaf level, serializable props |
| 3 | Prisma Query Optimization | 12% | select, findUnique, indexes, singleton, pooling |
| 4 | API Route Design | 15% | Validation, auth, rate limit, CSRF, response envelope |
| 5 | State Management | 8% | Minimal client state, server-first |
| 6 | Caching & Revalidation | 10% | Cache headers, "use cache" directive, revalidation |
| 7 | Type Safety Across Boundaries | 10% | Zod schemas, shared types, ApiResponse<T> |
| 8 | Error Propagation | 8% | error.tsx, error boundaries, safe error messages |
| 9 | Form Handling | 7% | Validation, loading states, CSRF, error display |
| 10 | Data Transformation (DTOs) | 5% | No Prisma leak, date serialization, field filtering |

### Grade Scale

| Grade | Score | Grade | Score | Grade | Score |
|-------|-------|-------|-------|-------|-------|
| A+ | 97-100 | B+ | 87-89 | C+ | 77-79 |
| A | 93-96 | B | 83-86 | C | 70-76 |
| A- | 90-92 | B- | 80-82 | D | 60-69 |
| | | | | F | <60 |

### Scoring References

- `references/scoring/overview.md` -- Scoring system, output format, quality gates
- `references/scoring/scoring-workflow.md` -- Step-by-step audit process
- `references/scoring/best-practices.md` -- Do/Don't tables for all categories
- `references/scoring/criteria/rsc-composition.md` -- RSC Fetching (15%) + Composition (10%)
- `references/scoring/criteria/prisma-api.md` -- Prisma Optimization (12%) + API Routes (15%)
- `references/scoring/criteria/state-cache.md` -- State Management (8%) + Caching (10%)
- `references/scoring/criteria/types-errors.md` -- Type Safety (10%) + Error Propagation (8%)
- `references/scoring/criteria/forms-dtos.md` -- Form Handling (7%) + DTOs (5%)

## Mode: Fix

Parse a scorecard and systematically implement all fixes. Prioritize by severity x weight, apply code changes, verify each fix, re-score.

### Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or data leak | Fix immediately -- blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next -- moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

### Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Server Component Fetching, Server/Client Composition | `references/fix/fix-patterns/rsc-composition.md` |
| Prisma Optimization, API Route Design | `references/fix/fix-patterns/prisma-api.md` |
| State Management, Caching & Revalidation | `references/fix/fix-patterns/state-cache.md` |
| Type Safety, Error Propagation | `references/fix/fix-patterns/types-errors.md` |
| Form Handling, Data Transformation | `references/fix/fix-patterns/forms-dtos.md` |

### Fix References

- `references/fix/overview.md` -- How fix mode works, priority order, score targets
- `references/fix/best-practices.md` -- Fix discipline, safe vs dangerous changes
- `references/fix/implementation-workflow.md` -- 6-step process, priority matrix
- `references/fix/verification.md` -- Post-fix checklist, re-scoring protocol, loop mode

## Mode: Loop

Auto-iterate: score -> fix all issues -> re-score -> repeat until target grade reached (default B+ for production, A- for enterprise). Halts if any category regresses or if no improvement after a cycle.

## Output Templates

- **Scorecard**: `assets/templates/scorecard.md.template` -- fill `{{VARIABLE}}` placeholders
- **Fix Report**: `assets/templates/fix-report.md.template` -- fill `{{VARIABLE}}` placeholders
