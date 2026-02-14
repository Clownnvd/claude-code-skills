# Criteria: Checkout & Billing Flow + Customer Portal + Pricing

## Category 1: Checkout & Billing Flow (15%)

### Session Creation (3 points)

| Score | Criteria |
|-------|---------|
| +1 | `success_url` and `cancel_url` configured with proper app URLs |
| +1 | `metadata` includes userId and business context on every session |
| +1 | `line_items` use Stripe Price IDs (not ad-hoc amounts) |
| -1 | Missing success_url or cancel_url — user gets stuck |
| -1 | No metadata — cannot link payment to user in webhook |

### Payment Methods (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Multiple payment method types configured or `automatic_payment_methods` enabled |
| +1 | Currency properly set, matching target market |
| -1 | Only single payment method with no fallback |
| -1 | Hardcoded amounts instead of Stripe Price objects |

### Billing Flow UX (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Loading states shown during checkout redirect |
| +1 | Success/cancel pages handle query params and show appropriate messaging |
| -1 | No loading state — user clicks button and nothing visible happens |
| -1 | Success page trusts URL param alone without webhook verification |

### Invoice Handling (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Invoice generation configured for subscription payments |
| +1 | Invoice PDF accessible to customers |
| -1 | No invoice records accessible to users |

### Customer Linking (1 point)

| Score | Criteria |
|-------|---------|
| +1 | Existing Stripe customer looked up before creating new (dedup) |
| -1 | New customer created on every checkout — duplicates |

---

## Category 6: Customer Portal (8%)

### Portal Configuration (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Billing portal session creation endpoint exists |
| +1 | Portal configured with subscription management features |
| +1 | `return_url` set to proper billing/account page |
| -1 | No portal endpoint — users cannot self-manage |
| -1 | Portal creates but has no features enabled |

### Self-Service Features (4 points)

| Score | Criteria |
|-------|---------|
| +1 | Subscription cancellation available through portal |
| +1 | Plan switching/upgrade available through portal |
| +1 | Payment method update available through portal |
| +1 | Invoice history visible in portal |
| -1 | Users must contact support for basic billing changes |

### Portal Integration (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Portal link accessible from app billing/settings page |
| +1 | Portal styled to match application branding |
| +1 | Return URL properly handles post-portal state |
| -1 | No visible way for users to access portal |

---

## Category 5: Pricing & Plan Management (10%)

### Price Configuration (4 points)

| Score | Criteria |
|-------|---------|
| +1 | Products and Prices created in Stripe (not hardcoded amounts) |
| +1 | Multiple pricing tiers (free, pro, enterprise) with clear differentiation |
| +1 | Both monthly and annual billing intervals available |
| +1 | Price IDs stored in config/env, not hardcoded in source |
| -1 | Ad-hoc amounts in checkout instead of Price objects |
| -1 | Single plan with no upgrade path |

### Plan Switching (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Upgrade path implemented (lower tier -> higher tier) |
| +1 | Downgrade supported with proper proration |
| +1 | Proration behavior explicitly configured |
| -1 | No plan switching — users must cancel and re-subscribe |

### Pricing Display (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Pricing page fetches prices from Stripe API (not hardcoded) |
| +1 | Current plan highlighted for authenticated users |
| +1 | Feature comparison table per plan |
| -1 | Prices hardcoded in frontend — out of sync with Stripe |

## Scoring Summary

| Sub-area | Max Points |
|----------|-----------|
| Session Creation | 3 |
| Payment Methods | 2 |
| Billing Flow UX | 2 |
| Invoice Handling | 2 |
| Customer Linking | 1 |
| **Checkout & Billing Total** | **10** |
| Portal Configuration | 3 |
| Self-Service Features | 4 |
| Portal Integration | 3 |
| **Customer Portal Total** | **10** |
| Price Configuration | 4 |
| Plan Switching | 3 |
| Pricing Display | 3 |
| **Pricing & Plans Total** | **10** |
