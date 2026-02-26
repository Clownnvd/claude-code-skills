// =============================================================
// app/actions/portal.ts — Customer Portal Server Action
// =============================================================
// IMPORTANT: Replace getCurrentUser() with your auth implementation

"use server";

import { redirect } from "next/navigation";
import { stripe } from "@/lib/stripe";
import type Stripe from "stripe";

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

// TODO: Replace with your DB query
async function getUserStripeCustomerId(_userId: string): Promise<string> {
  // Example: const user = await db.user.findUniqueOrThrow({ where: { id: userId } });
  // if (!user.stripeCustomerId) throw new Error("No Stripe customer");
  // return user.stripeCustomerId;
  throw new Error("Implement getUserStripeCustomerId() with your database");
}

/**
 * Create a Customer Portal session and redirect
 */
export async function createPortalSession() {
  const user = await getCurrentUser();
  const customerId = await getUserStripeCustomerId(user.id);

  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${BASE_URL}/dashboard`,
  });

  // redirect() throws internally in Next.js — never call inside try/catch
  redirect(session.url);
}

/**
 * Create a portal session with deep link to specific section
 */
export async function createPortalSessionWithFlow(
  flow: "payment_method_update" | "subscription_cancel" | "subscription_update",
  subscriptionId?: string
) {
  const user = await getCurrentUser();
  const customerId = await getUserStripeCustomerId(user.id);

  type FlowData = Stripe.BillingPortal.SessionCreateParams["flow_data"];
  const flowData: FlowData = { type: flow };

  if (flow === "subscription_cancel" && subscriptionId) {
    flowData!.subscription_cancel = { subscription: subscriptionId };
  }
  if (flow === "subscription_update" && subscriptionId) {
    flowData!.subscription_update = { subscription: subscriptionId };
  }

  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${BASE_URL}/dashboard`,
    flow_data: flowData,
  });

  redirect(session.url);
}
