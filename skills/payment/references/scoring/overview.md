# Payment Scoring — Overview

## What This Skill Does

Audit any Stripe payment integration (checkout, webhooks, subscriptions, billing) against 10 enterprise-grade criteria weighted by impact. Outputs a scorecard with numeric score (0-100), letter grade, and prioritized issues list.

## How It Works

```
User says "score my payments" or "audit Stripe integration"
  -> Claude loads SKILL.md -> identifies scoring mode
  -> Reads: stripe config, webhook routes, checkout routes, env files
  -> Scores 10 categories (each 0-10, weighted)
  -> Outputs scorecard + issues list ranked by severity
```

## Scoring System

### 10 Categories (Weighted)

| # | Category | Weight | What It Measures |
|---|----------|--------|-----------------|
| 1 | Checkout & Billing Flow | 15% | Session creation, URLs, metadata, line items, UX |
| 2 | Subscription Lifecycle | 15% | Create, update, cancel, pause, status management |
| 3 | Webhook Integration | 12% | Signature verification, event routing, idempotency |
| 4 | Payment Security & PCI | 12% | Key management, PCI compliance, amount validation |
| 5 | Pricing & Plan Management | 10% | Products/prices config, plan switching, proration |
| 6 | Customer Portal | 8% | Portal config, self-service, return URLs |
| 7 | Error Handling & Recovery | 8% | Stripe error types, retry logic, user messaging |
| 8 | Metered/Usage Billing | 8% | Usage records, metered prices, reporting |
| 9 | Testing & Simulation | 6% | Test mode, test clocks, Stripe CLI usage |
| 10 | Monitoring & Analytics | 6% | Payment failure alerts, revenue metrics, logging |

### Grade Scale

| Grade | Range | Meaning |
|-------|-------|---------|
| A+ | 97-100 | Enterprise-ready, all best practices followed |
| A | 93-96 | Production-grade, minor improvements possible |
| A- | 90-92 | Strong, few gaps |
| B+ | 87-89 | Good, some enterprise criteria missing |
| B | 83-86 | Acceptable for production |
| B- | 80-82 | Functional but gaps in security/reliability |
| C+ | 77-79 | Needs work before production |
| C | 73-76 | Significant gaps |
| D | 60-72 | Major issues, not production-ready |
| F | <60 | Critical problems, immediate action needed |

### Anti-Bias Rules

- Start every category at 5/10 (neutral baseline)
- Subtract for missing items, add for evidence of best practices
- 9-10 requires concrete evidence (actual webhook handlers, constructEvent calls, error handling)
- Never give 10/10 without verifying implementation exists in code

## Scorecard Format

```markdown
## Payment Scorecard — [Project Name]

| # | Category | Score | Weight | Weighted |
|---|----------|-------|--------|----------|
| 1 | Checkout & Billing | 7/10 | 15% | 10.5 |
| ... | ... | ... | ... | ... |
| **Total** | | | | **72/100** |

**Grade: D**

### Issues (by priority)
1. [CRITICAL] No webhook signature verification — accepting unverified payloads
2. [HIGH] Missing error handling on checkout — Stripe errors crash the route
3. [MEDIUM] No customer portal configured — users cannot self-manage
4. [LOW] No test clock usage — subscription lifecycle untested
```

## File Structure

```
payment/
├── SKILL.md                              — Entry point, category table, grade scale
├── LICENSE.txt                           — Apache 2.0
├── references/
│   ├── overview.md                       — This file
│   ├── best-practices.md                 — Do/Don't for payments
│   ├── scoring-workflow.md               — Step-by-step audit process
│   ├── criteria/
│   │   ├── checkout-billing.md           — Checkout + Portal + Pricing criteria
│   │   ├── subscription-lifecycle.md     — Subscriptions + Metered billing criteria
│   │   ├── webhook-integration.md        — Webhooks + Error Handling criteria
│   │   └── security-compliance.md        — Security + Testing + Monitoring criteria
│   ├── stripe-patterns.md               — Stripe SDK patterns
│   └── webhook-patterns.md              — Webhook verification patterns
```

## Integration Points

- **Stripe config**: `src/lib/stripe.ts` — SDK initialization, API version
- **Webhook route**: `src/app/api/stripe/webhook/route.ts` — event handling
- **Checkout route**: `src/app/api/stripe/checkout/route.ts` — session creation
- **Env files**: `.env`, `.env.example` — STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
- **Prisma schema**: `prisma/schema.prisma` — subscription/payment models
