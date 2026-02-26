---
name: scalability
description: Scalability quality system. 7 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score then fix until target).
license: Complete terms in LICENSE.txt
---

# Scalability Quality System

One skill, 7 modes. Score scalability, fix bottlenecks, or run the full loop.

## Modes

| Mode | Trigger | What it does |
|------|---------|--------------|
| **score** | "score scalability", "scalability audit" | Run 10-category audit, produce scorecard with grade A+ to F |
| **fix** | "fix scalability", provide a scorecard | Parse scorecard, prioritize by severity x weight, apply fixes, verify |
| **loop** | "scalability loop", "score and fix until B+" | Score -> fix -> re-score, repeat until target grade reached |
| **generate** | Create new code | Load criteria -> Generate meeting all 10 -> Self-check |
| **review** | Quick 1-2 file check | Read files -> Score applicable categories -> Annotate + fix |
| **migrate** | Framework upgrade | Detect versions -> Map breaking changes -> Migrate -> Verify |
| **test** | Generate test cases | Map categories to assertions -> Generate test files |

## Mode: Score

Audit scalability and performance against 10 weighted categories. Produces scorecard with grade, per-category scores, issues list with severity, and fix recommendations.

### Scoring Categories

| # | Category | Weight | Key Signals |
|---|----------|--------|-------------|
| 1 | Bundle Size & Code Splitting | 15% | Dynamic imports, tree shaking, no barrel re-exports, lazy components |
| 2 | Image & Asset Optimization | 12% | next/image, WebP/AVIF, lazy loading, responsive sizes |
| 3 | Server Component Architecture | 12% | RSC by default, minimal "use client", streaming, Suspense |
| 4 | Database Query Performance | 12% | No N+1, connection pooling, indexed queries, select fields |
| 5 | API Response Performance | 10% | Small payloads, pagination, no over-fetching, compression |
| 6 | Client-Side Performance | 10% | Minimal re-renders, memoization where needed, no layout thrash |
| 7 | Edge & CDN Optimization | 8% | Static generation, ISR, proxy configuration, CDN-friendly headers |
| 8 | Memory & Resource Management | 8% | No leaks, connection cleanup, bounded caches, AbortController |
| 9 | Concurrent & Parallel Processing | 7% | Promise.all for independent fetches, streaming responses |
| 10 | Performance Monitoring & Budgets | 6% | Web Vitals tracking, bundle budget, lighthouse CI |

### Grade Scale

| Grade | Score | Grade | Score | Grade | Score |
|-------|-------|-------|-------|-------|-------|
| A+ | 97-100 | B+ | 87-89 | C+ | 77-79 |
| A | 93-96 | B | 83-86 | C | 73-76 |
| A- | 90-92 | B- | 80-82 | D | 60-72 |
| | | | | F | <60 |

### Scoring References

- `references/scoring/overview.md` -- Scoring system, output format, files to audit
- `references/scoring/scoring-workflow.md` -- Step-by-step audit process
- `references/scoring/best-practices.md` -- Do/Don't tables for all categories
- `references/scoring/criteria/bundle-images.md` -- Bundle Size (15%) + Images (12%)
- `references/scoring/criteria/rsc-dbperf.md` -- Server Components (12%) + DB Perf (12%)
- `references/scoring/criteria/api-client.md` -- API Perf (10%) + Client Perf (10%)
- `references/scoring/criteria/edge-memory.md` -- Edge/CDN (8%) + Memory (8%)
- `references/scoring/criteria/concurrency-monitoring.md` -- Concurrency (7%) + Monitoring (6%)

## Mode: Fix

Parse a scorecard and systematically implement all fixes. Prioritize by severity x weight, apply code changes, verify each fix, re-score.

### Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or user-visible perf | Fix immediately -- blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next -- moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

### Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Bundle Size, Image Optimization | `references/fix/fix-patterns/bundle-images.md` |
| RSC Architecture, DB Performance | `references/fix/fix-patterns/rsc-dbperf.md` |
| API Performance, Client Performance | `references/fix/fix-patterns/api-client.md` |
| Edge/CDN, Memory Management | `references/fix/fix-patterns/edge-memory.md` |
| Concurrency, Monitoring | `references/fix/fix-patterns/concurrency-monitoring.md` |

### Fix References

- `references/fix/overview.md` -- How fix mode works, priority order, score targets
- `references/fix/best-practices.md` -- Fix discipline, safe vs dangerous changes
- `references/fix/implementation-workflow.md` -- 6-step process, priority matrix
- `references/fix/verification.md` -- Post-fix checklist, re-scoring protocol, loop mode

## Mode: Loop

Auto-iterate: score -> fix all issues -> re-score -> repeat until target grade reached (default B+ for production, A- for enterprise). Max 5 iterations. Halts if any category regresses or if no improvement after a cycle.

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

## Output Templates

- **Scorecard**: `assets/templates/scorecard.md.template` -- fill `{{VARIABLE}}` placeholders
- **Fix Report**: `assets/templates/fix-report.md.template` -- fill `{{VARIABLE}}` placeholders
- Generate: `assets/templates/generated-code.md.template`
- Review: `assets/templates/review-report.md.template`
- Migrate: `assets/templates/migration-report.md.template`
- Test: `assets/templates/test-suite.md.template`
