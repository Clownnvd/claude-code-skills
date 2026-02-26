# Fix Patterns: Webhook Integration + Error Handling & Recovery

## Missing Signature Verification (CRITICAL)

### Before
```typescript
export async function POST(request: Request) {
  const event = await request.json() // NO VERIFICATION
  await handleEvent(event)
  return new Response("OK", { status: 200 })
}
```

### After
```typescript
import { headers } from "next/headers"
import { stripe } from "@/lib/stripe"
import Stripe from "stripe"

export async function POST(request: Request) {
  const body = await request.text() // MUST use text(), not json()
  const signature = (await headers()).get("stripe-signature")
  if (!signature) return new Response("Missing stripe-signature", { status: 400 })

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch (err) {
    console.error("Webhook verification failed:", err)
    return new Response("Webhook signature verification failed", { status: 400 })
  }

  try {
    await processWebhookEvent(event)
  } catch (error) {
    console.error(`Error processing event ${event.id}:`, error)
    return new Response("Processing error", { status: 500 })
  }
  return new Response("OK", { status: 200 })
}
```

## No Idempotency

### Before
```typescript
async function handleEvent(event: Stripe.Event) {
  switch (event.type) {
    case "checkout.session.completed":
      await grantAccess(event.data.object) // runs on every retry
  }
}
```

### After
```typescript
async function processWebhookEvent(event: Stripe.Event) {
  const existing = await prisma.webhookEvent.findUnique({
    where: { stripeEventId: event.id },
  })
  if (existing) { console.log(`Event ${event.id} already processed`); return }

  await handleWebhookEvent(event)

  await prisma.webhookEvent.create({
    data: { stripeEventId: event.id, type: event.type, processedAt: new Date() },
  })
}
```
Requires Prisma model:
```prisma
model WebhookEvent {
  id            String   @id @default(cuid())
  stripeEventId String   @unique
  type          String
  processedAt   DateTime @default(now())
  createdAt     DateTime @default(now())
  @@index([type])
}
```

## Missing Event Handlers

### Before: Only checkout handled, subscription events ignored

### After: Handle all critical events
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
    default:
      console.log(`Unhandled event type: ${event.type}`)
  }
}
```

## No Error Recovery on Payment Failure

### After: Handle failures with notification
```typescript
async function handleInvoiceFailed(invoice: Stripe.Invoice) {
  const customerId = invoice.customer as string
  const user = await prisma.user.findFirst({
    where: { stripeCustomerId: customerId }, select: { id: true, email: true },
  })
  if (!user) { console.error(`No user for customer ${customerId}`); return }

  if (invoice.subscription) {
    await prisma.subscription.updateMany({
      where: { stripeSubscriptionId: invoice.subscription as string },
      data: { status: "past_due" },
    })
  }
  await sendPaymentFailureNotification(user.email, {
    amount: invoice.amount_due / 100, currency: invoice.currency,
  })
}
```

## Silent Error Swallowing

### Before
```typescript
try { await handleEvent(event) } catch (e) { /* silently ignored */ }
return new Response("OK", { status: 200 }) // Stripe thinks success
```

### After
```typescript
try {
  await processWebhookEvent(event)
} catch (error) {
  console.error(`Error processing ${event.id}:`, { eventType: event.type, error })
  return new Response("Processing error", { status: 500 }) // Stripe retries
}
return new Response("OK", { status: 200 })
```
