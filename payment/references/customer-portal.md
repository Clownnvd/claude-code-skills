# Polar Customer Portal Integration

> Section 6 from the Polar Payment SDK Comprehensive Reference.
> Covers hosted portal, pre-authenticated links, portal route with @polar-sh/nextjs, and customer state API.

---

## 6. Customer Portal Integration

### 6.1 Polar Hosted Portal

Customers can directly access: `https://polar.sh/{your-org-slug}/portal`

They authenticate with their purchase email. Features:
- View orders and subscriptions
- Access receipts and invoices
- Update payment methods
- Cancel/manage subscriptions
- Access granted benefits

### 6.2 Pre-Authenticated Portal Link (SDK)

```typescript
import { polar } from "@/lib/polar"

const result = await polar.customerSessions.create({
  customerId: polarCustomerId, // Polar's customer ID
})

// Redirect to result.customerPortalUrl
```

### 6.3 Portal Route with @polar-sh/nextjs

```typescript
// src/app/api/portal/route.ts
import { CustomerPortal } from "@polar-sh/nextjs"

export const GET = CustomerPortal({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  getCustomerId: async (req) => {
    // Look up the Polar customer ID for the authenticated user
    const session = await getServerSession()
    const user = await db.user.findUnique({ where: { id: session.user.id } })
    return user?.polarCustomerId ?? ""
  },
  server: "sandbox", // or "production"
})
```

**Usage:** Redirect users to `/api/portal` from the billing page.

### 6.4 Customer State API

Get comprehensive customer data in a single call:

```typescript
// By Polar customer ID
const state = await polar.customers.getState(polarCustomerId)

// By your external user ID
const state = await polar.customers.getStateExternal(userId)
```

Returns: active subscriptions, granted benefits, active meters with balances.
