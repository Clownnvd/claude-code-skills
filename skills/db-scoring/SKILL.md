---
name: db-scoring
description: Audit databases against 10 enterprise criteria (schema, security, indexing, performance, migration, monitoring, backup, scalability, DevEx). Prisma + Neon patterns included.
license: Complete terms in LICENSE.txt
---

# Database Scoring

Audit any database against 10 enterprise-grade criteria. Score 0-100 with letter grade and prioritized issues list.

## When to Use

- Before deploying a new database schema to production
- Auditing an existing project's database health
- Reviewing schema design in a pull request
- Checking Prisma + Neon configuration for best practices
- Quality gate: require B+ (87+) before production deploy

## Scoring Categories

| # | Category | Weight | Criteria Reference |
|---|----------|--------|--------------------|
| 1 | Schema Design | 15% | `criteria/schema-design.md` |
| 2 | Data Integrity | 12% | `criteria/schema-design.md` |
| 3 | Indexing Strategy | 12% | `criteria/performance-scaling.md` |
| 4 | Security | 15% | `criteria/security-compliance.md` |
| 5 | Query Performance | 10% | `criteria/performance-scaling.md` |
| 6 | Migration & Versioning | 10% | `criteria/operations-reliability.md` |
| 7 | Monitoring & Observability | 8% | `criteria/operations-reliability.md` |
| 8 | Backup & Recovery | 8% | `criteria/operations-reliability.md` |
| 9 | Scalability | 5% | `criteria/performance-scaling.md` |
| 10 | Developer Experience | 5% | `criteria/operations-reliability.md` |

## Audit Process

Load `references/scoring-workflow.md` for full steps.

1. **Gather** — Read schema, config, migrations, API routes, env files
2. **Score** — Each category 0-10, starting at 5 (neutral baseline)
3. **Calculate** — Weighted sum → 0-100 score → letter grade
4. **Report** — Scorecard table + prioritized issues list + quick wins

## Grades

| Grade | Range | Production Ready? |
|-------|-------|-------------------|
| A+/A/A- | 90-100 | Enterprise-grade |
| B+/B | 83-89 | Production-ready |
| B- | 80-82 | Acceptable with caveats |
| C+/C | 73-79 | Needs work first |
| D/F | <73 | Not ready |

## ORM & Provider Adjustments

| Stack | Additional Reference |
|-------|---------------------|
| Prisma (any version) | `references/prisma-patterns.md` — schema patterns, query anti-patterns, migration commands |
| Prisma 7 specifically | `references/prisma-patterns.md` — `prisma.config.ts` requirement (critical) |
| Neon PostgreSQL | `references/neon-patterns.md` — branching, pooling, PITR, edge runtime |

## Issue Severity

| Severity | Criteria | Action |
|----------|----------|--------|
| CRITICAL | Score 0-3 or security hole | Fix before deploy |
| HIGH | Score 4-5, weight >= 12% | Fix in current sprint |
| MEDIUM | Score 4-5, weight < 12% | Fix next sprint |
| LOW | Score 7-8 | Backlog |

## Quick Reference — All Files

### Overview & Best Practices
- `references/overview.md` — Scoring system, grade scale, scorecard format, file structure
- `references/best-practices.md` — Do/Don't for schema, security, performance, migrations

### Workflow
- `references/scoring-workflow.md` — 6-step audit process, category mapping, issue format

### Criteria (4 files covering 10 categories)
- `references/criteria/schema-design.md` — Schema Design + Data Integrity
- `references/criteria/security-compliance.md` — Security + Compliance
- `references/criteria/performance-scaling.md` — Indexing + Queries + Scalability
- `references/criteria/operations-reliability.md` — Migration + Monitoring + Backup + DevEx

### ORM & Provider Specific
- `references/prisma-patterns.md` — Prisma 7 config, schema/query patterns, migration commands
- `references/neon-patterns.md` — Branching, pooling, PITR, edge runtime, region selection
