# Best Practices for Payment Integration

## Checkout & Billing

### Do
- Always set `success_url` and `cancel_url` with proper redirect handling
- Include `metadata` with userId and business context on every session
- Use `line_items` with Stripe Price IDs (not ad-hoc amounts)
- Set `customer_email` or `customer` to link sessions to users
- Show loading states during checkout redirect
- Handle the `?success=true` and `?canceled=true` query params on return

### Don't
- Don't create checkout sessions without metadata — you cannot link payment to user
- Don't hardcode amounts in checkout — use Stripe Price objects
- Don't skip cancel_url — user gets stuck if they abandon checkout
- Don't trust client-side success param alone — verify via webhook
- Don't create duplicate customers — look up existing customer first

## Subscriptions

### Do
- Check `subscription.status` before granting access (active, trialing)
- Support both immediate and end-of-period cancellation
- Handle proration when switching plans
- Track subscription status in your database, synced via webhooks
- Handle trial_will_end event to send reminders
- Store `stripeCustomerId` and `stripeSubscriptionId` on user record

### Don't
- Don't grant access without checking subscription status
- Don't only support immediate cancellation — users lose remaining paid time
- Don't ignore `past_due` status — payment failed but subscription not yet canceled
- Don't manage subscription state only in Stripe — keep local database in sync
- Don't skip trial support if your pricing includes trials

## Webhooks

### Do
- Always verify webhook signatures with `constructEvent`
- Use `request.text()` for raw body (not `request.json()`)
- Implement idempotency — check event ID before processing
- Return 200 quickly, process heavy work asynchronously
- Handle all critical subscription event types
- Log webhook events for debugging

### Don't
- Don't parse webhook body as JSON without signature verification
- Don't use `request.json()` — it breaks signature verification
- Don't process events without deduplication — Stripe retries
- Don't swallow errors silently — return 500 to trigger Stripe retry
- Don't ignore `invoice.payment_failed` — users need to be notified

## Security

### Do
- Store all Stripe keys in environment variables
- Validate Stripe env vars at startup with Zod
- Use Stripe.js on client-side — never handle raw card numbers
- Validate amounts server-side before creating payment intents
- Use HTTPS for all webhook endpoints
- Rotate API keys periodically

### Don't
- Don't hardcode Stripe keys in source code (sk_test_*, sk_live_*)
- Don't store credit card numbers — rely on Stripe tokens
- Don't expose Stripe secret key to client-side code
- Don't trust client-submitted amounts without server validation
- Don't use the same API keys for development and production
- Don't log full Stripe event payloads (may contain PII)

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| No webhook signature verification | Accepting spoofed events | Add `constructEvent` with raw body |
| Using `request.json()` in webhook | Signature always fails | Switch to `request.text()` |
| No idempotency on webhooks | Duplicate charges/grants | Store processed event IDs |
| Hardcoded Stripe keys | Keys in git history | Move to env vars, rotate keys |
| No subscription status check | Users access without paying | Check `status === 'active'` |
| Missing error handling | Checkout crashes silently | Try/catch with Stripe error types |
| No test mode separation | Accidental live charges in dev | Env-based key selection |
| Trusting client success param | Access without payment | Verify via webhook, not URL param |

## Pre-Deploy Checklist

- [ ] Webhook signature verification with `constructEvent`
- [ ] All Stripe keys in env vars, validated at startup
- [ ] Idempotent webhook processing (event ID dedup)
- [ ] Subscription status checked before granting access
- [ ] Both success_url and cancel_url configured
- [ ] Error handling with specific Stripe error types
- [ ] Test mode / live mode separation
- [ ] Customer portal configured for self-service
- [ ] `.env` in `.gitignore`, `.env.example` committed
- [ ] Stripe CLI tested locally for webhook events
