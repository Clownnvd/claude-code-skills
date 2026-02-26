# Payment Review Workflow

## Process

1. **Read** — Load target file(s): webhook route, checkout route, stripe config, billing page
2. **Classify** — Determine applicable categories:
   - Webhook route -> Webhook Integration, Error Handling, Security, Idempotency
   - Checkout route -> Checkout & Billing, Security, Error Handling
   - Stripe config -> Security, Testing, Monitoring
   - Billing page -> Pricing, Customer Portal, UX
3. **Score** — Rate each applicable category 0-10
4. **Annotate** — Cite line numbers, explain issues
5. **Suggest** — Concrete fixes with TypeScript/Stripe syntax
6. **Summarize** — Score, priorities, quick wins

## Common Payment Issues

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | No webhook signature verification | Webhook Integration | CRITICAL |
| 2 | Hardcoded Stripe keys | Payment Security | CRITICAL |
| 3 | No error handling on Stripe calls | Error Handling | HIGH |
| 4 | Missing subscription status checks | Subscription Lifecycle | HIGH |
| 5 | No idempotency on webhooks | Webhook Integration | HIGH |
| 6 | Missing checkout metadata | Checkout & Billing | MEDIUM |
| 7 | No customer portal | Customer Portal | MEDIUM |
| 8 | No test mode separation | Testing | MEDIUM |
