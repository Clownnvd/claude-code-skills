# Implementation Workflow

## Step 1: Parse Scorecard

Extract from the payment-scoring output:
- **Scorecard table** — 10 category scores + weighted total + grade
- **CRITICAL issues** — must fix before deploy (score 0-3 or security risk)
- **HIGH issues** — fix this sprint (score 4-5, weight >= 12%)
- **MEDIUM issues** — fix next sprint
- **LOW issues** — backlog
- **Quick wins** — highest delta per effort

## Step 2: Prioritize

Fix order: CRITICAL -> HIGH -> MEDIUM -> LOW.

Within each severity, prioritize by:
1. **Weight** — higher-weight categories first (Checkout 15% > Monitoring 6%)
2. **Blast radius** — fixes affecting multiple routes/handlers before single-file fixes
3. **Dependencies** — fixes that unblock other fixes first (e.g., env validation before webhook verification)

### Priority Matrix

| Severity x Weight | Action |
|-------------------|--------|
| CRITICAL + any weight | Fix immediately, block other work |
| HIGH + weight >= 12% | Fix next, these move the score most |
| HIGH + weight < 12% | Fix after high-weight items |
| MEDIUM | Fix if time allows |
| LOW | Skip unless targeting A+ |

## Step 3: Execute Fixes

For each fix:

### 3a. Read Before Edit
- Read the target file(s) — webhook route, checkout route, stripe config
- Read `src/lib/env.ts` if fix involves env vars
- Read `src/lib/stripe.ts` if fix involves SDK configuration

### 3b. Apply Fix
- Use Edit tool for surgical changes (prefer over full Write)
- Follow project coding style (TypeScript, immutable patterns)
- Load the relevant `references/fix-patterns/` file for the category

### 3c. Verify Each Fix
- Run `pnpm typecheck` after type/Stripe changes
- Run `pnpm test` after logic changes
- Read the modified file to confirm correctness

## Step 4: Webhook Sync (if webhook route changed)

If any webhook route changes were made:
1. Run `stripe listen --forward-to localhost:3000/api/stripe/webhook`
2. Trigger test events: `stripe trigger checkout.session.completed`
3. Verify events process correctly and return 200

## Step 5: Batch Verification

After all fixes:
1. `pnpm typecheck` — 0 errors
2. `pnpm test` — all pass, no regressions
3. `pnpm build` — builds successfully

## Step 6: Re-Score

Invoke `payment-scoring` skill to produce new scorecard.

### Before/After Comparison Template

```
## Fix Results: Payment Audit

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
1. [Fix description] — [files changed]

### Remaining Issues
1. [Issue] — [reason: needs Stripe Dashboard access / design decision / external dependency]
```

## Which Fix-Pattern References to Load

| Scorecard Category | Load |
|-------------------|------|
| Checkout & Billing, Customer Portal, Pricing | `fix-patterns/checkout-billing.md` |
| Subscription Lifecycle, Metered Billing | `fix-patterns/subscription-lifecycle.md` |
| Webhook Integration, Error Handling | `fix-patterns/webhook-integration.md` |
| Payment Security, Testing, Monitoring | `fix-patterns/security-compliance.md` |
