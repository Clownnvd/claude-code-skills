# Polar Webhook Handling

> Section 5 from the Polar Payment SDK Comprehensive Reference.
> Covers setup, CViet handler, manual verification, event types, headers, retries, best practices, IP allowlisting, and local dev.

---

## 5. Webhook Handling

### 5.1 Setup with @polar-sh/nextjs

```typescript
// src/app/api/polar/route.ts (or src/app/api/webhook/polar/route.ts)
import { Webhooks } from "@polar-sh/nextjs"

export const POST = Webhooks({
  webhookSecret: process.env.POLAR_WEBHOOK_SECRET!,

  // Catch-all handler
  onPayload: async (payload) => {
    console.log("Polar event:", payload.type)
  },

  // Granular handlers (23 available)
  onOrderCreated: async (payload) => { /* ... */ },
  onOrderPaid: async (payload) => { /* ... */ },
  onSubscriptionCreated: async (payload) => { /* ... */ },
  onSubscriptionActive: async (payload) => { /* ... */ },
  onSubscriptionCanceled: async (payload) => { /* ... */ },
  onSubscriptionRevoked: async (payload) => { /* ... */ },
  onCustomerStateChanged: async (payload) => { /* ... */ },
})
```

### 5.2 CViet Actual Webhook Handler

```typescript
// src/app/api/polar/route.ts
import { Webhooks } from "@polar-sh/nextjs"
import { db } from "@/lib/db"

export const POST = Webhooks({
  webhookSecret: process.env.POLAR_WEBHOOK_SECRET!,

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onSubscriptionCreated: async (payload: any) => {
    const sub = payload.data
    const userId = sub.metadata?.userId as string | undefined
    if (userId) {
      await db.user.update({
        where: { id: userId },
        data: {
          plan: "PRO",
          polarCustomerId: sub.customerId,
        },
      })
    }
  },

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onSubscriptionCanceled: async (payload: any) => {
    const sub = payload.data
    const userId = sub.metadata?.userId as string | undefined
    if (userId) {
      await db.user.update({
        where: { id: userId },
        data: { plan: "FREE" },
      })
    }
  },

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onSubscriptionRevoked: async (payload: any) => {
    const sub = payload.data
    const userId = sub.metadata?.userId as string | undefined
    if (userId) {
      await db.user.update({
        where: { id: userId },
        data: { plan: "FREE" },
      })
    }
  },
})
```

### 5.3 Manual Webhook Verification (without @polar-sh/nextjs)

```typescript
import { validateEvent, WebhookVerificationError } from "@polar-sh/sdk/webhooks"

export async function POST(req: Request) {
  try {
    const body = await req.text()
    const headers = Object.fromEntries(req.headers.entries())

    const event = validateEvent(
      body,
      headers,
      process.env.POLAR_WEBHOOK_SECRET!,
    )

    // Process event
    switch (event.type) {
      case "subscription.created":
        // ...
        break
      case "subscription.revoked":
        // ...
        break
    }

    return new Response("", { status: 202 })
  } catch (error) {
    if (error instanceof WebhookVerificationError) {
      return new Response("", { status: 403 })
    }
    throw error
  }
}
```

### 5.4 All Available Webhook Event Handlers

| Category | Handler | Event Type |
|----------|---------|------------|
| **Checkout** | `onCheckoutCreated` | `checkout.created` |
| | `onCheckoutUpdated` | `checkout.updated` |
| **Order** | `onOrderCreated` | `order.created` |
| | `onOrderPaid` | `order.paid` |
| | `onOrderRefunded` | `order.refunded` |
| **Refund** | `onRefundCreated` | `refund.created` |
| | `onRefundUpdated` | `refund.updated` |
| **Subscription** | `onSubscriptionCreated` | `subscription.created` |
| | `onSubscriptionUpdated` | `subscription.updated` |
| | `onSubscriptionActive` | `subscription.active` |
| | `onSubscriptionCanceled` | `subscription.canceled` |
| | `onSubscriptionRevoked` | `subscription.revoked` |
| | `onSubscriptionUncanceled` | `subscription.uncanceled` |
| **Product** | `onProductCreated` | `product.created` |
| | `onProductUpdated` | `product.updated` |
| **Benefit** | `onBenefitCreated` | `benefit.created` |
| | `onBenefitUpdated` | `benefit.updated` |
| **Benefit Grant** | `onBenefitGrantCreated` | `benefit_grant.created` |
| | `onBenefitGrantUpdated` | `benefit_grant.updated` |
| | `onBenefitGrantRevoked` | `benefit_grant.revoked` |
| **Customer** | `onCustomerCreated` | `customer.created` |
| | `onCustomerUpdated` | `customer.updated` |
| | `onCustomerDeleted` | `customer.deleted` |
| | `onCustomerStateChanged` | `customer.state_changed` |
| **Organization** | `onOrganizationUpdated` | `organization.updated` |
| **Catch-all** | `onPayload` | Any event |

### 5.5 Webhook Headers (Standard Webhooks Spec)

| Header | Purpose |
|--------|---------|
| `webhook-id` | Unique delivery identifier (use for idempotency) |
| `webhook-timestamp` | Unix timestamp |
| `webhook-signature` | HMAC signature (base64 encoded secret) |

### 5.6 Webhook Retry Behavior

| Aspect | Value |
|--------|-------|
| Timeout | 10 seconds (respond within 2 seconds recommended) |
| Retries | Up to 10 attempts with exponential backoff |
| Auto-disable | After 10 consecutive failures (email notification sent) |
| Redirect following | NO -- configure final destination URL directly |

### 5.7 Webhook Best Practices

1. **Respond immediately** -- return `202` and queue async processing
2. **Idempotency** -- use `webhook-id` + event type + resource ID to deduplicate
3. **Don't revoke on canceled** -- wait for `subscription.revoked`
4. **Exclude from auth** -- webhook routes must not be behind auth middleware/proxy
5. **No dead letter queue** -- Polar has no DLQ; failed events after 10 retries are lost
6. **Cloudflare Bot Fight Mode** -- will block webhook deliveries; whitelist Polar IPs

### 5.8 Polar Webhook IP Addresses (for allowlisting)

```
3.134.238.10
3.129.111.220
52.15.118.168
74.220.50.0/24
74.220.58.0/24
```

### 5.9 Local Development Webhook Testing

Use ngrok to tunnel webhooks to localhost:

```bash
ngrok http 3000
# Copy the HTTPS URL
# Set webhook endpoint to: https://xxxx.ngrok.io/api/polar
```
