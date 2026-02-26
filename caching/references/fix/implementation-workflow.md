# Caching Strategy Fix — Implementation Workflow

## Step 1: Parse Scorecard

Extract from caching-scoring output:
- Per-category scores (identify < 10)
- Issues list with severity
- Affected files

## Step 2: Prioritize

Sort issues by: `severity * category_weight`

| Priority | What to fix |
|----------|------------|
| P1 | CRITICAL in any category |
| P2 | HIGH in 15% categories (Headers, Revalidation) |
| P3 | HIGH in 10-12% categories (Static/Dynamic, ReactCache, UseCache) |
| P4 | MEDIUM in any category |
| P5 | LOW (backlog) |

## Step 3: Load Fix Patterns

For each issue, load the corresponding fix-patterns file:

| Category | Fix Patterns File |
|----------|------------------|
| Headers + Revalidation | `fix-patterns/headers-revalidation.md` |
| Static/Dynamic + ISR | `fix-patterns/static-dynamic-isr.md` |
| React cache + `"use cache"` | `fix-patterns/react-cache-use-cache.md` |
| CDN + Request Dedup | `fix-patterns/cdn-dedup.md` |
| Proxy + Monitoring | `fix-patterns/proxy-monitoring.md` |

## Step 4: Apply Fixes

For each fix:
1. Read the target file
2. Apply the change
3. Run `npx tsc --noEmit` immediately
4. Fix any type errors before moving on

## Step 5: Verify

After all fixes:
1. `npx tsc --noEmit` — 0 errors
2. `pnpm test` — all tests pass
3. `pnpm build` — build succeeds

## Step 6: Re-Score

Run caching-scoring again on fixed code. Output comparison:

```markdown
| # | Category | Before | After | Delta |
|---|----------|--------|-------|-------|
| 1 | Cache-Control Headers (15%) | X/10 | Y/10 | +Z |
| ... | | | | |
| **Total** | | **XX/100** | **YY/100** | **+ZZ** |
```
