# DB Scoring — Overview

## What This Skill Does

Audit any database (schema, queries, config) against 10 enterprise-grade criteria weighted by impact. Outputs a scorecard with numeric score (0-100), letter grade, and prioritized issues list.

## How It Works

```
User says "score my database" or "audit my schema"
  → Claude loads SKILL.md → identifies scoring mode
  → Reads: schema.prisma, prisma.config.ts, migration files, API routes
  → Scores 10 categories (each 0-10, weighted)
  → Outputs scorecard + issues list ranked by severity
```

## Scoring System

### 10 Categories (Weighted)

| # | Category | Weight | What It Measures |
|---|----------|--------|-----------------|
| 1 | Schema Design | 15% | Naming, types, normalization, relationships |
| 2 | Data Integrity | 12% | Constraints, validation, referential integrity |
| 3 | Indexing Strategy | 12% | Coverage, composite indexes, unused indexes |
| 4 | Security | 15% | Encryption, access control, RLS, secrets |
| 5 | Query Performance | 10% | N+1, select optimization, transactions |
| 6 | Migration & Versioning | 10% | Versioned, rollback capability, seeding |
| 7 | Monitoring & Observability | 8% | Logging, metrics, alerting, slow queries |
| 8 | Backup & Recovery | 8% | Frequency, PITR, tested restores |
| 9 | Scalability | 5% | Connection pooling, read replicas, partitioning |
| 10 | Developer Experience | 5% | Type safety, ORM config, documentation |

### Grade Scale

| Grade | Range | Meaning |
|-------|-------|---------|
| A+ | 97-100 | Enterprise-ready, all best practices followed |
| A | 93-96 | Production-grade, minor improvements possible |
| A- | 90-92 | Strong, few gaps |
| B+ | 87-89 | Good, some enterprise criteria missing |
| B | 83-86 | Acceptable for production |
| B- | 80-82 | Functional but gaps in security/reliability |
| C+ | 77-79 | Needs work before production |
| C | 73-76 | Significant gaps |
| D | 60-72 | Major issues, not production-ready |
| F | <60 | Critical problems, immediate action needed |

### Anti-Bias Rules

- Start every category at 5/10 (neutral baseline)
- Subtract for missing items, add for evidence of best practices
- 9-10 requires concrete evidence (actual index definitions, RLS policies, backup logs)
- Never give 10/10 without verifying implementation exists in code

## Scorecard Format

```markdown
## Database Scorecard — [Project Name]

| # | Category | Score | Weight | Weighted |
|---|----------|-------|--------|----------|
| 1 | Schema Design | 8/10 | 15% | 12.0 |
| ... | ... | ... | ... | ... |
| **Total** | | | | **82/100** |

**Grade: B-**

### Issues (by priority)
1. [CRITICAL] No index on `Purchase.userId` — full table scan on dashboard
2. [HIGH] Connection string in schema.prisma instead of prisma.config.ts
3. [MEDIUM] Missing `updatedAt` on User model
4. [LOW] No seed script for development
```

## File Structure

```
db-scoring/
├── SKILL.md                              — Entry point, category table, grade scale
├── LICENSE.txt                           — Apache 2.0
├── references/
│   ├── overview.md                       — This file
│   ├── best-practices.md                 — Do/Don't for database design
│   ├── scoring-workflow.md               — Step-by-step audit process
│   ├── criteria/
│   │   ├── schema-design.md              — Schema + Data Integrity criteria
│   │   ├── security-compliance.md        — Security + Compliance criteria
│   │   ├── performance-scaling.md        — Indexing + Queries + Scalability
│   │   └── operations-reliability.md     — Migration + Monitoring + Backup
│   ├── prisma-patterns.md               — Prisma 7 specific scoring
│   └── neon-patterns.md                 — Neon PostgreSQL specific scoring
```

## Integration Points

- **Prisma schema**: `prisma/schema.prisma` — models, relations, indexes
- **Prisma config**: `prisma.config.ts` (Prisma 7) — datasource URL
- **Migrations**: `prisma/migrations/` — version history
- **API routes**: `src/app/api/` — query patterns
- **Env files**: `.env`, `.env.example` — connection strings, secrets
