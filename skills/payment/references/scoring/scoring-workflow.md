# Payment Scoring — Audit Workflow

## Step 1: Gather Files

Read these files (in order of priority):

| File | What to Look For |
|------|-----------------|
| `src/lib/stripe.ts` | Stripe SDK initialization, API version, singleton pattern |
| `src/app/api/stripe/webhook/route.ts` | Signature verification, event routing, idempotency |
| `src/app/api/stripe/checkout/route.ts` | Session creation, URLs, metadata, line items |
| `src/app/api/stripe/portal/route.ts` | Customer portal session, return URL |
| `prisma/schema.prisma` | Subscription model, payment records, webhook events |
| `.env.example` | STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY |
| `src/lib/env.ts` | Zod validation of Stripe env vars |
| `src/app/(app)/billing/page.tsx` | Pricing display, plan selection, portal link |

## Step 2: Score Each Category

For each of the 10 categories:

1. Start at **5/10** (neutral baseline)
2. Read the relevant criteria file from `criteria/`
3. Check each item on the checklist
4. **Subtract 1** for each missing critical item
5. **Add 1** for each best practice found with evidence
6. Cap at 0 minimum, 10 maximum
7. Require **concrete evidence** for scores 9-10

### Category -> Criteria File Mapping

| Categories | Criteria Reference |
|-----------|-------------------|
| Checkout & Billing (1), Customer Portal (6), Pricing (5) | `criteria/checkout-billing.md` |
| Subscription Lifecycle (2), Metered Billing (8) | `criteria/subscription-lifecycle.md` |
| Webhook Integration (3), Error Handling (7) | `criteria/webhook-integration.md` |
| Payment Security (4), Testing (9), Monitoring (10) | `criteria/security-compliance.md` |

### Stack-Specific Adjustments

| If Using... | Also Load |
|------------|-----------|
| Stripe | `stripe-patterns.md` — SDK init, Products/Prices, Checkout, Portal |
| Next.js App Router | `webhook-patterns.md` — route handlers, raw body, signature verification |

## Step 3: Calculate Weighted Score

```
weighted_score = sum(category_score * weight) for each category
grade = lookup(weighted_score) from grade table
```

| Weight | Categories |
|--------|-----------|
| 15% | Checkout & Billing, Subscription Lifecycle |
| 12% | Webhook Integration, Payment Security |
| 10% | Pricing & Plan Management |
| 8% | Customer Portal, Error Handling, Metered Billing |
| 6% | Testing & Simulation, Monitoring & Analytics |

## Step 4: Generate Issues List

Classify each finding:

| Severity | Criteria | Examples |
|----------|----------|---------|
| CRITICAL | Score 0-3 or security risk | No webhook verification, hardcoded keys, no auth |
| HIGH | Score 4-5 | Missing error handling, no subscription sync |
| MEDIUM | Score 6-7 | No portal config, missing test mode |
| LOW | Score 8, minor improvement | Could add usage billing, missing analytics |

### Issue Format

```markdown
[SEVERITY] Short description
  File: path/to/file.ts:line
  Current: What exists now
  Expected: What should be there
  Fix: Concrete action to take
```

## Step 5: Output Scorecard

Use the scorecard template from `assets/templates/scorecard.md.template`. Include:

1. **Score table** — all 10 categories with scores, weights, weighted totals
2. **Final score and grade**
3. **Issues list** — sorted by severity (CRITICAL -> HIGH -> MEDIUM -> LOW)
4. **Quick wins** — top 3 changes that would most improve the score
5. **Stripe config notes** — SDK version, webhook status, test mode

## Step 6: Re-Score (Optional)

After fixes are applied:
1. Re-read modified files
2. Re-score only affected categories
3. Show before/after comparison
4. Stop when target grade reached or delta = 0 for 2 rounds
