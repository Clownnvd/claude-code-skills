# Fix Patterns: Payment Security + Testing + Monitoring

## Hardcoded Stripe Keys (CRITICAL)

### Before
```typescript
const stripe = new Stripe("sk_live_abc123def456", { apiVersion: "2024-12-18.acacia" })
```

### After
```typescript
// src/lib/stripe.ts
import Stripe from "stripe"
if (!process.env.STRIPE_SECRET_KEY) throw new Error("STRIPE_SECRET_KEY is required")
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: "2024-12-18.acacia", typescript: true,
})
```
**Also**: Rotate compromised keys in Stripe Dashboard -> Developers -> API Keys. Update all environments.

## No Env Var Validation

### Before
```typescript
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { ... }) // crashes if missing
```

### After: Zod validation at startup
```typescript
// src/lib/env.ts
import { z } from "zod"
const serverEnvSchema = z.object({
  STRIPE_SECRET_KEY: z.string().min(1).refine(
    (k) => k.startsWith("sk_test_") || k.startsWith("sk_live_"),
    "Must start with sk_test_ or sk_live_"
  ),
  STRIPE_WEBHOOK_SECRET: z.string().min(1).refine(
    (k) => k.startsWith("whsec_"), "Must start with whsec_"
  ),
  NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: z.string().min(1),
})
export const env = serverEnvSchema.parse(process.env)
```
Update `.env.example` with `STRIPE_SECRET_KEY=sk_test_xxx`, `STRIPE_WEBHOOK_SECRET=whsec_xxx`.

## No Amount Validation

### Before
```typescript
const { amount, currency } = await request.json()
await stripe.paymentIntents.create({ amount, currency }) // client controls amount
```

### After: Use Price IDs
```typescript
const { priceId } = await request.json()
const price = await stripe.prices.retrieve(priceId)
if (!price.active) return NextResponse.json({ error: "Invalid price" }, { status: 400 })
const session = await stripe.checkout.sessions.create({
  mode: price.type === "recurring" ? "subscription" : "payment",
  line_items: [{ price: priceId, quantity: 1 }],
})
```

## Missing Test Mode Separation

### Before
```typescript
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { ... }) // no env check
```

### After: Prevent live keys in dev
```typescript
const isProduction = process.env.NODE_ENV === "production"
const stripeKey = process.env.STRIPE_SECRET_KEY!
if (!isProduction && stripeKey.startsWith("sk_live_")) {
  throw new Error("DANGER: Live Stripe key in non-production. Use sk_test_ keys.")
}
export const stripe = new Stripe(stripeKey, { apiVersion: "2024-12-18.acacia" })
```

## Missing Payment Monitoring

### Before: No visibility into payment failures

### After: Structured logging
```typescript
type PaymentEvent = {
  type: "checkout_created" | "payment_succeeded" | "payment_failed" | "subscription_changed"
  userId: string; amount?: number; currency?: string; error?: string
}
export function logPaymentEvent(event: PaymentEvent) {
  console.log(JSON.stringify({ timestamp: new Date().toISOString(), service: "payment", ...event }))
}
```

## No Stripe CLI Testing

### After: Add to dev workflow
```bash
stripe listen --forward-to localhost:3000/api/stripe/webhook
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
```
Add scripts to `package.json`:
```json
{ "scripts": {
  "stripe:listen": "stripe listen --forward-to localhost:3000/api/stripe/webhook",
  "stripe:trigger:checkout": "stripe trigger checkout.session.completed"
}}
```
