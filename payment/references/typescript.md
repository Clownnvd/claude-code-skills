# Polar Type Safety Patterns

> Section 10 from the Polar Payment SDK Comprehensive Reference.
> Covers webhook payload types, proper types when versions align, checkout response type, customer state type, and metadata type safety.

---

## 10. Type Safety Patterns

### 10.1 Webhook Payload Types (Version Mismatch Workaround)

When `@polar-sh/sdk` version doesn't match `@polar-sh/nextjs` peer dependency:

```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any
onSubscriptionCreated: async (payload: any) => {
  const sub = payload.data
  const userId = sub.metadata?.userId as string | undefined
  // ...
}
```

### 10.2 Proper Types (When Versions Align)

```typescript
import type {
  WebhookSubscriptionCreatedPayload,
  WebhookSubscriptionRevokedPayload,
} from "@polar-sh/sdk/models/components"

onSubscriptionCreated: async (payload: WebhookSubscriptionCreatedPayload) => {
  const sub = payload.data
  const userId = sub.metadata?.userId // Properly typed
}
```

### 10.3 Checkout Response Type

```typescript
import type { Checkout } from "@polar-sh/sdk/models/components"

const checkout: Checkout = await polar.checkouts.create({
  products: [productId],
  successUrl: "...",
})
// checkout.url -- string
// checkout.id -- string
// checkout.clientSecret -- string (for embedded checkout)
```

### 10.4 Customer State Type

```typescript
import type { CustomerState } from "@polar-sh/sdk/models/components"

const state: CustomerState = await polar.customers.getState(customerId)
// state.activeSubscriptions -- Subscription[]
// state.grantedBenefits -- BenefitGrant[]
// state.activeMeters -- CustomerMeter[]
```

### 10.5 Metadata Type Safety

```typescript
// Define your metadata shape
interface CheckoutMetadata {
  userId: string
  source?: string
}

// Type-safe metadata extraction
function extractUserId(metadata: Record<string, unknown> | null): string | null {
  if (!metadata) return null
  const userId = metadata.userId
  return typeof userId === "string" ? userId : null
}
```
