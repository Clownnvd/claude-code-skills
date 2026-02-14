# Payment Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| Checkout & Billing (15%) | Integration | Session created with URLs, metadata, line items |
| Subscription Lifecycle (15%) | Integration | Create, cancel, status checks, DB sync |
| Webhook Integration (12%) | Integration | Signature verification, event routing, idempotency |
| Payment Security (12%) | Unit | Env validation, key format, no hardcoded secrets |
| Pricing & Plans (10%) | Integration | Prices fetched, plan switching works |
| Customer Portal (8%) | Integration | Portal session created with return URL |
| Error Handling (8%) | Unit | Stripe error types caught, user-friendly messages |
| Metered Billing (8%) | Integration | Usage records created, limits enforced |
| Testing (6%) | Unit | Test mode detection, test key validation |
| Monitoring (6%) | Unit | Payment events logged, structured format |

2. **Generate Test Files**:
   - `__tests__/stripe/webhook.test.ts` — Signature verification + event routing
   - `__tests__/stripe/checkout.test.ts` — Session creation + error handling
   - `__tests__/stripe/subscription.test.ts` — Lifecycle + status checks
   - `__tests__/stripe/security.test.ts` — Env validation + key management

3. **Output** — Test files + coverage matrix
