# Better Auth + Polar Plugin

> Section 9 from the Polar Payment SDK Comprehensive Reference.
> Covers installation, server setup, client setup, client usage, and CViet's decision on standalone vs plugin.

---

## 9. Better Auth + Polar Plugin

### 9.1 Installation

```bash
pnpm add @polar-sh/better-auth @polar-sh/sdk
```

### 9.2 Server Setup

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth"
import { polar, checkout, portal, usage, webhooks } from "@polar-sh/better-auth"
import { Polar } from "@polar-sh/sdk"

const polarClient = new Polar({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  server: "sandbox",
})

export const auth = betterAuth({
  // ... other config
  plugins: [
    polar({
      client: polarClient,
      createCustomerOnSignUp: true, // Auto-create Polar customer
      use: [
        checkout({
          products: [
            { productId: process.env.POLAR_PRO_PRODUCT_ID!, slug: "pro" },
          ],
          successUrl: "/billing?success=true",
          authenticatedUsersOnly: true,
        }),
        portal(),
        usage(),
        webhooks({
          secret: process.env.POLAR_WEBHOOK_SECRET!,
          onOrderPaid: (payload) => { /* handle */ },
          onCustomerStateChanged: (payload) => { /* handle */ },
        }),
      ],
    }),
  ],
})
```

### 9.3 Client Setup

```typescript
// src/lib/auth-client.ts
import { createAuthClient } from "better-auth/react"
import { polarClient } from "@polar-sh/better-auth/client"

export const authClient = createAuthClient({
  plugins: [polarClient()],
})
```

### 9.4 Client Usage

```typescript
// Checkout
await authClient.checkout({ slug: "pro" })

// Customer portal
await authClient.customer.portal()

// Get customer state
const { data: state } = await authClient.customer.state()

// List subscriptions
const { data: subs } = await authClient.customer.subscriptions.list()

// Usage tracking
await authClient.usage.ingest({
  event: "ai-enhancement",
  metadata: { model: "claude-sonnet-4-6" },
})
```

### 9.5 CViet Decision: Standalone vs Better Auth Plugin

CViet uses standalone `@polar-sh/nextjs` webhooks + manual checkout route, NOT the Better Auth plugin. Reasons:
- Simpler -- fewer moving parts
- More control over checkout flow
- No extra dependency (`@polar-sh/better-auth`)
- Type workaround (`payload: any`) works fine for the version mismatch
