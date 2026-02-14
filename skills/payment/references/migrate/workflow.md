# Payment Migrate Workflow

## Process

1. **Detect Versions** — Identify Stripe SDK version, @stripe/stripe-js version, API version
2. **Map Breaking Changes**:

| From -> To | Category Affected | Breaking Change | Migration Action |
|-----------|------------------|-----------------|-----------------|
| Stripe v13 -> v14 | Webhook Integration | Event type changes | Update event type casts |
| Stripe v14 -> v15 | Checkout & Billing | Checkout Session API changes | Review session params |
| Stripe v15 -> v17 | All | API version updates | Update apiVersion string |
| @stripe/stripe-js v2 -> v3 | Checkout & Billing | loadStripe changes | Update client init |
| Any | Security | API key format changes | Verify key format |

3. **Apply Migrations** — Preserve webhook handlers, update API calls, verify types
4. **Verify** — Run `pnpm typecheck`, test webhooks with Stripe CLI, check all flows
5. **Re-score** — Ensure no payment quality regression

## Safety Rules

- ALWAYS test webhooks after Stripe SDK upgrade
- Verify API version compatibility with current Stripe account
- Never change webhook route path during migration (breaks active webhooks)
- Test all checkout flows after SDK upgrade
