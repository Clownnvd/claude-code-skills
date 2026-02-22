# Stripe Setup

## Step-by-Step

### 1. Install packages

```bash
npm install stripe @stripe/stripe-js @stripe/react-stripe-js
```

| Package | Purpose |
|---------|---------|
| `stripe` | Server-side SDK (API calls) |
| `@stripe/stripe-js` | Client-side Stripe.js loader |
| `@stripe/react-stripe-js` | React components (`<Elements>`, `<PaymentElement>`, `<EmbeddedCheckout>`) |

### 2. Get API keys

1. Go to [Stripe Dashboard → API Keys](https://dashboard.stripe.com/apikeys)
2. Copy **Publishable key** (`pk_test_...`) and **Secret key** (`sk_test_...`)
3. For webhooks: Dashboard → Webhooks → endpoint secret (`whsec_...`), or run `stripe listen --print-secret`

### 3. Create `.env.local`

```bash
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 4. Create `lib/stripe.ts` (server)

Copy `templates/stripe-server.ts` → `lib/stripe.ts`:

```typescript
import Stripe from "stripe";

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error("Missing STRIPE_SECRET_KEY environment variable");
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: "2026-01-28.clover",
});
```

Singleton — import from Server Components, Server Actions, Route Handlers.

### 5. Create `lib/stripe-client.ts` (client)

Copy `templates/stripe-client.ts` → `lib/stripe-client.ts`:

```typescript
"use client";

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

### 6. Verify setup

```bash
# Start dev server
npm run dev

# In another terminal — test webhook forwarding
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger a test event
stripe trigger checkout.session.completed
```

## TypeScript Types

```typescript
import type Stripe from "stripe";

type CheckoutSession = Stripe.Checkout.Session;
type Subscription = Stripe.Subscription;
type Invoice = Stripe.Invoice;
type PaymentIntent = Stripe.PaymentIntent;
type Customer = Stripe.Customer;
type Price = Stripe.Price;
type Product = Stripe.Product;
```

## API Version Pinning

Pin to a specific version to avoid breaking changes:

```typescript
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: "2026-01-28.clover", // Pin this
});
```

Update version when ready to adopt new API features. Test thoroughly before changing.

## Environment Variables

| Variable | Where Used | Prefix |
|----------|-----------|--------|
| `STRIPE_SECRET_KEY` | Server only | None |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Client + Server | `NEXT_PUBLIC_` |
| `STRIPE_WEBHOOK_SECRET` | Webhook handler | None |
| `NEXT_PUBLIC_APP_URL` | Checkout URLs | `NEXT_PUBLIC_` |
