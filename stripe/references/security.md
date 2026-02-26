# Security

## API Key Management

| Key | Prefix | Where |
|-----|--------|-------|
| Secret key | `sk_test_` / `sk_live_` | Server only, env vars |
| Publishable key | `pk_test_` / `pk_live_` | Client OK (`NEXT_PUBLIC_`) |
| Webhook secret | `whsec_` | Server only, env vars |

### Rules
- NEVER use `NEXT_PUBLIC_` prefix for secret keys
- NEVER commit keys to version control
- NEVER log secret keys or webhook secrets
- Use separate keys for test vs production
- Rotate keys immediately if exposed

```bash
# .gitignore
.env
.env.local
.env.production
```

## Webhook Signature Verification

```typescript
// ALWAYS verify — never skip (Next.js App Router pattern)
const body = await req.text();         // Raw body — NOT req.json()
const headersList = await headers();   // Next.js 15+ async headers()
const signature = headersList.get("stripe-signature")!;

const event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
```

Skip verification = anyone can send fake events to your webhook endpoint.

## Idempotency Keys

Prevent duplicate charges on network failures:

```typescript
import { v4 as uuid } from "uuid";

// All mutating operations should use idempotency keys
const pi = await stripe.paymentIntents.create(
  { amount: 5000, currency: "usd" },
  { idempotencyKey: uuid() }
);

const session = await stripe.checkout.sessions.create(
  { /* ... */ },
  { idempotencyKey: `checkout_${userId}_${orderId}` }
);
```

| Retry scenario | Idempotency key |
|----------------|-----------------|
| Network timeout | Same key (safe to retry) |
| 5xx server error | Same key (safe to retry) |
| 4xx client error | New key (fix the request first) |
| 429 rate limit | New key (conditions may have changed) |

Keys auto-expire after 24 hours.

## Amount Validation

```typescript
// ALWAYS validate amounts server-side
export async function createCheckout(priceId: string) {
  // Fetch price from Stripe (source of truth)
  const price = await stripe.prices.retrieve(priceId);

  if (!price.active) throw new Error("Price is not active");

  // Use Stripe's price, never trust client-sent amounts
  const session = await stripe.checkout.sessions.create({
    line_items: [{ price: price.id, quantity: 1 }],
    // ...
  });
}
```

Never accept `amount` from the client for payment creation. Always reference a Stripe Price ID or validate server-side.

## Content Security Policy for Stripe.js

```typescript
// next.config.js
const nextConfig = {
  async headers() {
    return [{
      source: "/(.*)",
      headers: [{
        key: "Content-Security-Policy",
        value: [
          "default-src 'self'",
          "script-src 'self' https://js.stripe.com",
          "frame-src https://js.stripe.com https://hooks.stripe.com",
          "connect-src 'self' https://api.stripe.com",
        ].join("; "),
      }],
    }];
  },
};
```

## PCI Compliance Checklist

| Requirement | How Stripe Handles |
|-------------|-------------------|
| Card data handling | Stripe.js / Checkout — never touches your server |
| TLS/HTTPS | Stripe enforces HTTPS for all API + webhooks |
| Key storage | Use env vars, never code/logs/commits |
| Access control | Use restricted keys for limited permissions |
| Vulnerability scans | Stripe is Level 1 PCI certified |

## Restricted API Keys

Create keys with limited permissions in Dashboard → Developers → API Keys:

```
# Example: key that can only create Checkout Sessions
- Checkout Sessions: Write
- All other resources: None
```

Use restricted keys for specific services/microservices.

## Key Points
- Use Checkout or Elements — never handle raw card data
- Verify webhook signatures — no exceptions
- Use idempotency keys on all mutating API calls
- Validate amounts server-side — never trust client input
- Add Stripe domains to CSP headers
- Use restricted keys for least-privilege access
