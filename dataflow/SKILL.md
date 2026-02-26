---
name: dataflow
description: Data flow quality system. 7 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score then fix until target), generate (create new code), review (quick file check), migrate (framework upgrade), test (generate test cases).
license: Complete terms in LICENSE.txt
---

# Data Flow Quality System

One skill, 7 modes. Score data flow quality, fix issues, run the full loop, generate compliant code, review files, migrate frameworks, or generate tests.

## Modes

| Mode | Trigger | What it does |
|------|---------|--------------|
| **score** | "score dataflow", "dataflow audit" | Run 10-category audit, produce scorecard with grade A+ to F |
| **fix** | "fix dataflow", provide a scorecard | Parse scorecard, prioritize by severity x weight, apply fixes, verify |
| **loop** | "dataflow loop", "score and fix until B+" | Score -> fix -> re-score, repeat until target grade reached |
| **generate** | Create new code | Load criteria -> Generate meeting all 10 -> Self-check |
| **review** | Quick 1-2 file check | Read files -> Score applicable categories -> Annotate + fix |
| **migrate** | Framework upgrade | Detect versions -> Map breaking changes -> Migrate -> Verify |
| **test** | Generate test cases | Map categories to assertions -> Generate test files |

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
| A | 93-96 | B | 83-86 | C | 73-76 |
| A- | 90-92 | B- | 80-82 | D | 60-72 |
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

Auto-iterate: score -> fix all issues -> re-score -> repeat until target grade reached (default B+ for production, A- for enterprise).
- Max 5 iterations
- Halts if any category regresses or if no improvement after a cycle

## Mode: Generate

Generate code meeting all 10 categories at 9-10/10. Load `references/generate/workflow.md`.
Parse request → Load criteria → Generate with all patterns → Self-check → Output (`assets/templates/generated-code.md.template`)

## Mode: Review

Quick 1-2 file review. Load `references/review/workflow.md`.
Read files → Score applicable categories → Annotate line numbers → Suggest fixes (`assets/templates/review-report.md.template`)

## Mode: Migrate

Upgrade code for framework changes. Load `references/migrate/workflow.md`.
Detect versions → Map breaking changes → Apply migrations → Verify (`assets/templates/migration-report.md.template`)

## Mode: Test

Generate tests from scoring criteria. Load `references/test/workflow.md`.
Map categories to assertions → Generate tests → Output suite (`assets/templates/test-suite.md.template`)

## Cross-Skill Overlap

Some dataflow categories overlap with other skills. When auditing or fixing:
- **Prisma Optimization** — overlaps with `database` skill (schema design, indexing). Use dataflow for query patterns in application code; use database for schema-level changes.
- **API Route Design** — overlaps with `api` skill (validation, auth, rate limiting). Use dataflow for data flow through routes; use api for API architecture and standards.
- **Caching & Revalidation** — overlaps with `caching` skill (headers, ISR, "use cache"). Use dataflow for cache integration in data pipelines; use caching for cache strategy and configuration.

## Output Templates

- **Scorecard**: `assets/templates/scorecard.md.template` -- fill `{{VARIABLE}}` placeholders
- **Fix Report**: `assets/templates/fix-report.md.template` -- fill `{{VARIABLE}}` placeholders
- **Generate**: `assets/templates/generated-code.md.template`
- **Review**: `assets/templates/review-report.md.template`
- **Migrate**: `assets/templates/migration-report.md.template`
- **Test**: `assets/templates/test-suite.md.template`
