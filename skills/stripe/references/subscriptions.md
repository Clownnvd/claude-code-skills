# Subscriptions

## Create via Checkout (Recommended)

```typescript
"use server";

import { stripe } from "@/lib/stripe";
import { redirect } from "next/navigation";

export async function createSubscription(priceId: string, userId: string) {
  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    customer_email: "user@example.com", // Or customer: stripeCustomerId
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    subscription_data: {
      metadata: { userId },
      trial_period_days: 14,
    },
    metadata: { userId },
  });

  redirect(session.url!);
}
```

## Create via API (Custom UI)

```typescript
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: priceId }],
  payment_behavior: "default_incomplete",
  payment_settings: { save_default_payment_method: "on_subscription" },
  expand: ["latest_invoice.payment_intent"],
  metadata: { userId },
});

// Return client_secret for frontend confirmation
const invoice = subscription.latest_invoice as Stripe.Invoice;
const pi = invoice.payment_intent as Stripe.PaymentIntent;
return { clientSecret: pi.client_secret, subscriptionId: subscription.id };
```

## Trial Periods

```typescript
// Via Checkout
subscription_data: { trial_period_days: 14 }

// Via API
await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: priceId }],
  trial_period_days: 14,
  trial_settings: {
    end_behavior: { missing_payment_method: "cancel" },
  },
});
```

## Plan Switching (Proration)

```typescript
export async function updateSubscription(subscriptionId: string, newPriceId: string) {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);

  await stripe.subscriptions.update(subscriptionId, {
    items: [
      { id: subscription.items.data[0].id, price: newPriceId },
    ],
    proration_behavior: "create_prorations", // or "none" / "always_invoice"
  });
}
```

## Cancel

```typescript
// Cancel at period end (grace period)
await stripe.subscriptions.update(subscriptionId, {
  cancel_at_period_end: true,
});

// Cancel immediately
await stripe.subscriptions.cancel(subscriptionId);

// Reactivate before period ends
await stripe.subscriptions.update(subscriptionId, {
  cancel_at_period_end: false,
});
```

## Status Reference

| Status | Meaning | Action |
|--------|---------|--------|
| `active` | Paid and current | Full access |
| `trialing` | In trial period | Full access |
| `past_due` | Payment failed, retrying | Warn user |
| `unpaid` | All retries failed | Restrict access |
| `canceled` | Cancelled | Revoke access |
| `incomplete` | Initial payment pending | Wait for payment |
| `incomplete_expired` | Initial payment failed | Prompt retry |
| `paused` | Manually paused | Restrict access |

## Webhook Events for Subscriptions

```typescript
// Essential events to handle
switch (event.type) {
  case "customer.subscription.created":    // New subscription
  case "customer.subscription.updated":    // Plan change, cancel_at_period_end
  case "customer.subscription.deleted":    // Fully cancelled
  case "customer.subscription.trial_will_end": // 3 days before trial ends
  case "invoice.paid":                     // Successful renewal
  case "invoice.payment_failed":           // Failed renewal
  case "invoice.payment_action_required":  // Needs 3D Secure
}
```

## Key Points
- Prefer Checkout for subscription creation (handles all edge cases)
- Always sync subscription status via webhooks, not polling
- Use `cancel_at_period_end` instead of immediate cancel for better UX
- Set `metadata.userId` for linking to your database
