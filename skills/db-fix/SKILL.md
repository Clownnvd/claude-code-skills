---
name: db-fix
description: Take db-scoring feedback (scorecard + issues list) and implement all fixes systematically. Prioritize by severity, apply code changes, verify, and re-score. Prisma + Neon patterns.
license: Complete terms in LICENSE.txt
---

# Database Fix

Take a db-scoring scorecard and systematically implement all fixes. Prioritize by severity + weight, apply code changes, verify, and re-score.

## When to Use

- After running `db-scoring` and receiving a scorecard with issues
- When database scores below target (< B for production, < A- for enterprise)
- To systematically fix all CRITICAL -> HIGH -> MEDIUM -> LOW items
- Before deploying a database that failed a quality gate

## Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or security hole | Fix immediately — blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next — moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

## Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Schema Design, Data Integrity | `references/fix-patterns/schema-integrity.md` |
| Security | `references/fix-patterns/security.md` |
| Indexing, Query Performance, Scalability | `references/fix-patterns/performance-scaling.md` |
| Migration, Monitoring, Backup, DevEx | `references/fix-patterns/operations.md` |

## Implementation

Load `references/implementation-workflow.md` for step-by-step process (parse -> prioritize -> fix -> verify -> re-score).

## Quick Reference

### Overview & Best Practices
- `references/overview.md` — How db-fix works, priority order, score targets, integration with db-scoring
- `references/best-practices.md` — Fix discipline, schema change safety, migration patterns, common mistakes

### Workflow
- `references/implementation-workflow.md` — 6-step process, priority matrix, which refs to load
- `references/verification.md` — Post-fix checklist, re-scoring protocol, comparison template, loop mode

### Fix Patterns (4 files covering 10 categories)
- `references/fix-patterns/schema-integrity.md` — Enums, timestamps, comments, composite unique, cascades
- `references/fix-patterns/security.md` — Env validation, SSL, select clauses, raw queries, error leaking
- `references/fix-patterns/performance-scaling.md` — Indexes, N+1, pagination, transactions, connection pooling
- `references/fix-patterns/operations.md` — Migration sync, prisma generate, seed quality, logging, backup docs

## Output Templates

Use `assets/templates/fix-report.md.template` as the output format when generating fix reports. Fill `{{VARIABLE}}` placeholders with actual values.
