---
name: database
description: Database quality system. 7 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score->fix until target). Prisma + Neon patterns.
license: Complete terms in LICENSE.txt
---

# Database Quality System

One skill, 7 modes. Score database design, fix issues, or run the full loop.

## Modes

| Mode | Trigger | What It Does |
|------|---------|--------------|
| **score** | "score my database", "audit DB" | 10-category audit -> scorecard with grade (A+ to F) |
| **fix** | "fix database issues", provide a scorecard | Parse scorecard -> prioritize -> apply fixes -> verify |
| **loop** | "score and fix until B+", "database loop" | Run score, then fix, then re-score until target grade reached |
| **generate** | Create new code | Load criteria -> Generate meeting all 10 -> Self-check |
| **review** | Quick 1-2 file check | Read files -> Score applicable categories -> Annotate + fix |
| **migrate** | Framework upgrade | Detect versions -> Map breaking changes -> Migrate -> Verify |
| **test** | Generate test cases | Map categories to assertions -> Generate test files |

## Mode: Score

Audit any database against 10 weighted categories. Score 0-100 with letter grade and prioritized issues list.

Load `references/scoring/scoring-workflow.md` for the full 6-step process.

| # | Category | Weight | Criteria Reference |
|---|----------|--------|--------------------|
| 1 | Schema Design | 15% | `scoring/criteria/schema-design.md` |
| 2 | Data Integrity | 12% | `scoring/criteria/schema-design.md` |
| 3 | Indexing Strategy | 12% | `scoring/criteria/performance-scaling.md` |
| 4 | Security | 15% | `scoring/criteria/security-compliance.md` |
| 5 | Query Performance | 10% | `scoring/criteria/performance-scaling.md` |
| 6 | Migration & Versioning | 10% | `scoring/criteria/operations-reliability.md` |
| 7 | Monitoring & Observability | 8% | `scoring/criteria/operations-reliability.md` |
| 8 | Backup & Recovery | 8% | `scoring/criteria/operations-reliability.md` |
| 9 | Scalability | 5% | `scoring/criteria/performance-scaling.md` |
| 10 | Developer Experience | 5% | `scoring/criteria/operations-reliability.md` |

### Grades

| Grade | Score | Grade | Score | Grade | Score |
|-------|-------|-------|-------|-------|-------|
| A+ | 97-100 | B+ | 87-89 | C+ | 77-79 |
| A | 93-96 | B | 83-86 | C | 73-76 |
| A- | 90-92 | B- | 80-82 | D | 60-72 |
| | | | | F | <60 |

### Issue Severity

| Severity | Criteria | Action |
|----------|----------|--------|
| CRITICAL | Score 0-3 or security hole | Fix before deploy |
| HIGH | Score 4-5, weight >= 12% | Fix in current sprint |
| MEDIUM | Score 4-5, weight < 12% | Fix next sprint |
| LOW | Score 7-8 | Backlog |

## Mode: Fix

Take a scorecard and systematically implement all fixes. Prioritize by severity * weight.

Load `references/fix/implementation-workflow.md` for the full 6-step process.

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or security hole | Fix immediately -- blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next -- moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

### Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Schema Design, Data Integrity | `fix/fix-patterns/schema-integrity.md` |
| Security | `fix/fix-patterns/security.md` |
| Indexing, Query Performance, Scalability | `fix/fix-patterns/performance-scaling.md` |
| Migration, Monitoring, Backup, DevEx | `fix/fix-patterns/operations.md` |

### Verification

Load `references/fix/verification.md` for post-fix checklist, re-scoring protocol, and comparison template.

## Mode: Loop

Automated score-fix cycle. Runs score -> fix -> re-score until target grade is met.

1. **Score** the database (Mode: Score)
2. If grade < target, **fix** all CRITICAL + HIGH issues (Mode: Fix)
3. **Re-score** and compare
4. Repeat until target grade reached or no score improvement between iterations

Default target: **B+ (87+)**. Override with "loop until A-" or similar.
- Max 5 iterations
- Stop on plateau (score unchanged after full fix cycle)

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

## Stack Adjustments

| Stack | Additional Reference |
|-------|---------------------|
| Prisma (any version) | `references/prisma-patterns.md` -- schema patterns, query anti-patterns, migration commands |
| Prisma 7 specifically | `references/prisma-patterns.md` -- `prisma.config.ts` requirement (critical) |
| Neon PostgreSQL | `references/neon-patterns.md` -- branching, pooling, PITR, edge runtime |

## Quick Reference -- All Files

### Scoring
- `references/scoring/overview.md` -- Scoring system, grade scale, scorecard format
- `references/scoring/best-practices.md` -- Do/Don't for schema, security, performance, migrations
- `references/scoring/scoring-workflow.md` -- 6-step audit process, category mapping, issue format
- `references/scoring/criteria/` -- 4 files covering 10 categories (schema-design, security-compliance, performance-scaling, operations-reliability)
- `references/neon-patterns.md` -- Branching, pooling, PITR, edge runtime, region selection
- `references/prisma-patterns.md` -- Prisma 7 config, schema/query patterns, migration commands

### Fix
- `references/fix/overview.md` -- How fix works, priority order, score targets
- `references/fix/best-practices.md` -- Fix discipline, schema change safety, migration patterns
- `references/fix/implementation-workflow.md` -- 6-step process, priority matrix, which refs to load
- `references/fix/verification.md` -- Post-fix checklist, re-scoring protocol, comparison template
- `references/fix/fix-patterns/` -- 4 files covering 10 categories (schema-integrity, security, performance-scaling, operations)

## Output Templates

- Score: `assets/templates/scorecard.md.template` | Fix: `assets/templates/fix-report.md.template`
- Generate: `assets/templates/generated-code.md.template` | Review: `assets/templates/review-report.md.template`
- Migrate: `assets/templates/migration-report.md.template` | Test: `assets/templates/test-suite.md.template`
Fill `{{VARIABLE}}` placeholders with actual values.
