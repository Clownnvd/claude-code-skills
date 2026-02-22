# Billing Meter — Usage-Based Billing

Charge customers based on actual usage (API calls, storage, compute, messages, etc.).

## Create Metered Price

```typescript
const product = await stripe.products.create({
  name: "API Calls",
});

const price = await stripe.prices.create({
  product: product.id,
  currency: "usd",
  recurring: {
    interval: "month",
    usage_type: "metered",
  },
  billing_scheme: "per_unit",
  unit_amount: 1, // $0.01 per unit
  // OR tiered:
  // billing_scheme: "tiered",
  // tiers_mode: "graduated",
  // tiers: [
  //   { up_to: 1000, unit_amount: 0 },     // First 1000 free
  //   { up_to: 10000, unit_amount: 1 },     // $0.01 each
  //   { up_to: "inf", unit_amount: 0.5 },   // $0.005 each
  // ],
});
```

## Create Subscription with Metered Price

```typescript
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: meteredPriceId }],
  // No initial charge — billed at period end based on usage
});
```

## Report Usage

```typescript
// Report usage for a subscription item
const subscriptionItem = subscription.items.data[0];

await stripe.subscriptionItems.createUsageRecord(subscriptionItem.id, {
  quantity: 150,            // Number of units consumed
  timestamp: Math.floor(Date.now() / 1000),
  action: "increment",     // Add to existing usage (default)
  // action: "set",        // Replace current period usage
});
```

## Report Usage in Bulk (Server Action)

```typescript
"use server";

import { stripe } from "@/lib/stripe";

export async function reportUsage(
  subscriptionItemId: string,
  quantity: number
) {
  return stripe.subscriptionItems.createUsageRecord(subscriptionItemId, {
    quantity,
    action: "increment",
    timestamp: Math.floor(Date.now() / 1000),
  });
}
```

## Usage Summary

```typescript
// Get usage for current period
const usageRecords = await stripe.subscriptionItems.listUsageRecordSummaries(
  subscriptionItemId,
  { limit: 1 }
);

const currentUsage = usageRecords.data[0]?.total_usage ?? 0;
```

## Invoice Preview (Show Estimated Cost)

```typescript
// createPreview replaces deprecated retrieveUpcoming (removed in API 2025-03-31+)
const preview = await stripe.invoices.createPreview({
  customer: customerId,
  subscription: subscriptionId,
});

const estimatedTotal = preview.amount_due; // In cents
const lineItems = preview.lines.data;      // Breakdown per item
```

## Mixed Billing (Fixed + Metered)

```typescript
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [
    { price: fixedPriceId },   // $29/mo base fee
    { price: meteredPriceId }, // + usage charges
  ],
});
```

## Aggregation

| `action` | Behavior |
|----------|----------|
| `increment` | Add to running total (default) |
| `set` | Replace current period total |

## Key Points
- Metered subscriptions bill at period END based on reported usage
- Report usage frequently (at least daily) — lost reports = lost revenue
- Use `increment` for event-based reporting (API calls)
- Use `set` for snapshot-based reporting (storage used)
- Combine fixed + metered prices for base fee + overage model
- Use invoice preview to show customers estimated charges
