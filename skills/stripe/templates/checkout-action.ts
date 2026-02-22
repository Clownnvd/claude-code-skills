// =============================================================
// app/actions/checkout.ts — Checkout Session Server Actions
// =============================================================
// IMPORTANT: Replace getCurrentUser() with your auth implementation

"use server";

import { redirect } from "next/navigation";
import { stripe } from "@/lib/stripe";

if (!process.env.NEXT_PUBLIC_APP_URL) {
  throw new Error("Missing NEXT_PUBLIC_APP_URL environment variable");
}
const BASE_URL = process.env.NEXT_PUBLIC_APP_URL;

// TODO: Replace with your auth implementation
async function getCurrentUser() {
  // Example: const session = await auth();
  // if (!session?.user) throw new Error("Not authenticated");
  // return session.user;
  throw new Error("Implement getCurrentUser() with your auth provider");
}

/**
 * Create a Checkout Session for one-time payment
 */
export async function createOneTimeCheckout(priceId: string) {
  const user = await getCurrentUser();

  const session = await stripe.checkout.sessions.create({
    mode: "payment",
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${BASE_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${BASE_URL}/pricing`,
    allow_promotion_codes: true,
    metadata: { userId: user.id, priceId },
  });

  // redirect() throws internally in Next.js — never call inside try/catch
  if (!session.url) throw new Error("Checkout session URL is null");
  redirect(session.url);
}

/**
 * Create a Checkout Session for subscription
 */
export async function createSubscriptionCheckout(priceId: string) {
  const user = await getCurrentUser();

  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    customer_email: user.email,
    customer_creation: "always",
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${BASE_URL}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${BASE_URL}/pricing`,
    allow_promotion_codes: true,
    subscription_data: {
      metadata: { userId: user.id },
      // trial_period_days: 14, // Uncomment for free trial
    },
    metadata: { userId: user.id, priceId },
  });

  if (!session.url) throw new Error("Checkout session URL is null");
  redirect(session.url);
}

/**
 * Create a Checkout Session for existing Stripe customer
 */
export async function createCheckoutForExistingCustomer(
  priceId: string,
  mode: "payment" | "subscription" = "subscription"
) {
  const user = await getCurrentUser();

  // TODO: Look up stripeCustomerId from your database
  // const dbUser = await db.user.findUniqueOrThrow({ where: { id: user.id } });
  // const customerId = dbUser.stripeCustomerId;
  // if (!customerId) throw new Error("No Stripe customer found");

  const customerId = ""; // Replace with DB lookup above

  const session = await stripe.checkout.sessions.create({
    mode,
    customer: customerId,
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${BASE_URL}/dashboard`,
    cancel_url: `${BASE_URL}/pricing`,
    allow_promotion_codes: true,
    metadata: { userId: user.id, priceId },
  });

  if (!session.url) throw new Error("Checkout session URL is null");
  redirect(session.url);
}
