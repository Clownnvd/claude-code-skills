# Webhook Patterns

## Signature Verification (Critical)

### Next.js App Router Route Handler
```typescript
// src/app/api/stripe/webhook/route.ts
import { headers } from "next/headers"
import { stripe } from "@/lib/stripe"
import Stripe from "stripe"

export async function POST(request: Request) {
  const body = await request.text() // MUST use text(), not json()
  const signature = (await headers()).get("stripe-signature")
  if (!signature) return new Response("Missing stripe-signature header", { status: 400 })

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch (err) {
    console.error("Webhook signature verification failed:", err)
    return new Response("Webhook signature verification failed", { status: 400 })
  }
  // Process event...
  return new Response("OK", { status: 200 })
}
```
Note: Next.js App Router does NOT need body parser config. `request.text()` gives raw body automatically.

## Event Routing
```typescript
async function handleWebhookEvent(event: Stripe.Event) {
  switch (event.type) {
    case "checkout.session.completed":
      await handleCheckoutComplete(event.data.object as Stripe.Checkout.Session); break
    case "customer.subscription.created":
    case "customer.subscription.updated":
      await handleSubscriptionUpdated(event.data.object as Stripe.Subscription); break
    case "customer.subscription.deleted":
      await handleSubscriptionDeleted(event.data.object as Stripe.Subscription); break
    case "invoice.payment_succeeded":
      await handleInvoiceSuccess(event.data.object as Stripe.Invoice); break
    case "invoice.payment_failed":
      await handleInvoiceFailed(event.data.object as Stripe.Invoice); break
    default: console.log(`Unhandled event type: ${event.type}`)
  }
}
```

## Idempotency (Dedup by Event ID)
```typescript
async function processWebhookEvent(event: Stripe.Event) {
  const existing = await prisma.webhookEvent.findUnique({ where: { stripeEventId: event.id } })
  if (existing) { console.log(`Event ${event.id} already processed`); return }
  await handleWebhookEvent(event)
  await prisma.webhookEvent.create({
    data: { stripeEventId: event.id, type: event.type, processedAt: new Date() },
  })
}
```
Prisma model:
```prisma
model WebhookEvent {
  id            String   @id @default(cuid())
  stripeEventId String   @unique
  type          String
  processedAt   DateTime @default(now())
  createdAt     DateTime @default(now())
  @@index([type])
  @@index([createdAt])
}
```

## Retry Handling
Stripe retries for up to 3 days with exponential backoff. Return 200 quickly; process heavy work async. Return 500 to trigger retry.

## Key Subscription Event Types

| Event | When | Action |
|-------|------|--------|
| `checkout.session.completed` | Checkout done | Create subscription, grant access |
| `customer.subscription.updated` | Plan/status change | Update subscription record |
| `customer.subscription.deleted` | Canceled/expired | Revoke access |
| `invoice.payment_succeeded` | Payment success | Update billing history |
| `invoice.payment_failed` | Payment failed | Notify user, update status |
| `customer.subscription.trial_will_end` | Trial ending 3d | Send reminder |

## Testing with Stripe CLI
```bash
stripe listen --forward-to localhost:3000/api/stripe/webhook
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
```
