# Pricing Page

## Server Component — Fetch Prices from Stripe

```typescript
// app/pricing/page.tsx
import { stripe } from "@/lib/stripe";
import { PricingCard } from "./pricing-card";

export default async function PricingPage() {
  const { data: prices } = await stripe.prices.list({
    active: true,
    expand: ["data.product"],
    type: "recurring",
  });

  // Sort by unit_amount ascending
  const sorted = prices
    .filter((p) => p.unit_amount !== null)
    .sort((a, b) => (a.unit_amount ?? 0) - (b.unit_amount ?? 0));

  return (
    <section className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto py-16 px-4">
      {sorted.map((price) => {
        const product = price.product as import("stripe").Stripe.Product;
        return (
          <PricingCard
            key={price.id}
            priceId={price.id}
            name={product.name}
            description={product.description}
            amount={price.unit_amount!}
            currency={price.currency}
            interval={price.recurring!.interval}
            features={product.marketing_features?.map((f) => f.name ?? "") ?? []}
          />
        );
      })}
    </section>
  );
}
```

## Client Component — Pricing Card with Checkout

```tsx
// app/pricing/pricing-card.tsx
"use client";

import { useTransition } from "react";
import { createSubscriptionCheckout } from "@/app/actions/checkout";

interface PricingCardProps {
  priceId: string;
  name: string;
  description: string | null;
  amount: number;
  currency: string;
  interval: string;
  features: string[];
}

export function PricingCard({
  priceId, name, description, amount, currency, interval, features,
}: PricingCardProps) {
  const [isPending, startTransition] = useTransition();

  const formatted = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(amount / 100);

  return (
    <div className="border rounded-2xl p-8 flex flex-col">
      <h3 className="text-xl font-bold">{name}</h3>
      {description && <p className="text-gray-500 mt-2">{description}</p>}
      <p className="text-4xl font-bold mt-4">
        {formatted}<span className="text-base font-normal">/{interval}</span>
      </p>
      <ul className="mt-6 space-y-2 flex-1">
        {features.map((f) => (
          <li key={f} className="flex items-center gap-2">
            <span>✓</span> {f}
          </li>
        ))}
      </ul>
      <button
        onClick={() => startTransition(() => createSubscriptionCheckout(priceId))}
        disabled={isPending}
        className="mt-8 w-full py-3 rounded-lg bg-black text-white disabled:opacity-50"
      >
        {isPending ? "Redirecting..." : "Get Started"}
      </button>
    </div>
  );
}
```

## Toggle Monthly / Yearly

```tsx
"use client";

import { useState } from "react";

export function PricingToggle({ monthlyPrices, yearlyPrices }) {
  const [annual, setAnnual] = useState(false);
  const prices = annual ? yearlyPrices : monthlyPrices;

  return (
    <>
      <div className="flex items-center gap-3 justify-center mb-8">
        <span>Monthly</span>
        <button
          onClick={() => setAnnual(!annual)}
          className={`w-14 h-7 rounded-full transition ${annual ? "bg-black" : "bg-gray-300"}`}
        >
          <span className={`block w-5 h-5 bg-white rounded-full transition ${annual ? "translate-x-8" : "translate-x-1"}`} />
        </button>
        <span>Yearly <span className="text-green-600 text-sm">Save 20%</span></span>
      </div>
      {/* Render prices */}
    </>
  );
}
```

## Key Points
- Fetch prices server-side — Stripe is the source of truth
- Use `product.marketing_features` for feature lists (set in Stripe Dashboard)
- Use `useTransition` for non-blocking checkout redirect
- Never hardcode prices — always fetch from Stripe API
- Add `revalidate` or `cache: "no-store"` if prices change frequently
