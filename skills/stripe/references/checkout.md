# Checkout Sessions

## Server Action — Create Session

```typescript
// app/actions/checkout.ts
"use server";

import { redirect } from "next/navigation";
import { stripe } from "@/lib/stripe";

export async function createCheckoutSession(priceId: string) {
  const session = await stripe.checkout.sessions.create({
    mode: "payment", // or "subscription"
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    metadata: { priceId },
  });

  redirect(session.url!);
}
```

## Mode Options

| Mode | Use Case |
|------|----------|
| `payment` | One-time charge |
| `subscription` | Recurring billing |
| `setup` | Save card for later (no charge) |

## With Customer (logged-in user)

```typescript
const session = await stripe.checkout.sessions.create({
  customer: stripeCustomerId, // Existing Stripe customer
  // OR create new:
  customer_email: user.email,
  customer_creation: "always",
  mode: "subscription",
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${baseUrl}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${baseUrl}/pricing`,
  allow_promotion_codes: true,
  billing_address_collection: "required",
  metadata: { userId: user.id },
});
```

## Success Page — Retrieve Session

```typescript
// app/success/page.tsx
import { stripe } from "@/lib/stripe";

export default async function SuccessPage({
  searchParams,
}: {
  searchParams: Promise<{ session_id?: string }>;
}) {
  const { session_id } = await searchParams;
  if (!session_id) return <p>Invalid session</p>;

  const session = await stripe.checkout.sessions.retrieve(session_id, {
    expand: ["line_items", "customer"],
  });

  return (
    <div>
      <h1>Payment successful</h1>
      <p>Amount: {(session.amount_total! / 100).toFixed(2)}</p>
    </div>
  );
}
```

## Embedded Checkout (in-page)

```typescript
// Server: return client_secret instead of redirect
const session = await stripe.checkout.sessions.create({
  ui_mode: "embedded",
  line_items: [{ price: priceId, quantity: 1 }],
  mode: "payment",
  return_url: `${baseUrl}/return?session_id={CHECKOUT_SESSION_ID}`,
});
return { clientSecret: session.client_secret };
```

```tsx
// Client Component
import { EmbeddedCheckoutProvider, EmbeddedCheckout } from "@stripe/react-stripe-js";
import { getStripe } from "@/lib/stripe-client";

export function CheckoutForm({ clientSecret }: { clientSecret: string }) {
  return (
    <EmbeddedCheckoutProvider stripe={getStripe()} options={{ clientSecret }}>
      <EmbeddedCheckout />
    </EmbeddedCheckoutProvider>
  );
}
```

## Custom Fields

```typescript
const session = await stripe.checkout.sessions.create({
  // ...
  custom_fields: [
    { key: "company", label: { type: "custom", custom: "Company" }, type: "text" },
  ],
  phone_number_collection: { enabled: true },
  shipping_address_collection: { allowed_countries: ["US", "CA", "GB"] },
});
```

## Key Points
- Always set `metadata` for tracking (userId, orderId, etc.)
- Use `allow_promotion_codes: true` for coupon support
- Session expires after 24 hours (configurable: 30 min — 24 hours)
- Fulfill orders via `checkout.session.completed` webhook, NOT success URL
- Add `app/success/error.tsx` error boundary — see `references/error-handling.md`
