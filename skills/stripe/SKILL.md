---
name: stripe
description: Use when integrating Stripe payments in Next.js. Checkout Sessions, Payment Intents, Subscriptions, Webhooks, Customer Portal, Connect, Tax, Radar. Setup, implementation, testing, security patterns.
---

# Stripe — Next.js App Router

Complete Stripe integration patterns for Next.js App Router with Server Actions and Route Handlers.

## Setup

```bash
npm install stripe @stripe/stripe-js @stripe/react-stripe-js
```

| Env Variable | Value | Exposed to Client |
|-------------|-------|-------------------|
| `STRIPE_SECRET_KEY` | `sk_test_...` or `sk_live_...` | NO |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | `pk_test_...` or `pk_live_...` | Yes |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` | NO |
| `NEXT_PUBLIC_APP_URL` | `http://localhost:3000` | Yes |

Load `references/setup.md` for SDK initialization patterns.

## Quick Patterns

| Task | Approach | Reference |
|------|----------|-----------|
| One-time payment | Checkout Session → redirect to Stripe | `references/checkout.md` |
| Custom payment UI | Payment Intents + Stripe Elements | `references/payment-intents.md` |
| Recurring billing | Subscriptions + Invoices | `references/subscriptions.md` |
| Receive events | Webhook Route Handler | `references/webhooks.md` |
| Self-service billing | Customer Portal session | `references/customer-portal.md` |
| Products & pricing | Products + Prices API | `references/products-prices.md` |
| Marketplace splits | Stripe Connect | `references/connect.md` |
| Auto tax calc | Stripe Tax | `references/tax.md` |
| Fraud prevention | Radar rules + 3D Secure | `references/radar-fraud.md` |
| Usage-based billing | Billing Meter + usage records | `references/billing-meter.md` |

## Essential Webhook Events

| Event | When | Action |
|-------|------|--------|
| `checkout.session.completed` | Payment captured | Fulfill order |
| `invoice.paid` | Subscription renewed | Extend access |
| `invoice.payment_failed` | Payment failed | Notify user, retry |
| `customer.subscription.updated` | Plan changed | Update entitlements |
| `customer.subscription.deleted` | Cancelled | Revoke access |
| `payment_intent.succeeded` | Custom flow completed | Confirm order |
| `charge.dispute.created` | Dispute opened | Alert + evidence |

Load `references/webhooks.md` for handler implementation.

## Test Cards

| Number | Result |
|--------|--------|
| `4242 4242 4242 4242` | Success |
| `4000 0000 0000 0002` | Generic decline |
| `4000 0000 0000 9995` | Insufficient funds |
| `4000 0000 0000 0069` | Expired card |
| `4000 0025 0000 3155` | 3D Secure required |
| `4000 0000 0000 3220` | 3D Secure 2 required |

Load `references/testing.md` for full test cards + Stripe CLI workflow.

## Stripe CLI

```bash
stripe login
stripe listen --forward-to localhost:3000/api/webhooks/stripe
stripe trigger checkout.session.completed
stripe trigger invoice.payment_failed
stripe logs tail --filter status:400
```

## Templates

| Template | Description |
|----------|-------------|
| `templates/stripe-setup.ts` | Server + client Stripe initialization |
| `templates/webhook-handler.ts` | Complete webhook Route Handler |
| `templates/checkout-action.ts` | Server Action: Checkout Session |
| `templates/subscription-action.ts` | Server Actions: subscription CRUD |
| `templates/customer-portal-action.ts` | Server Action: portal session |
| `templates/env-example.txt` | `.env.example` with all Stripe vars |

## Error Handling

Load `references/error-handling.md` for Stripe error types and retry patterns.

## Security

Load `references/security.md` for PCI compliance, idempotency, and key management.

## All References

- `references/setup.md` — SDK init, singleton, TypeScript config
- `references/checkout.md` — Checkout Sessions, hosted vs embedded
- `references/payment-intents.md` — Payment Intents, 3D Secure, capture
- `references/subscriptions.md` — Recurring billing, trials, proration
- `references/webhooks.md` — Signature verification, event routing, idempotency
- `references/customer-portal.md` — Self-service portal setup
- `references/products-prices.md` — Products, Prices, coupons, promo codes
- `references/connect.md` — Marketplace, platform fees, payouts
- `references/tax.md` — Automatic tax calculation
- `references/radar-fraud.md` — Fraud detection, disputes
- `references/billing-meter.md` — Usage-based billing
- `references/error-handling.md` — Error types, retry logic
- `references/testing.md` — Test cards, CLI, test clocks
- `references/security.md` — PCI, keys, idempotency, CSP
