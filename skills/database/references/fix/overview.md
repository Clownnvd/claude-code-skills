# Database Fix — Overview

## Purpose

Take a db-scoring scorecard (10-category audit) and systematically implement all fixes. Prioritize by severity + weight, apply code changes, verify, and re-score.

## How It Works

```
db-scoring output → parse scorecard → prioritize issues → apply fixes → verify → re-score
```

### Input: db-scoring Scorecard

The scorecard contains:
- **10 category scores** (0-10 each, weighted to 0-100 total)
- **Letter grade** (A+ to F)
- **Issues list** with severity (CRITICAL / HIGH / MEDIUM / LOW)
- **Quick wins** (highest impact, lowest effort)

### Output: Fixed Codebase + Before/After Comparison

## Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or security hole | Fix immediately — blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next — moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

## Category → Fix Pattern Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Schema Design, Data Integrity | `fix-patterns/schema-integrity.md` |
| Security | `fix-patterns/security.md` |
| Indexing, Query Performance, Scalability | `fix-patterns/performance-scaling.md` |
| Migration, Monitoring, Backup, DevEx | `fix-patterns/operations.md` |

## Files Touched During Fix

| File Type | Examples |
|-----------|---------|
| Schema | `prisma/schema.prisma` |
| Config | `prisma.config.ts`, `package.json` |
| DB client | `src/lib/db/index.ts` |
| Env validation | `src/lib/env.ts`, `.env.example` |
| API routes | `src/app/api/**/*.ts` |
| Services | `src/lib/**/*.ts` |
| Seed | `prisma/seed.ts` |
| Migrations | `prisma/migrations/` (generated) |

## Score Targets

| Target | Score | When |
|--------|-------|------|
| Minimum viable | 73+ (C+) | Internal/prototype |
| Production-ready | 83+ (B) | Public launch |
| Enterprise-grade | 90+ (A-) | Critical systems |

## Integration with db-scoring

1. Run `db-scoring` → get scorecard
2. Run `db-fix` → implement fixes from scorecard
3. Run `db-scoring` again → verify improvement
4. Repeat if score < target (max 3 iterations)
