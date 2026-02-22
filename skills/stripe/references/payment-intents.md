# Payment Intents

Use when building a custom payment UI with Stripe Elements instead of hosted Checkout.

## Create PaymentIntent (Server Action)

```typescript
// app/actions/payment.ts
"use server";

import { stripe } from "@/lib/stripe";
import { v4 as uuid } from "uuid";

export async function createPaymentIntent(amount: number, currency = "usd") {
  // Validate amount server-side — never trust client
  if (amount < 50) throw new Error("Minimum amount is $0.50");

  const paymentIntent = await stripe.paymentIntents.create(
    {
      amount, // In cents: $10.00 = 1000
      currency,
      automatic_payment_methods: { enabled: true },
      metadata: { orderId: uuid() },
    },
    { idempotencyKey: uuid() }
  );

  return { clientSecret: paymentIntent.client_secret };
}
```

## Confirm on Client

```tsx
"use client";

import { PaymentElement, useStripe, useElements } from "@stripe/react-stripe-js";
import { useState } from "react";

export function PaymentForm() {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState<string>();
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!stripe || !elements) return;

    setLoading(true);
    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/payment/success`,
      },
    });

    if (error) {
      setError(error.message);
      setLoading(false);
    }
    // If no error, user redirected to return_url
  }

  return (
    <form onSubmit={handleSubmit}>
      <PaymentElement />
      <button disabled={!stripe || loading}>
        {loading ? "Processing..." : "Pay"}
      </button>
      {error && <p>{error}</p>}
    </form>
  );
}
```

## Wrap with Elements Provider

```tsx
"use client";

import { Elements } from "@stripe/react-stripe-js";
import { getStripe } from "@/lib/stripe-client";

export function PaymentWrapper({ clientSecret }: { clientSecret: string }) {
  return (
    <Elements stripe={getStripe()} options={{ clientSecret }}>
      <PaymentForm />
    </Elements>
  );
}
```

## Status Lifecycle

```
requires_payment_method → requires_confirmation → requires_action → processing → succeeded
                                                       ↓
                                                   (3D Secure)
                                                       ↓
                                                   succeeded / requires_payment_method (failed)
```

## Capture vs Authorize

```typescript
// Authorize only (hold funds, capture later)
const pi = await stripe.paymentIntents.create({
  amount: 5000,
  currency: "usd",
  capture_method: "manual", // Default: "automatic"
});

// Capture later (within 7 days)
await stripe.paymentIntents.capture(pi.id, {
  amount_to_capture: 4500, // Can capture less than authorized
});
```

## Key Points
- Amount is in smallest currency unit (cents for USD)
- `automatic_payment_methods` enables all configured methods
- Always use `idempotencyKey` for creates to prevent double charges
- 3D Secure handled automatically via `requires_action` status
- Check `payment_intent.succeeded` webhook for confirmation
