// =============================================================
// lib/stripe.ts — Server-side Stripe instance
// =============================================================
// Import in Server Components, Server Actions, Route Handlers

import Stripe from "stripe";

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error("Missing STRIPE_SECRET_KEY environment variable");
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: "2026-01-28.clover",
});

// =============================================================
// lib/stripe-client.ts — Client-side Stripe.js (lazy loaded)
// =============================================================
// IMPORTANT: Copy this section into a separate file: lib/stripe-client.ts
// Required for Payment Intents (Elements) and Embedded Checkout

import { loadStripe, type Stripe as StripeClient } from "@stripe/stripe-js";

let stripePromise: Promise<StripeClient | null>;

export function getStripe() {
  if (!stripePromise) {
    stripePromise = loadStripe(
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
    );
  }
  return stripePromise;
}
