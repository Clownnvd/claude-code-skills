# DB Scoring — Audit Workflow

## Step 1: Gather Files

Read these files (in order of priority):

| File | What to Look For |
|------|-----------------|
| `prisma/schema.prisma` | Models, fields, types, relations, indexes, enums |
| `prisma.config.ts` | Datasource URL, provider, preview features |
| `prisma/migrations/` | Migration history, destructive changes |
| `prisma/seed.ts` | Seeding strategy |
| `src/app/api/**/*.ts` | Query patterns (findMany, include, select, raw) |
| `src/lib/` or `src/services/` | Data access layer, transactions |
| `.env.example` | Connection string format, env var naming |
| `src/lib/validations/` | Zod schemas for input validation |

## Step 2: Score Each Category

For each of the 10 categories:

1. Start at **5/10** (neutral baseline)
2. Read the relevant criteria file from `criteria/`
3. Check each item on the checklist
4. **Subtract 1** for each missing critical item
5. **Add 1** for each best practice found with evidence
6. Cap at 0 minimum, 10 maximum
7. Require **concrete evidence** for scores 9-10

### Category → Criteria File Mapping

| Categories | Criteria Reference |
|-----------|-------------------|
| Schema Design (1), Data Integrity (2) | `criteria/schema-design.md` |
| Security (4) | `criteria/security-compliance.md` |
| Indexing (3), Query Performance (5), Scalability (9) | `criteria/performance-scaling.md` |
| Migration (6), Monitoring (7), Backup (8) | `criteria/operations-reliability.md` |
| Developer Experience (10) | Check across all files |

### ORM-Specific Adjustments

| If Using... | Also Load |
|------------|-----------|
| Prisma | `prisma-patterns.md` — Prisma-specific scoring adjustments |
| Neon PostgreSQL | `neon-patterns.md` — Neon-specific scoring adjustments |

## Step 3: Calculate Weighted Score

```
weighted_score = sum(category_score * weight) for each category
grade = lookup(weighted_score) from grade table
```

| Weight | Categories |
|--------|-----------|
| 15% | Schema Design, Security |
| 12% | Data Integrity, Indexing Strategy |
| 10% | Query Performance, Migration & Versioning |
| 8% | Monitoring & Observability, Backup & Recovery |
| 5% | Scalability, Developer Experience |

## Step 4: Generate Issues List

Classify each finding:

| Severity | Criteria | Examples |
|----------|----------|---------|
| CRITICAL | Score 0-3 or security vulnerability | No auth on API, SQL injection, exposed secrets |
| HIGH | Score 4-5 | Missing indexes on FK, no constraints |
| MEDIUM | Score 6-7 | No updatedAt, weak naming |
| LOW | Score 8, minor improvement | Could add composite index, missing seed |

### Issue Format

```markdown
[SEVERITY] Short description
  File: path/to/file.ts:line
  Current: What exists now
  Expected: What should be there
  Fix: Concrete action to take
```

## Step 5: Output Scorecard

Use the scorecard template from `overview.md`. Include:

1. **Score table** — all 10 categories with scores, weights, weighted totals
2. **Final score and grade**
3. **Issues list** — sorted by severity (CRITICAL → HIGH → MEDIUM → LOW)
4. **Quick wins** — top 3 changes that would most improve the score
5. **ORM-specific notes** — Prisma/Neon findings if applicable

## Step 6: Re-Score (Optional)

After fixes are applied:
1. Re-read modified files
2. Re-score only affected categories
3. Show before/after comparison
4. Stop when target grade reached or delta = 0 for 2 rounds
