# Caching Strategy Fix — Verification & Re-Scoring

## Post-Fix Verification Checklist

### 1. TypeScript
```bash
npx tsc --noEmit
```
Must pass with zero errors.

### 2. Tests
```bash
pnpm test
```
All existing tests must pass. No regressions.

### 3. Build
```bash
pnpm build
```
Build must succeed. Check build output for static/dynamic route classification.

### 4. Caching Spot-Check
- Do ALL API routes have `NO_CACHE_HEADERS` on authenticated responses?
- Do ALL API routes have `export const dynamic = "force-dynamic"`?
- Is `revalidatePath` called after EVERY mutation?
- Is the landing page static in build output?
- Does proxy skip static assets?
- Is `cache()` wrapping auth/session lookups?

## Re-Scoring Protocol

After all fixes pass verification, invoke `caching-scoring` skill.

### Comparison Template
```markdown
## Caching Strategy Fix Results

| # | Category | Before | After | Delta |
|---|----------|--------|-------|-------|
| 1 | Cache-Control Headers (15%) | X/10 | Y/10 | +Z |
| 2 | Revalidation Strategy (15%) | X/10 | Y/10 | +Z |
| ... | | | | |
| **Total** | | **XX/100** | **YY/100** | **+ZZ** |
| **Grade** | | **C+** | **B+** | |

### Fixes Applied
1. [Fix description] — [files changed]

### Remaining Issues
1. [Issue] — [reason not fixed]
```

## Loop Mode Protocol

When "fix until 100" is requested:
1. Each iteration: parse new scorecard -> fix remaining deductions -> verify -> re-score
2. Track iteration count (max 5)
3. Track score delta per iteration — if delta = 0 for 2 consecutive iterations, stop
4. Final output: full before/after comparison across ALL iterations
