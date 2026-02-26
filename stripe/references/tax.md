# Stripe Tax

Automatic tax calculation for products and subscriptions.

## Enable in Checkout

```typescript
const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  line_items: [{ price: priceId, quantity: 1 }],
  automatic_tax: { enabled: true },
  customer_update: { address: "auto" }, // Auto-update customer address
  success_url: `${baseUrl}/success`,
  cancel_url: `${baseUrl}/pricing`,
});
```

## Enable on Subscription

```typescript
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: priceId }],
  automatic_tax: { enabled: true },
});
```

## Enable on Invoice

```typescript
const invoice = await stripe.invoices.create({
  customer: customerId,
  automatic_tax: { enabled: true },
});
```

## Enable on Payment Intent (one-time)

Tax on PaymentIntents requires using the Tax Calculation API:

```typescript
const calculation = await stripe.tax.calculations.create({
  currency: "usd",
  line_items: [
    {
      amount: 1000,
      reference: "product_123",
      tax_behavior: "exclusive", // Tax added on top
    },
  ],
  customer_details: {
    address: { country: "US", state: "CA", postal_code: "94111" },
    address_source: "billing",
  },
});

// calculation.tax_amount_exclusive = tax to charge
// calculation.amount_total = total including tax
```

## Product Tax Behavior

```typescript
// Set on Price creation
const price = await stripe.prices.create({
  product: productId,
  unit_amount: 2900,
  currency: "usd",
  tax_behavior: "exclusive", // or "inclusive" or "unspecified"
  recurring: { interval: "month" },
});
```

| Behavior | Display | Tax |
|----------|---------|-----|
| `exclusive` | $29.00 + tax | Added on top |
| `inclusive` | $29.00 (tax included) | Extracted from price |
| `unspecified` | Depends on config | Default behavior |

## Tax Registrations

Register where tax needs to be collected (Dashboard → Tax → Registrations):

| Registration Type | Example |
|-------------------|---------|
| State sales tax | California, New York |
| VAT | EU countries |
| GST | Australia, Canada |

## Key Points
- Enable `automatic_tax` on Checkout/Subscriptions — Stripe handles calculation
- Set `tax_behavior` on Prices (`exclusive` recommended for B2B)
- Register in all required jurisdictions via Dashboard
- Tax calculation requires customer address — Checkout collects automatically
- Use Tax API for custom payment flows without Checkout
