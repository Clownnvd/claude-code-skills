# Implementation Workflow

## Step 1: Parse Scorecard

Extract from the infra-scoring output:
- Per-category scores (0-10)
- Issues list with severity, file:line, description
- Current total and grade

## Step 2: Prioritize

Sort issues by: `severity_weight * category_weight`

| Severity | Weight |
|----------|--------|
| CRITICAL | 4 |
| HIGH | 3 |
| MEDIUM | 2 |
| LOW | 1 |

Example: CRITICAL in CI Pipeline (15%) = 4 * 15 = 60 priority score
Example: MEDIUM in IaC (4%) = 2 * 4 = 8 priority score

## Step 3: Fix (top-down)

For each issue, load the relevant fix pattern file:

| Category | Fix Pattern |
|----------|------------|
| CI Pipeline | `fix-patterns/ci-cd.md` |
| CD Pipeline | `fix-patterns/ci-cd.md` |
| Production Deploy | `fix-patterns/deploy-container.md` |
| Containerization | `fix-patterns/deploy-container.md` |
| Environment Mgmt | `fix-patterns/env-monitoring.md` |
| Monitoring | `fix-patterns/env-monitoring.md` |
| Backup/DR | `fix-patterns/backup-integrations.md` |
| Third-Party | `fix-patterns/backup-integrations.md` |
| IaC | `fix-patterns/iac-security.md` |
| Deploy Security | `fix-patterns/iac-security.md` |

## Step 4: Apply Fix

1. Read the target file
2. Apply the fix pattern
3. Verify the fix compiles (`tsc --noEmit`)
4. Run related tests if any

## Step 5: Verify All

After all fixes applied:
```bash
pnpm typecheck    # 0 errors
pnpm test:run     # all pass
pnpm build        # builds successfully
```

## Step 6: Re-Score

Run `infra-scoring` again to verify score improvement. If target not met, repeat from Step 2 with remaining issues.

## Loop Mode

If target score not reached after first pass:
1. Re-score to get updated scorecard
2. Identify remaining issues
3. Apply next round of fixes
4. Verify and re-score again
5. Maximum 5 iterations before reporting remaining issues to user
