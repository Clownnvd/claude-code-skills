# Products & Prices

## Create Product + Price (API)

```typescript
// One-time setup or migration script
const product = await stripe.products.create({
  name: "Pro Plan",
  description: "Full access to all features",
  metadata: { tier: "pro" },
});

// Recurring price
const monthlyPrice = await stripe.prices.create({
  product: product.id,
  unit_amount: 2900, // $29.00
  currency: "usd",
  recurring: { interval: "month" },
  metadata: { plan: "pro_monthly" },
});

// One-time price
const lifetimePrice = await stripe.prices.create({
  product: product.id,
  unit_amount: 29900, // $299.00
  currency: "usd",
  metadata: { plan: "pro_lifetime" },
});
```

## Price Types

| Type | `recurring` | Use Case |
|------|------------|----------|
| One-time | `null` | Single purchase |
| Monthly | `{ interval: "month" }` | Monthly subscription |
| Yearly | `{ interval: "year" }` | Annual subscription |
| Metered | `{ interval: "month", usage_type: "metered" }` | Pay per use |

## Tiered Pricing

```typescript
const tieredPrice = await stripe.prices.create({
  product: product.id,
  currency: "usd",
  recurring: { interval: "month" },
  billing_scheme: "tiered",
  tiers_mode: "graduated", // or "volume"
  tiers: [
    { up_to: 100, unit_amount: 10 },    // First 100: $0.10 each
    { up_to: 1000, unit_amount: 8 },    // 101-1000: $0.08 each
    { up_to: "inf", unit_amount: 5 },   // 1001+: $0.05 each
  ],
});
```

## Coupons & Promo Codes

```typescript
// Create coupon
const coupon = await stripe.coupons.create({
  percent_off: 20,
  duration: "repeating",
  duration_in_months: 3,
  name: "20% off for 3 months",
});

// Create promotion code (user-facing code)
const promoCode = await stripe.promotionCodes.create({
  coupon: coupon.id,
  code: "LAUNCH20",
  max_redemptions: 100,
  expires_at: Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60, // 30 days
});
```

Enable in Checkout:

```typescript
const session = await stripe.checkout.sessions.create({
  // ...
  allow_promotion_codes: true,
  // OR apply specific coupon:
  discounts: [{ coupon: coupon.id }],
});
```

## List Active Prices

```typescript
const prices = await stripe.prices.list({
  active: true,
  expand: ["data.product"],
  type: "recurring",
});
```

## Archive Price (Soft Delete)

```typescript
// Deactivate price (existing subscriptions unaffected)
await stripe.prices.update(priceId, { active: false });
```

## Key Points
- Create Products/Prices via Dashboard for simple setups, API for programmatic
- Prices are immutable — deactivate old, create new for changes
- Use `metadata` to map Stripe entities to your database
- `allow_promotion_codes: true` in Checkout enables coupon field
