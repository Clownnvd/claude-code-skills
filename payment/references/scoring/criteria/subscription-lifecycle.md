# Criteria: Subscription Lifecycle + Metered/Usage Billing

## Category 2: Subscription Lifecycle (15%)

### Create & Update (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Trial period support with `trial_period_days` or `trial_end` |
| +1 | Proration configured for mid-cycle plan changes |
| +1 | Plan switching supported with proper amount calculation |
| -1 | No trial support when pricing includes trial |
| -1 | Plan changes not handled — users must cancel and re-subscribe |

### Cancel & Pause (3 points)

| Score | Criteria |
|-------|---------|
| +1 | End-of-period cancellation (`cancel_at_period_end: true`) supported |
| +1 | Immediate cancellation option available for admin/support |
| +1 | Grace period or reactivation window for canceled subscriptions |
| -1 | Only immediate cancel — users lose remaining paid time |
| -1 | No cancel endpoint at all — users stuck in subscription |

### Status Management (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Subscription status checked before granting access (`active`, `trialing`) |
| +1 | All statuses handled: `active`, `past_due`, `canceled`, `trialing`, `incomplete` |
| -1 | Access granted without checking subscription status |
| -1 | `past_due` status ignored — user keeps access despite failed payment |

### Database Sync (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Subscription record in database with `stripeSubscriptionId` and `status` |
| +1 | Status synced via webhooks (not polling or manual) |
| -1 | No local subscription record — relying solely on Stripe API calls |
| -1 | Status synced manually or on page load instead of via webhooks |

---

## Category 8: Metered/Usage Billing (8%)

### Usage Reporting (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Usage records reported to Stripe via `stripe.subscriptionItems.createUsageRecord` |
| +1 | Usage tracked accurately with timestamps and idempotency keys |
| +1 | Usage aggregation matches Stripe price configuration (sum, max, last_during_period) |
| -1 | No usage reporting for metered billing plans |
| -1 | Usage reported without idempotency — risk of double counting |

### Metered Price Setup (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Metered prices created with proper `recurring.usage_type: "metered"` |
| +1 | Billing thresholds configured to prevent unexpected charges |
| +1 | Usage limits enforced application-side before reporting |
| -1 | Metered price misconfigured — wrong aggregation method |
| -1 | No billing thresholds — users can run up unlimited charges |

### Usage Visibility (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Current usage displayed to users in billing dashboard |
| +1 | Usage alerts/notifications when approaching limits |
| -1 | Users cannot see their current usage |

### Overage Handling (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Overage pricing or hard limits configured |
| +1 | Graceful degradation when usage limit reached |
| -1 | No overage handling — service continues or crashes |

## Scoring Summary

| Sub-area | Max Points |
|----------|-----------|
| Create & Update | 3 |
| Cancel & Pause | 3 |
| Status Management | 2 |
| Database Sync | 2 |
| **Subscription Lifecycle Total** | **10** |
| Usage Reporting | 3 |
| Metered Price Setup | 3 |
| Usage Visibility | 2 |
| Overage Handling | 2 |
| **Metered/Usage Billing Total** | **10** |
