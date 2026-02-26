# Email Fix -- Implementation Workflow

6-step process. Follow in order for each fix cycle.

## Step 1: Parse Scorecard

Extract from the scorecard:

| Field | Where to Find |
|-------|--------------|
| Total score | `{{TOTAL_SCORE}}/100` line |
| Grade | `{{GRADE}}` line |
| Category scores | Category Scores table, Raw column |
| Issues | Prioritized Issues table |
| Provider notes | Provider Notes table |

Build an issue list:
```
issues = [
  { severity, category, weight, score, issue, files, fix }
]
```

## Step 2: Prioritize Issues

Sort by priority (see `overview.md` priority table):

1. CRITICAL (score 0-3 or security risk) -- any weight
2. HIGH (score 4-5) + weight >= 12%
3. HIGH (score 4-5) + weight < 12%
4. MEDIUM (score 6-7)
5. LOW (score 8)

Within same priority, sort by weight descending.

## Step 3: Load Fix Patterns

For each issue, load the appropriate fix pattern file:

| Issue Category | Load File |
|---------------|-----------|
| Transactional Email, Notification Queue | `fix-patterns/transactional-delivery.md` |
| Email Templates, Testing & Preview | `fix-patterns/templates-rendering.md` |
| Email Provider, Analytics & Tracking | `fix-patterns/provider-integration.md` |
| Deliverability, Bounce, Auth, Rate Limiting | `fix-patterns/security-compliance.md` |

Also load stack-specific references as needed:
- `references/resend-patterns.md` for Resend API patterns
- `references/react-email-patterns.md` for template patterns

## Step 4: Apply Fixes

For each issue in priority order:

1. **Read** the affected files listed in the issue
2. **Find** the matching pattern in the fix pattern file
3. **Apply** the before->after code change
4. **Verify** the fix (see Step 5)
5. **Record** the fix for the report

### Fix Record Format

```
Fix #N: [title]
- Severity: CRITICAL/HIGH/MEDIUM/LOW
- Category: [name] (weight: N%)
- Pattern: fix-patterns/[file].md
- Files: [paths]
- Before: [code snippet]
- After: [code snippet]
- Verification: [result]
```

## Step 5: Verify Each Fix

After each individual fix:

| Check | Command / Action | Pass Criteria |
|-------|-----------------|---------------|
| TypeScript | `npx tsc --noEmit` | Exit 0 |
| Imports | Search for broken imports | No unresolved imports |
| Tests | `pnpm test` | All tests pass |
| Template render | Call `render()` on modified template | Non-empty HTML output |
| Queue roundtrip | Enqueue + verify worker processes | Worker returns 200 |

If verification fails:
1. Revert the failing change
2. Identify the root cause
3. Apply a corrected fix
4. Re-verify

Do NOT proceed to the next fix until the current one passes verification.

## Step 6: Output Fix Report

Fill `assets/templates/fix-report.md.template`:

1. Scoring Input section with before scores
2. Each fix with before/after code
3. Re-Score Results table with all 10 categories
4. Final grade and improvement delta

### Re-Scoring Rules

- Re-score ONLY categories that were fixed
- Unfixed categories retain their original scores
- No category may score LOWER after a fix (flag regression if it does)
- Total must equal sum of all weighted scores

## When to Stop

Stop the fix cycle when:
- All CRITICAL and HIGH issues are resolved
- Target grade is reached (if specified)
- No more issues can be fixed without major refactoring
- A fix introduces a regression that cannot be resolved

## Priority Matrix Quick Reference

```
                    Weight >= 12%    Weight < 12%
CRITICAL (0-3)     Priority 1       Priority 1
HIGH (4-5)         Priority 2       Priority 3
MEDIUM (6-7)       Priority 4       Priority 4
LOW (8)            Priority 5       Priority 5
```
