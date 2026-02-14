# Best Practices for Payment Fixes

## Fix Discipline

### Do
- Read the file completely before editing — understand surrounding code
- Fix one issue at a time — commit each fix separately when possible
- Run `pnpm typecheck` after every Stripe-related change
- Test webhooks with Stripe CLI after webhook route changes
- Update `.env.example` when adding new Stripe env vars
- Update `src/lib/env.ts` when adding new env vars
- Verify signature verification still works after webhook changes
- Test checkout flow end-to-end after checkout route changes

### Don't
- Don't batch unrelated fixes into one giant edit
- Don't modify webhook handler without testing with Stripe CLI
- Don't change Stripe API version without checking breaking changes
- Don't add payment logic to client components — keep server-side
- Don't skip error handling on any Stripe API call
- Don't hardcode price IDs — use env vars or config
- Don't trust client-submitted amounts
- Don't log full Stripe event payloads (PII risk)

## Safe vs Dangerous Changes

### Safe Changes (no payment disruption)
| Change | Risk | Procedure |
|--------|------|-----------|
| Add error handling to existing route | None | Add try/catch, test |
| Add env var validation | None | Add Zod schema, update .env.example |
| Add idempotency to webhook | None | Add event ID check, create WebhookEvent model |
| Add customer portal endpoint | None | New route, no existing code modified |
| Add logging to webhook handler | None | Additive change only |

### Dangerous Changes (potential payment disruption)
| Change | Risk | Procedure |
|--------|------|-----------|
| Change webhook route path | Active webhooks break | Update Stripe Dashboard -> test -> deploy |
| Change Stripe API version | API behavior changes | Review changelog -> test all flows -> deploy |
| Modify checkout session params | Checkout may fail | Test in Stripe test mode first |
| Change subscription model schema | Data loss | Backup -> migrate -> verify |
| Modify webhook signature verification | Events rejected | Test with Stripe CLI before deploy |

## Webhook Fix Patterns

### When to modify webhook handler
- Adding new event type handlers: SAFE
- Fixing signature verification: CRITICAL but safe (adding, not removing)
- Changing event processing logic: test with Stripe CLI first
- Modifying response codes: test that Stripe receives 200 for success

### When NOT to modify webhook handler
- During active deployment (webhook deliveries in flight)
- Without Stripe CLI available for testing
- Without understanding current event processing flow

## Checkout Fix Patterns

### When to modify checkout route
- Adding metadata: SAFE (additive)
- Changing success/cancel URLs: test redirect flow
- Adding line items: test full checkout flow
- Changing mode (payment vs subscription): verify all downstream handlers

## Env Var Sync Checklist

When adding a new Stripe env var, update ALL of these:
1. `.env.example` — with placeholder value (sk_test_xxx, whsec_xxx)
2. `src/lib/env.ts` — Zod schema validation
3. `src/lib/stripe.ts` — if new var affects SDK init
4. Deployment platform (Vercel/Railway env settings)

## Common Fix Mistakes

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Using `request.json()` in webhook | Signature verification always fails | Always use `request.text()` for raw body |
| No try/catch on Stripe calls | Route crashes on any Stripe error | Wrap every Stripe call in try/catch |
| Hardcoding webhook secret | Different per environment | Use `process.env.STRIPE_WEBHOOK_SECRET` |
| Not testing after fix | Fix introduces new bug | Run Stripe CLI + typecheck + test |
| Changing live webhook URL | Active webhooks fail delivery | Update Stripe Dashboard, test, then deploy |
| Adding event handler without DB sync | Data inconsistency | Always sync Stripe state to local DB |
| Removing error handler instead of fixing | Errors silently swallowed | Fix error handling, don't remove it |

## Fix Verification Order

Always verify in this order:
1. `pnpm typecheck` — catches Stripe type mismatches
2. `pnpm test` — catches logic regressions
3. `stripe listen --forward-to localhost:3000/api/stripe/webhook` — webhook test
4. `stripe trigger checkout.session.completed` — end-to-end test
5. `pnpm build` — catches build-time issues
