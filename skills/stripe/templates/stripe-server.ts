// =============================================================
// lib/stripe.ts — Server-side Stripe instance
// =============================================================
// Import in: Server Components, Server Actions, Route Handlers
// NEVER import in Client Components (secret key would leak)

import Stripe from "stripe";

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error("Missing STRIPE_SECRET_KEY environment variable");
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: "2026-01-28.clover",
});
