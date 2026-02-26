# Criteria: Payment Security & PCI + Testing + Monitoring

## Category 4: Payment Security & PCI (12%)

### API Key Management (3 points)

| Score | Criteria |
|-------|---------|
| +1 | All Stripe keys stored in environment variables |
| +1 | Zod validation of Stripe env vars at startup |
| +1 | Key rotation process documented or automated |
| -1 | Hardcoded Stripe keys in source code (CRITICAL) |
| -1 | No env var validation — app silently fails |
| -1 | Same keys used for development and production |

### PCI Compliance (2 points)

| Score | Criteria |
|-------|---------|
| +1 | No raw card data handled server-side — using Stripe.js / Elements |
| +1 | Card tokenization via Stripe client-side SDK only |
| -1 | Server-side code handles raw card numbers (CRITICAL) |
| -1 | Card data stored in application database |

### Amount Validation (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Amounts validated server-side before creating payment intents |
| +1 | Price IDs used instead of client-submitted amounts |
| -1 | Client can submit arbitrary amounts to checkout endpoint |
| -1 | No server-side validation of payment amounts |

### Access Control (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Checkout/billing endpoints require authentication |
| +1 | Users can only manage their own subscriptions (not others) |
| -1 | Unauthenticated access to payment endpoints |
| -1 | No ownership check — user A can cancel user B subscription |

### Secret Protection (1 point)

| Score | Criteria |
|-------|---------|
| +1 | `.env` in `.gitignore`, `.env.example` committed without real values |
| -1 | Real keys committed to git history |

---

## Category 9: Testing & Simulation (6%)

### Test Mode Separation (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Environment-based key selection (test keys for dev, live for prod) |
| +1 | Test mode checks prevent accidental live charges in development |
| +1 | Separate Stripe webhook endpoints for test and live |
| -1 | Same Stripe key used in all environments |
| -1 | No safeguard against live charges in development |

### Test Clocks (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Stripe Test Clocks used for subscription lifecycle testing |
| +1 | Trial expiration, renewal, and cancellation tested via time advance |
| +1 | Edge cases tested: past_due, incomplete, payment failure |
| -1 | No test clock usage — subscription lifecycle untested |

### Stripe CLI Usage (2 points)

| Score | Criteria |
|-------|---------|
| +1 | `stripe listen --forward-to` used for local webhook testing |
| +1 | `stripe trigger` used to test specific event flows |
| -1 | Webhooks never tested locally |

### Test Data (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Test card numbers used in integration tests (4242...) |
| +1 | Failure scenarios tested (declined card, insufficient funds) |
| -1 | No integration tests for payment flows |

---

## Category 10: Monitoring & Analytics (6%)

### Payment Failure Alerts (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Payment failure events trigger alerts (email, Slack, Sentry) |
| +1 | Subscription churn tracked (cancellations, failed renewals) |
| +1 | Webhook delivery failures monitored |
| -1 | Payment failures go unnoticed |

### Revenue Metrics (3 points)

| Score | Criteria |
|-------|---------|
| +1 | MRR (Monthly Recurring Revenue) tracked or calculable |
| +1 | Conversion rate from checkout to active subscription tracked |
| +1 | Revenue per plan tier visible in dashboard or analytics |
| -1 | No revenue visibility |

### Operational Monitoring (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Stripe API error rates monitored |
| +1 | Webhook processing latency tracked |
| -1 | No operational metrics for payment system |

### Audit Trail (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Payment events logged with timestamps and correlation IDs |
| +1 | Subscription state changes auditable |
| -1 | No audit trail for payment actions |

## Scoring Summary

| Sub-area | Max Points |
|----------|-----------|
| API Key Management | 3 |
| PCI Compliance | 2 |
| Amount Validation | 2 |
| Access Control | 2 |
| Secret Protection | 1 |
| **Payment Security Total** | **10** |
| Test Mode Separation | 3 |
| Test Clocks | 3 |
| Stripe CLI Usage | 2 |
| Test Data | 2 |
| **Testing Total** | **10** |
| Payment Failure Alerts | 3 |
| Revenue Metrics | 3 |
| Operational Monitoring | 2 |
| Audit Trail | 2 |
| **Monitoring Total** | **10** |
