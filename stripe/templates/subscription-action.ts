// =============================================================
// app/actions/subscription.ts — Subscription Server Actions
// =============================================================
// IMPORTANT: Replace getCurrentUser() with your auth implementation
// (e.g., NextAuth, Clerk, Lucia, custom session)

"use server";

import { stripe } from "@/lib/stripe";
import type Stripe from "stripe";

// TODO: Replace with your auth implementation
async function getCurrentUser() {
  // Example with NextAuth:
  // const session = await auth();
  // if (!session?.user?.id) throw new Error("Not authenticated");
  // return session.user;
  throw new Error("Implement getCurrentUser() with your auth provider");
}

// TODO: Replace with your DB query
async function getUserStripeIds(_userId: string) {
  // Example with Prisma:
  // const user = await db.user.findUniqueOrThrow({ where: { id: userId } });
  // return { customerId: user.stripeCustomerId, subscriptionId: user.stripeSubscriptionId };
  throw new Error("Implement getUserStripeIds() with your database");
}

/**
 * Cancel subscription at period end (grace period)
 */
export async function cancelSubscription() {
  const user = await getCurrentUser();
  const { subscriptionId } = await getUserStripeIds(user.id);
  if (!subscriptionId) throw new Error("No active subscription");

  const subscription = await stripe.subscriptions.update(subscriptionId, {
    cancel_at_period_end: true,
  });

  return {
    status: subscription.status,
    cancelAt: subscription.cancel_at
      ? new Date(subscription.cancel_at * 1000).toISOString()
      : null,
    currentPeriodEnd: new Date(
      subscription.current_period_end * 1000
    ).toISOString(),
  };
}

/**
 * Reactivate a subscription scheduled for cancellation
 */
export async function reactivateSubscription() {
  const user = await getCurrentUser();
  const { subscriptionId } = await getUserStripeIds(user.id);
  if (!subscriptionId) throw new Error("No active subscription");

  const subscription = await stripe.subscriptions.update(subscriptionId, {
    cancel_at_period_end: false,
  });

  return { status: subscription.status };
}

/**
 * Switch subscription to a different price (plan change)
 */
export async function updateSubscriptionPlan(newPriceId: string) {
  // Validate price is in your allowed list
  // const ALLOWED_PRICES = ["price_basic", "price_pro", "price_enterprise"];
  // if (!ALLOWED_PRICES.includes(newPriceId)) throw new Error("Invalid price");

  const user = await getCurrentUser();
  const { subscriptionId } = await getUserStripeIds(user.id);
  if (!subscriptionId) throw new Error("No active subscription");

  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  const currentItem = subscription.items.data[0];
  if (!currentItem) throw new Error("No subscription item found");

  const updated = await stripe.subscriptions.update(subscriptionId, {
    items: [{ id: currentItem.id, price: newPriceId }],
    proration_behavior: "create_prorations",
  });

  return {
    status: updated.status,
    currentPrice: newPriceId,
  };
}

/**
 * Get subscription details for display
 * Note: Consider calling this directly in Server Components instead of as a Server Action
 */
export async function getSubscriptionDetails() {
  const user = await getCurrentUser();
  const { subscriptionId } = await getUserStripeIds(user.id);
  if (!subscriptionId) return null;

  const subscription = await stripe.subscriptions.retrieve(subscriptionId, {
    expand: ["default_payment_method", "items.data.price.product"],
  });

  const item = subscription.items.data[0];
  const price = item?.price;
  const product = price?.product as Stripe.Product | undefined;

  return {
    id: subscription.id,
    status: subscription.status,
    cancelAtPeriodEnd: subscription.cancel_at_period_end,
    currentPeriodEnd: new Date(
      subscription.current_period_end * 1000
    ).toISOString(),
    plan: {
      name: product?.name ?? "Unknown",
      amount: price?.unit_amount ?? 0,
      currency: price?.currency ?? "usd",
      interval: price?.recurring?.interval ?? "month",
    },
  };
}

/**
 * Preview upcoming invoice (show estimated charges)
 * Uses createPreview (replaces deprecated retrieveUpcoming in API 2025-03-31+)
 */
export async function previewUpcomingInvoice() {
  const user = await getCurrentUser();
  const { customerId, subscriptionId } = await getUserStripeIds(user.id);
  if (!customerId) throw new Error("No Stripe customer");

  const invoice = await stripe.invoices.createPreview({
    customer: customerId,
    subscription: subscriptionId ?? undefined,
  });

  return {
    amountDue: invoice.amount_due,
    currency: invoice.currency,
    lines: invoice.lines.data.map((line) => ({
      description: line.description,
      amount: line.amount,
    })),
  };
}
