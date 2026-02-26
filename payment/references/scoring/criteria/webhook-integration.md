# Criteria: Webhook Integration + Error Handling & Recovery

## Category 3: Webhook Integration (12%)

### Signature Verification (3 points)

| Score | Criteria |
|-------|---------|
| +1 | `stripe.webhooks.constructEvent()` used with raw body |
| +1 | Raw body obtained via `request.text()` (not `request.json()`) |
| +1 | Verification failure returns 400 with error logging |
| -1 | No signature verification — accepting unverified payloads (CRITICAL) |
| -1 | Using `request.json()` which breaks signature verification |
| -1 | Verification errors silently swallowed |

### Event Routing (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Switch/map on `event.type` with handlers for all critical events |
| +1 | Type-safe event data casting (`event.data.object as Stripe.Checkout.Session`) |
| -1 | Single handler for all events without type differentiation |
| -1 | Missing handlers for critical events (checkout.session.completed, subscription.updated) |

### Idempotency (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Event ID checked against database before processing (dedup) |
| +1 | Processed events stored in WebhookEvent table with `@unique` on event ID |
| -1 | No deduplication — duplicate events cause duplicate actions |
| -1 | Idempotency key missing on Stripe API calls that modify state |

### Event Coverage (2 points)

| Score | Criteria |
|-------|---------|
| +1 | All subscription lifecycle events handled (created, updated, deleted) |
| +1 | Invoice events handled (payment_succeeded, payment_failed) |
| -1 | Missing critical event handlers — data gets out of sync |

### Response Handling (1 point)

| Score | Criteria |
|-------|---------|
| +1 | 200 returned quickly to Stripe, heavy processing done asynchronously |
| -1 | Slow webhook processing causes Stripe timeout and retries |

---

## Category 7: Error Handling & Recovery (8%)

### Stripe Error Types (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Try/catch around all Stripe API calls |
| +1 | Specific Stripe error types handled (`StripeCardError`, `StripeInvalidRequestError`) |
| +1 | User-friendly error messages (not raw Stripe errors exposed) |
| -1 | No try/catch on Stripe API calls — crashes on any error |
| -1 | Raw Stripe error messages returned to client |

### Retry Logic (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Transient failures (network, rate limit) trigger retry with backoff |
| +1 | Non-retryable errors (invalid card, expired) handled gracefully |
| -1 | No retry logic — transient failures are permanent |
| -1 | All errors treated the same regardless of type |

### Payment Recovery (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Failed payment webhook triggers user notification |
| +1 | Dunning (automatic retry) configured in Stripe |
| +1 | Expired card handling — user prompted to update payment method |
| -1 | Payment failures go unnoticed — no user notification |
| -1 | No recovery path for failed payments |

### Logging (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Structured logging for payment events (not console.log) |
| +1 | Error context includes event ID, customer ID, amount |
| -1 | No payment event logging |
| -1 | Logging includes full card details or sensitive PII |

## Scoring Summary

| Sub-area | Max Points |
|----------|-----------|
| Signature Verification | 3 |
| Event Routing | 2 |
| Idempotency | 2 |
| Event Coverage | 2 |
| Response Handling | 1 |
| **Webhook Integration Total** | **10** |
| Stripe Error Types | 3 |
| Retry Logic | 2 |
| Payment Recovery | 3 |
| Logging | 2 |
| **Error Handling Total** | **10** |
