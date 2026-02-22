# Stripe Setup

## Server-Side Instance

```typescript
// lib/stripe.ts
import Stripe from "stripe";

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error("STRIPE_SECRET_KEY is not set");
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: "2026-01-28.clover",
});
```

Singleton — import from any Server Component, Server Action, or Route Handler.

## Client-Side (Lazy Load)

```typescript
// lib/stripe-client.ts
import { loadStripe, type Stripe } from "@stripe/stripe-js";

let stripePromise: Promise<Stripe | null>;

export function getStripe() {
  if (!stripePromise) {
    stripePromise = loadStripe(
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
    );
  }
  return stripePromise;
}
```

Only loads Stripe.js when `getStripe()` is first called. Use in Client Components.

## Environment Variables

```bash
# .env.local
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

| Variable | Where Used | Prefix |
|----------|-----------|--------|
| `STRIPE_SECRET_KEY` | Server only | None |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Client + Server | `NEXT_PUBLIC_` |
| `STRIPE_WEBHOOK_SECRET` | Webhook handler | None |

## TypeScript Types

```typescript
// Import Stripe types directly
import type Stripe from "stripe";

// Common types
type CheckoutSession = Stripe.Checkout.Session;
type Subscription = Stripe.Subscription;
type Invoice = Stripe.Invoice;
type PaymentIntent = Stripe.PaymentIntent;
type Customer = Stripe.Customer;
type Price = Stripe.Price;
type Product = Stripe.Product;
```

## API Version Pinning

Pin to a specific version to avoid breaking changes on upgrade:

```typescript
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: "2026-01-28.clover", // Pin this
});
```

Update version when ready to adopt new API features. Test thoroughly before changing.
