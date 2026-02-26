# Email Fix -- Verification

Post-fix checklist, re-scoring protocol, comparison template, and iteration decision.

## Post-Fix Checklist

Run after ALL fixes in a cycle are applied:

### Compilation

- [ ] `npx tsc --noEmit` exits 0
- [ ] No unused imports or variables
- [ ] All email-related types resolve correctly

### Functionality

- [ ] Email service functions callable without runtime errors
- [ ] Templates render to non-empty HTML via `render()`
- [ ] Queue client initializes with valid token
- [ ] Worker endpoint returns 200 on valid payload
- [ ] Webhook endpoint verifies Svix signature correctly

### Tests

- [ ] `pnpm test` -- all existing tests pass
- [ ] No test regressions from fix changes
- [ ] New tests added for new functionality (if applicable)

### Environment

- [ ] All new env vars added to `.env.example`
- [ ] No secrets committed to repository
- [ ] Env var validation throws at startup if missing

### Email Delivery

- [ ] From address uses verified domain
- [ ] Suppression list checked before send (if implemented)
- [ ] Rate limiting active on email-triggering endpoints (if implemented)

## Re-Scoring Protocol

1. Run the full scoring workflow from `scoring/scoring-workflow.md`
2. Use the SAME criteria files as the original scoring
3. Score each category independently -- do not reference the original scores
4. Compare results using the comparison template below

### Comparison Template

```
| Category | Before | After | Delta | Status |
|----------|--------|-------|-------|--------|
| Transactional Email (15%) | X/10 | Y/10 | +N | IMPROVED / UNCHANGED / REGRESSED |
| Email Templates (12%) | X/10 | Y/10 | +N | ... |
| Notification Queue (12%) | X/10 | Y/10 | +N | ... |
| Email Provider (12%) | X/10 | Y/10 | +N | ... |
| Deliverability (10%) | X/10 | Y/10 | +N | ... |
| Bounce Handling (10%) | X/10 | Y/10 | +N | ... |
| Email Auth (8%) | X/10 | Y/10 | +N | ... |
| Rate Limiting (8%) | X/10 | Y/10 | +N | ... |
| Analytics (7%) | X/10 | Y/10 | +N | ... |
| Testing (6%) | X/10 | Y/10 | +N | ... |

Total: X/100 -> Y/100 (+N)
Grade: X -> Y
```

## Regression Detection

A regression occurs when any category score DECREASES after fixes.

If regression detected:
1. **STOP** -- do not continue with more fixes
2. Identify which fix caused the regression
3. Check for broken imports, removed functionality, or side effects
4. Revert the offending fix or correct it
5. Re-verify and re-score

Common regression causes:
- Moving email service functions breaks import paths in triggers
- Refactoring templates removes required content
- Adding queue but forgetting to create the worker endpoint
- Changing from address to unverified domain

## Iteration Decision

After re-scoring, decide whether to iterate:

| Condition | Decision |
|-----------|----------|
| Target grade reached | STOP -- output final report |
| Score improved and CRITICAL/HIGH remain | CONTINUE -- fix remaining issues |
| Score unchanged after full fix cycle | STOP -- plateau reached |
| Score decreased (regression) | STOP -- investigate regression |
| Max iterations (5) reached | STOP -- output best result |

### Loop Mode Specifics

When running in loop mode (score -> fix -> re-score):
- Default target: B+ (87+)
- Max iterations: 5
- Stop on plateau: score unchanged between iterations
- Each iteration should fix at least 1 CRITICAL or 2 HIGH issues
- If only MEDIUM/LOW remain, evaluate if further iteration is worth it

## Final Report Checklist

Before outputting the fix report:
- [ ] All fix entries have before/after code
- [ ] Re-score table shows all 10 categories
- [ ] No regressions (all deltas >= 0)
- [ ] Final grade and score are correct
- [ ] Fix pattern references listed
- [ ] Verification results documented per fix
