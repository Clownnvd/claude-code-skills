# Verification & Re-Scoring

## Post-Fix Verification Checklist

### 1. TypeScript
```bash
pnpm typecheck
```
Must pass with zero errors. Schema changes regenerate types — run `prisma generate` first.

### 2. Tests
```bash
pnpm test
```
All existing tests must pass. No regressions. If new DB logic added, add tests.

### 3. Build
```bash
pnpm build
```
Build must succeed. Watch for:
- Missing imports (renamed models, removed fields)
- Prisma client type mismatches after schema change
- Env var references that changed names

### 4. Migration Check
```bash
npx prisma migrate dev --name verify_sync
```
If this creates a new migration, schema was out of sync. If "Already in sync", good.

### 5. Seed Verification
```bash
npx prisma migrate reset --force
```
Seed script must run successfully after full reset (dev environment only).

## Re-Scoring Protocol

After all fixes pass verification, invoke `db-scoring` skill to produce a new scorecard.

### Comparison Template

```markdown
## Fix Results: Database Audit

### Score Comparison
| # | Category | Weight | Before | After | Delta |
|---|----------|--------|--------|-------|-------|
| 1 | Schema Design | 15% | X/10 | Y/10 | +Z |
| 2 | Data Integrity | 12% | X/10 | Y/10 | +Z |
| 3 | Indexing Strategy | 12% | X/10 | Y/10 | +Z |
| 4 | Security | 15% | X/10 | Y/10 | +Z |
| 5 | Query Performance | 10% | X/10 | Y/10 | +Z |
| 6 | Migration & Versioning | 10% | X/10 | Y/10 | +Z |
| 7 | Monitoring & Observability | 8% | X/10 | Y/10 | +Z |
| 8 | Backup & Recovery | 8% | X/10 | Y/10 | +Z |
| 9 | Scalability | 5% | X/10 | Y/10 | +Z |
| 10 | Developer Experience | 5% | X/10 | Y/10 | +Z |
| **Total** | | | **XX/100** | **YY/100** | **+ZZ** |
| **Grade** | | | **C+** | **B+** | |

### Fixes Applied (N total)
1. [Description] — [files changed]

### Remaining Issues
1. [Issue] — [reason not fixed]

### Score Target Met?
- [ ] Target: >= B (83+)
- [ ] All CRITICALs resolved
- [ ] No new issues introduced
```

## Score Targets

| Target | Score | When |
|--------|-------|------|
| Minimum viable | 73+ (C+) | Internal/prototype |
| Production-ready | 83+ (B) | Public launch |
| Enterprise-grade | 90+ (A-) | Critical systems |

## Iteration Decision

After re-scoring:

| Result | Action |
|--------|--------|
| Score >= target | Done. Output final comparison. |
| Score improved but < target | Auto-iterate: go to Step 1 with new scorecard |
| Score didn't improve after 2 iterations | Stop. Report remaining as "needs external action". |
| Score decreased | Revert last batch. Fix introduced regressions. |

### Loop Mode Protocol

When "fix until target" is requested:
1. Each iteration: parse new scorecard -> fix remaining -> verify -> re-score
2. Track iteration count (max 3)
3. Track score delta per iteration — if delta = 0 for 2 consecutive, stop
4. Final output: full before/after comparison across ALL iterations

## Commit Message Template

```
fix(db): improve database score from XX to YY

- [Fix 1 description]
- [Fix 2 description]
- [Fix N description]

Score: XX/100 (C+) -> YY/100 (B+)
```
