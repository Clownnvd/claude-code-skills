# Stripe Connect (Marketplace / Platform)

## Account Types

| Type | Control | Onboarding | Use Case |
|------|---------|-----------|----------|
| **Standard** | Seller manages | Stripe-hosted | Marketplace with independent sellers |
| **Express** | Platform manages | Stripe-hosted (simplified) | Gig platforms, driver apps |
| **Custom** | Full control | Build your own | White-label, full customization |

## Create Connected Account

```typescript
const account = await stripe.accounts.create({
  type: "express", // or "standard", "custom"
  country: "US",
  email: "seller@example.com",
  capabilities: {
    card_payments: { requested: true },
    transfers: { requested: true },
  },
  metadata: { userId: sellerId },
});
```

## Onboarding Link

```typescript
const accountLink = await stripe.accountLinks.create({
  account: account.id,
  refresh_url: `${baseUrl}/connect/refresh`,
  return_url: `${baseUrl}/connect/complete`,
  type: "account_onboarding",
});

// Redirect seller to accountLink.url
```

## Payment with Platform Fee

```typescript
// Destination charge — platform collects, transfers to seller
const session = await stripe.checkout.sessions.create({
  mode: "payment",
  line_items: [{ price: priceId, quantity: 1 }],
  payment_intent_data: {
    application_fee_amount: 500, // $5.00 platform fee
    transfer_data: { destination: connectedAccountId },
  },
  success_url: `${baseUrl}/success`,
  cancel_url: `${baseUrl}/cancel`,
});
```

## Direct Charge (on behalf of seller)

```typescript
const paymentIntent = await stripe.paymentIntents.create(
  {
    amount: 10000,
    currency: "usd",
    application_fee_amount: 1000,
  },
  { stripeAccount: connectedAccountId } // Charge on seller's account
);
```

## Transfer (Separate Charges and Transfers)

```typescript
// Charge customer on platform
const charge = await stripe.paymentIntents.create({
  amount: 10000,
  currency: "usd",
});

// Transfer to seller later
const transfer = await stripe.transfers.create({
  amount: 8500, // After platform fee
  currency: "usd",
  destination: connectedAccountId,
  transfer_group: `order_${orderId}`,
});
```

## Check Account Status

```typescript
const account = await stripe.accounts.retrieve(connectedAccountId);

const isReady =
  account.charges_enabled &&
  account.payouts_enabled &&
  account.details_submitted;
```

## Webhook Events

| Event | When |
|-------|------|
| `account.updated` | Account status changed |
| `account.application.deauthorized` | Seller disconnected |
| `payout.paid` | Payout sent to seller |
| `payout.failed` | Payout failed |

## Key Points
- Use **Express** for most marketplaces (fastest integration)
- `application_fee_amount` is in cents
- Always verify `charges_enabled` before processing payments
- Listen to `account.updated` to track onboarding completion
- Refunds on platform reduce the connected account balance
