// =============================================================
// app/api/webhooks/stripe/route.ts — Stripe Webhook Handler
// =============================================================

import { headers } from "next/headers";
import { stripe } from "@/lib/stripe";
import type Stripe from "stripe";

if (!process.env.STRIPE_WEBHOOK_SECRET) {
  throw new Error("Missing STRIPE_WEBHOOK_SECRET environment variable");
}
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

export async function POST(req: Request) {
  // 1. Read raw body (MUST be text, not JSON)
  const body = await req.text();
  const headersList = await headers();
  const signature = headersList.get("stripe-signature");

  if (!signature) {
    return new Response("Missing stripe-signature header", { status: 400 });
  }

  // 2. Verify signature
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      webhookSecret
    );
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    console.error(`Webhook signature verification failed: ${message}`);
    return new Response(`Webhook Error: ${message}`, { status: 400 });
  }

  // 3. Idempotency check (uncomment with your DB)
  // const existing = await db.webhookEvent.findUnique({
  //   where: { stripeEventId: event.id },
  // });
  // if (existing) return new Response("Already processed", { status: 200 });

  // 4. Route event
  try {
    switch (event.type) {
      case "checkout.session.completed":
        await handleCheckoutComplete(
          event.data.object as Stripe.Checkout.Session
        );
        break;

      case "invoice.paid":
        await handleInvoicePaid(event.data.object as Stripe.Invoice);
        break;

      case "invoice.payment_failed":
        await handlePaymentFailed(event.data.object as Stripe.Invoice);
        break;

      case "customer.subscription.created":
      case "customer.subscription.updated":
        await handleSubscriptionChange(
          event.data.object as Stripe.Subscription
        );
        break;

      case "customer.subscription.deleted":
        await handleSubscriptionDeleted(
          event.data.object as Stripe.Subscription
        );
        break;

      case "payment_intent.succeeded":
        await handlePaymentIntentSucceeded(
          event.data.object as Stripe.PaymentIntent
        );
        break;

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }
  } catch (err) {
    console.error(`Error processing ${event.type}:`, err);
    return new Response("Webhook handler error", { status: 500 });
  }

  // 5. Mark as processed (uncomment with your DB)
  // await db.webhookEvent.create({
  //   data: { stripeEventId: event.id, type: event.type, processedAt: new Date() },
  // });

  return new Response("OK", { status: 200 });
}

// =============================================================
// Event Handlers — Customize these for your application
// =============================================================

async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId;
  if (!userId) {
    console.error("Missing userId in checkout session metadata");
    return;
  }

  if (session.mode === "subscription") {
    // TODO: Update user's subscription in database
    console.log(`Subscription created for user ${userId}:`, session.subscription);
  } else if (session.mode === "payment") {
    // TODO: Fulfill one-time purchase
    console.log(`Payment completed for user ${userId}:`, session.amount_total);
  }
}

async function handleInvoicePaid(invoice: Stripe.Invoice) {
  // TODO: Extend subscription access, send receipt
  console.log(`Invoice paid: ${invoice.id}, amount: ${invoice.amount_paid}`);
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  // TODO: Notify user, update status to past_due
  console.log(`Payment failed: ${invoice.id}`);
}

async function handleSubscriptionChange(subscription: Stripe.Subscription) {
  // TODO: Update plan/entitlements in database
  console.log(`Subscription updated: ${subscription.id}, status: ${subscription.status}`);
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  // TODO: Revoke access, downgrade to free plan
  console.log(`Subscription cancelled: ${subscription.id}`);
}

async function handlePaymentIntentSucceeded(paymentIntent: Stripe.PaymentIntent) {
  // TODO: Fulfill order for custom payment flow
  console.log(`PaymentIntent succeeded: ${paymentIntent.id}`);
}
