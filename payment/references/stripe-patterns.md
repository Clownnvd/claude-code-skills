# Stripe SDK Patterns

## Client Initialization

### Server-Side (Node.js)
```typescript
// src/lib/stripe.ts
import Stripe from "stripe"
if (!process.env.STRIPE_SECRET_KEY) throw new Error("STRIPE_SECRET_KEY is required")
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: "2024-12-18.acacia", typescript: true,
})
```

### Client-Side (@stripe/stripe-js)
```typescript
// src/lib/stripe-client.ts
import { loadStripe } from "@stripe/stripe-js"
export const getStripe = () => loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!)
```

## Products & Prices
```typescript
const product = await stripe.products.create({ name: "Pro Plan", metadata: { tier: "pro" } })
const price = await stripe.prices.create({
  product: product.id, unit_amount: 2900, currency: "usd",
  recurring: { interval: "month" },
})
```

### Retrieve Prices for Pricing Page
```typescript
export async function getPrices() {
  const prices = await stripe.prices.list({ active: true, expand: ["data.product"], type: "recurring" })
  return prices.data
}
```

## Checkout Sessions

### Subscription Checkout
```typescript
export async function POST(request: Request) {
  const { priceId, userId } = await request.json()
  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    payment_method_types: ["card"],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing?canceled=true`,
    metadata: { userId },
    subscription_data: { metadata: { userId }, trial_period_days: 14 },
  })
  return NextResponse.json({ url: session.url })
}
```

### One-Time Payment Checkout
```typescript
const session = await stripe.checkout.sessions.create({
  mode: "payment",
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${process.env.NEXT_PUBLIC_APP_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/cancel`,
  metadata: { userId, productType: "KING_TEMPLATE" },
})
```

## Customer Portal
```typescript
export async function POST(request: Request) {
  const { customerId } = await request.json()
  const portalSession = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing`,
  })
  return NextResponse.json({ url: portalSession.url })
}
```

### Portal Configuration
```typescript
await stripe.billingPortal.configurations.create({
  features: {
    subscription_cancel: { enabled: true, mode: "at_period_end" },
    subscription_update: { enabled: true, default_allowed_updates: ["price", "quantity"],
      proration_behavior: "create_prorations" },
    payment_method_update: { enabled: true },
    invoice_history: { enabled: true },
  },
})
```

## Test Clocks
```typescript
const testClock = await stripe.testHelpers.testClocks.create({
  frozen_time: Math.floor(Date.now() / 1000), name: "Subscription lifecycle test",
})
const customer = await stripe.customers.create({ test_clock: testClock.id, email: "test@example.com" })
// Advance time to trigger renewal
await stripe.testHelpers.testClocks.advance(testClock.id, {
  frozen_time: Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60,
})
```
