# Scalability Fix — Implementation Workflow

## Step 1: Parse Scorecard

Extract from the scalability-scoring output:
- Per-category scores (which are below 10?)
- Issues list with severity, file:line, and fix description
- Current total and grade

## Step 2: Prioritize

Sort issues by: `severity_weight * category_weight` (see priority matrix in overview.md).

Group into fix batches:
1. **Batch 1**: CRITICAL issues (any category)
2. **Batch 2**: HIGH issues in categories >=12% weight (Bundle, Images, RSC, DB)
3. **Batch 3**: HIGH issues in categories <12% weight
4. **Batch 4**: MEDIUM issues (by weight)
5. **Batch 5**: LOW issues (optional)

## Step 3: Fix Each Issue

For each issue, load the relevant fix pattern file and apply:

| Category | Fix Pattern File |
|----------|-----------------|
| Bundle Size & Code Splitting | `fix-patterns/bundle-images.md` |
| Image & Asset Optimization | `fix-patterns/bundle-images.md` |
| Server Component Architecture | `fix-patterns/rsc-dbperf.md` |
| Database Query Performance | `fix-patterns/rsc-dbperf.md` |
| API Response Performance | `fix-patterns/api-client.md` |
| Client-Side Performance | `fix-patterns/api-client.md` |
| Edge & CDN Optimization | `fix-patterns/edge-memory.md` |
| Memory & Resource Management | `fix-patterns/edge-memory.md` |
| Concurrent & Parallel Processing | `fix-patterns/concurrency-monitoring.md` |
| Performance Monitoring & Budgets | `fix-patterns/concurrency-monitoring.md` |

## Step 4: Verify Each Fix

After each fix:
1. `pnpm typecheck` — no new type errors
2. `pnpm test` — all tests pass
3. Visually confirm fix addresses the specific issue

## Step 5: Re-Score

Run `scalability-scoring` again on the modified codebase:
- Compare before/after per-category scores
- Verify deductions removed
- Check for regressions (fixes that broke other categories)

## Step 6: Loop Until Target

If score < target:
1. Re-read new issues list
2. Repeat Steps 2-5
3. Maximum 3 loops (if still below target after 3, flag remaining issues as "requires architectural change")

## Common Fix Sequences

### Bundle Size Quick Wins
1. Add `next/dynamic` to heavy components → +1-2 points
2. Remove barrel re-exports → +1 point
3. Remove unused deps → +1 point

### Database Quick Wins
1. Add `select` to all queries → +1-2 points
2. Add `@@index` on query fields → +1 point
3. Convert sequential queries to Promise.all → +1 point

### RSC Quick Wins
1. Extract client interactivity to leaf components → +1-2 points
2. Add Suspense boundaries → +1 point
3. Add error.tsx files → +1 point
