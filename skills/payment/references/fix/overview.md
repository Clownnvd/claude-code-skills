# Payment Fix — Overview

## Purpose

Take a payment-scoring scorecard (10-category audit) and systematically implement all fixes. Prioritize by severity + weight, apply code changes, verify, and re-score.

## How It Works

```
payment-scoring output -> parse scorecard -> prioritize issues -> apply fixes -> verify -> re-score
```

### Input: payment-scoring Scorecard

The scorecard contains:
- **10 category scores** (0-10 each, weighted to 0-100 total)
- **Letter grade** (A+ to F)
- **Issues list** with severity (CRITICAL / HIGH / MEDIUM / LOW)
- **Quick wins** (highest impact, lowest effort)

### Output: Fixed Codebase + Before/After Comparison

## Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or security risk | Fix immediately — blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next — moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

## Category -> Fix Pattern Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Checkout & Billing, Customer Portal, Pricing | `fix-patterns/checkout-billing.md` |
| Subscription Lifecycle, Metered Billing | `fix-patterns/subscription-lifecycle.md` |
| Webhook Integration, Error Handling | `fix-patterns/webhook-integration.md` |
| Payment Security, Testing, Monitoring | `fix-patterns/security-compliance.md` |

## Files Touched During Fix

| File Type | Examples |
|-----------|---------|
| Stripe config | `src/lib/stripe.ts` |
| Webhook route | `src/app/api/stripe/webhook/route.ts` |
| Checkout route | `src/app/api/stripe/checkout/route.ts` |
| Portal route | `src/app/api/stripe/portal/route.ts` |
| Env validation | `src/lib/env.ts`, `.env.example` |
| Prisma schema | `prisma/schema.prisma` |
| Billing page | `src/app/(app)/billing/page.tsx` |
| Services | `src/lib/stripe/*.ts` |

## Score Targets

| Target | Score | When |
|--------|-------|------|
| Minimum viable | 73+ (C+) | Internal/prototype |
| Production-ready | 87+ (B+) | Public launch |
| Enterprise-grade | 90+ (A-) | Critical systems |

## Integration with payment-scoring

1. Run `payment-scoring` -> get scorecard
2. Run `payment-fix` -> implement fixes from scorecard
3. Run `payment-scoring` again -> verify improvement
4. Repeat if score < target (max 5 iterations)
