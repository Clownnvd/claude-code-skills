# Customer Portal

Self-service billing management. Customers update payment methods, change plans, cancel subscriptions, view invoices.

## Create Portal Session

```typescript
// app/actions/portal.ts
"use server";

import { redirect } from "next/navigation";
import { stripe } from "@/lib/stripe";

export async function createPortalSession(customerId: string) {
  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard`,
  });

  redirect(session.url);
}
```

## Portal Configuration (API)

```typescript
// Run once to configure portal (or configure in Dashboard)
const config = await stripe.billingPortal.configurations.create({
  business_profile: {
    headline: "Manage your subscription",
  },
  features: {
    customer_update: {
      allowed_updates: ["email", "address", "phone"],
      enabled: true,
    },
    invoice_history: { enabled: true },
    payment_method_update: { enabled: true },
    subscription_cancel: {
      enabled: true,
      mode: "at_period_end",
      cancellation_reason: {
        enabled: true,
        options: ["too_expensive", "missing_features", "switched_service", "other"],
      },
    },
    subscription_update: {
      enabled: true,
      default_allowed_updates: ["price"],
      products: [
        {
          product: "prod_xxx",
          prices: ["price_basic", "price_pro", "price_enterprise"],
        },
      ],
      proration_behavior: "create_prorations",
    },
  },
});
```

## Deep Linking

```typescript
// Link directly to specific portal section
const session = await stripe.billingPortal.sessions.create({
  customer: customerId,
  return_url: returnUrl,
  flow_data: {
    type: "subscription_cancel",
    subscription_cancel: {
      subscription: subscriptionId,
    },
  },
});
```

| `flow_data.type` | Opens |
|-------------------|-------|
| `payment_method_update` | Update payment method |
| `subscription_cancel` | Cancel flow with reasons |
| `subscription_update` | Plan change selector |
| `subscription_update_confirm` | Confirm specific plan change |

## Usage in Component

```tsx
// app/dashboard/billing/page.tsx
import { createPortalSession } from "@/app/actions/portal";

export default async function BillingPage() {
  const user = await getCurrentUser();

  return (
    <form action={createPortalSession.bind(null, user.stripeCustomerId!)}>
      <button type="submit">Manage Billing</button>
    </form>
  );
}
```

## Key Points
- Configure portal in Stripe Dashboard or via API (one-time setup)
- Portal handles PCI compliance automatically (Stripe-hosted)
- Listen to webhooks for subscription changes made through portal
- Use `cancel_at_period_end` mode for better retention
