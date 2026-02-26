// =============================================================
// lib/stripe-client.ts — Client-side Stripe.js (lazy loaded)
// =============================================================
// Import in: Client Components that use <Elements> or <EmbeddedCheckout>
// Only loads Stripe.js when getStripe() is first called

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
