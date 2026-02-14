# Verification & Re-Scoring

## Post-Fix Verification Checklist

### 1. TypeScript
```bash
pnpm typecheck
```
Must pass with zero errors. Stripe SDK type changes may require updating event type casts.

### 2. Tests
```bash
pnpm test
```
All existing tests must pass. No regressions. If new payment logic added, add tests.

### 3. Build
```bash
pnpm build
```
Build must succeed. Watch for:
- Missing imports (Stripe types, new utility functions)
- Env var references that changed names
- Route handler signature changes

### 4. Webhook Verification
```bash
stripe listen --forward-to localhost:3000/api/stripe/webhook
```
In a separate terminal:
```bash
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
```
All events should process with 200 response. Check logs for errors.

### 5. Checkout Flow Test
```bash
# Start dev server
pnpm dev
# Navigate to checkout page, complete test purchase with card 4242 4242 4242 4242
# Verify success redirect, webhook processing, database update
```

## Re-Scoring Protocol

After all fixes pass verification, invoke `payment-scoring` skill to produce a new scorecard.

### Comparison Template

```markdown
## Fix Results: Payment Audit

### Score Comparison
| # | Category | Weight | Before | After | Delta |
|---|----------|--------|--------|-------|-------|
| 1 | Checkout & Billing | 15% | X/10 | Y/10 | +Z |
| 2 | Subscription Lifecycle | 15% | X/10 | Y/10 | +Z |
| 3 | Webhook Integration | 12% | X/10 | Y/10 | +Z |
| 4 | Payment Security | 12% | X/10 | Y/10 | +Z |
| 5 | Pricing & Plans | 10% | X/10 | Y/10 | +Z |
| 6 | Customer Portal | 8% | X/10 | Y/10 | +Z |
| 7 | Error Handling | 8% | X/10 | Y/10 | +Z |
| 8 | Metered Billing | 8% | X/10 | Y/10 | +Z |
| 9 | Testing | 6% | X/10 | Y/10 | +Z |
| 10 | Monitoring | 6% | X/10 | Y/10 | +Z |
| **Total** | | | **XX/100** | **YY/100** | **+ZZ** |
| **Grade** | | | **D** | **B+** | |

### Fixes Applied (N total)
1. [Description] — [files changed]

### Remaining Issues
1. [Issue] — [reason not fixed]

### Score Target Met?
- [ ] Target: >= B+ (87+)
- [ ] All CRITICALs resolved
- [ ] No new issues introduced
```

## Score Targets

| Target | Score | When |
|--------|-------|------|
| Minimum viable | 73+ (C+) | Internal/prototype |
| Production-ready | 87+ (B+) | Public launch |
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
2. Track iteration count (max 5)
3. Track score delta per iteration — if delta = 0 for 2 consecutive, stop
4. Final output: full before/after comparison across ALL iterations

## Commit Message Template

```
fix(payment): improve payment score from XX to YY

- [Fix 1 description]
- [Fix 2 description]
- [Fix N description]

Score: XX/100 (D) -> YY/100 (B+)
```
