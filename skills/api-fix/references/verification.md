# Verification & Re-Scoring

## Post-Fix Verification Checklist

### 1. TypeScript
```bash
pnpm typecheck
```
Must pass with zero errors. New types, interfaces, or response shapes must be consistent.

### 2. Tests
```bash
pnpm test
```
All existing tests must pass. No regressions. New API tests must cover auth + validation + happy path.

### 3. Build
```bash
pnpm build
```
Build must succeed. Watch for:
- Missing imports (renamed helpers, new modules)
- Type mismatches from response envelope changes
- Middleware changes breaking API routes

## Re-Scoring Protocol

After all fixes pass verification, invoke `api-scoring` skill to produce a new scorecard.

### Comparison Template

```markdown
## Fix Results: API Audit

### Score Comparison
| # | Category | Weight | Before | After | Delta |
|---|----------|--------|--------|-------|-------|
| 1 | Security | 20% | X/10 | Y/10 | +Z |
| 2 | Auth & AuthZ | 15% | X/10 | Y/10 | +Z |
| 3 | Input Validation | 12% | X/10 | Y/10 | +Z |
| 4 | Error Handling | 10% | X/10 | Y/10 | +Z |
| 5 | Rate Limiting | 10% | X/10 | Y/10 | +Z |
| 6 | Response Design | 8% | X/10 | Y/10 | +Z |
| 7 | Performance | 8% | X/10 | Y/10 | +Z |
| 8 | Observability | 7% | X/10 | Y/10 | +Z |
| 9 | Documentation | 5% | X/10 | Y/10 | +Z |
| 10 | Testing | 5% | X/10 | Y/10 | +Z |
| **Total** | | | **XX/100** | **YY/100** | **+ZZ** |
| **Grade** | | | **C+** | **A** | |

### Fixes Applied (N total)
1. [Description] — [files changed]

### Remaining Issues
1. [Issue] — [reason not fixed]
```

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
1. Each iteration: parse new scorecard → fix remaining → verify → re-score
2. Track iteration count (max 3)
3. Track score delta per iteration — if delta = 0 for 2 consecutive, stop
4. Final output: full before/after comparison across ALL iterations

## Commit Message Template

```
fix(api): improve API score from XX to YY

- [Fix 1 description]
- [Fix 2 description]
- [Fix N description]

Score: XX/100 (C+) -> YY/100 (A+)
```
