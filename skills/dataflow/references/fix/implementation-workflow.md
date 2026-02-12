# Data Flow Fix — Implementation Workflow

## Step 1: Parse Scorecard

Extract from dataflow-scoring output:
- Per-category scores (identify < 10)
- Issues list with severity
- Affected files

## Step 2: Prioritize

Sort issues by: `severity * category_weight`

| Priority | What to fix |
|----------|------------|
| P1 | CRITICAL in any category |
| P2 | HIGH in 15% categories (API, RSC) |
| P3 | HIGH in 10-12% categories (Prisma, Cache, Types, Composition) |
| P4 | MEDIUM in any category |
| P5 | LOW (backlog) |

## Step 3: Load Fix Patterns

For each issue, load the corresponding fix-patterns file:

| Category | Fix Patterns File |
|----------|------------------|
| RSC Fetching + Composition | `fix-patterns/rsc-composition.md` |
| Prisma + API Routes | `fix-patterns/prisma-api.md` |
| State + Caching | `fix-patterns/state-cache.md` |
| Types + Errors | `fix-patterns/types-errors.md` |
| Forms + DTOs | `fix-patterns/forms-dtos.md` |

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

Run dataflow-scoring again on fixed code. Output comparison:

```markdown
| # | Category | Before | After | Delta |
|---|----------|--------|-------|-------|
| 1 | RSC Fetching (15%) | X/10 | Y/10 | +Z |
| ... | | | | |
| **Total** | | **XX/100** | **YY/100** | **+ZZ** |
```
