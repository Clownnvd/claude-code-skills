# Webhooks

## Route Handler (Next.js App Router)

```typescript
// app/api/webhooks/stripe/route.ts
import { headers } from "next/headers";
import { stripe } from "@/lib/stripe";
import type Stripe from "stripe";

export async function POST(req: Request) {
  const body = await req.text(); // MUST use text(), not json()
  const headersList = await headers();
  const signature = headersList.get("stripe-signature");

  if (!signature) {
    return new Response("Missing stripe-signature", { status: 400 });
  }

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error("Webhook signature verification failed:", err);
    return new Response("Invalid signature", { status: 400 });
  }

  try {
    await handleEvent(event);
  } catch (err) {
    console.error(`Error processing ${event.type}:`, err);
    return new Response("Webhook handler error", { status: 500 });
  }

  return new Response("OK", { status: 200 });
}
```

## CRITICAL: Raw Body

Signature verification requires the raw request body. Use `req.text()` — NEVER `req.json()`. JSON parsing changes whitespace/order and breaks verification.

## Event Router

```typescript
async function handleEvent(event: Stripe.Event) {
  switch (event.type) {
    case "checkout.session.completed":
      await handleCheckoutComplete(event.data.object as Stripe.Checkout.Session);
      break;
    case "invoice.paid":
      await handleInvoicePaid(event.data.object as Stripe.Invoice);
      break;
    case "invoice.payment_failed":
      await handlePaymentFailed(event.data.object as Stripe.Invoice);
      break;
    case "customer.subscription.updated":
      await handleSubscriptionUpdated(event.data.object as Stripe.Subscription);
      break;
    case "customer.subscription.deleted":
      await handleSubscriptionDeleted(event.data.object as Stripe.Subscription);
      break;
    case "payment_intent.succeeded":
      await handlePaymentSucceeded(event.data.object as Stripe.PaymentIntent);
      break;
    default:
      console.log(`Unhandled event: ${event.type}`);
  }
}
```

## Idempotency (Prevent Duplicate Processing)

```typescript
// Using a database (e.g., Prisma)
async function handleEvent(event: Stripe.Event) {
  // Check if already processed
  const existing = await db.webhookEvent.findUnique({
    where: { stripeEventId: event.id },
  });
  if (existing) return; // Already processed

  // Process event
  await processEvent(event);

  // Mark as processed
  await db.webhookEvent.create({
    data: {
      stripeEventId: event.id,
      type: event.type,
      processedAt: new Date(),
    },
  });
}
```

## Handler Examples

```typescript
async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId;
  if (!userId) throw new Error("Missing userId in metadata");

  if (session.mode === "subscription") {
    await db.user.update({
      where: { id: userId },
      data: {
        stripeCustomerId: session.customer as string,
        stripeSubscriptionId: session.subscription as string,
        plan: "pro",
      },
    });
  } else if (session.mode === "payment") {
    await db.order.create({
      data: {
        userId,
        amount: session.amount_total!,
        status: "paid",
        stripeSessionId: session.id,
      },
    });
  }
}

async function handleSubscriptionDeleted(sub: Stripe.Subscription) {
  await db.user.update({
    where: { stripeSubscriptionId: sub.id },
    data: { plan: "free", stripeSubscriptionId: null },
  });
}
```

## Next.js Config — Disable Body Parsing

Not needed in App Router. `req.text()` works directly. No additional config required.

## Key Points
- ALWAYS verify signature — never skip in production
- Return 200 within 5 seconds — process async for heavy operations
- Stripe retries failed webhooks (3 times over 72 hours)
- Set `metadata` on Checkout/Subscription to link to your user
- Use idempotency to handle webhook retries safely
