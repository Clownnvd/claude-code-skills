# Polar Checkout Flow Patterns

> Section 3 from the Polar Payment SDK Comprehensive Reference.
> Covers server-side checkout, nextjs helper, embedded checkout, metadata, and external customer IDs.

---

## 3. Checkout Flow Patterns

### 3.1 Pattern A: Server-Side Checkout (Route Handler) -- RECOMMENDED

This is the pattern used by CViet. Create a checkout session server-side, return the URL.

```typescript
// src/app/api/polar/checkout/route.ts
import { NextRequest, NextResponse } from "next/server"
import { auth } from "@/lib/auth"
import { polar } from "@/lib/polar"
import { headers } from "next/headers"

export async function POST(req: NextRequest) {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }

  try {
    const checkout = await polar.checkouts.create({
      products: [process.env.POLAR_PRO_PRODUCT_ID!],
      successUrl: `${process.env.NEXT_PUBLIC_APP_URL}/billing?success=true`,
      customerEmail: session.user.email,
      metadata: {
        userId: session.user.id,
      },
    })

    return NextResponse.json({ url: checkout.url })
  } catch (error) {
    console.error("Polar checkout error:", error)
    return NextResponse.json(
      { error: "Failed to create checkout" },
      { status: 500 }
    )
  }
}
```

**Client-side usage:**
```typescript
async function handleUpgrade() {
  setLoading(true)
  try {
    const res = await fetch("/api/polar/checkout", { method: "POST" })
    const data = await res.json()
    if (data.url) {
      window.location.href = data.url  // Redirect to Polar hosted checkout
    }
  } finally {
    setLoading(false)
  }
}
```

### 3.2 Pattern B: @polar-sh/nextjs Checkout Helper

Simpler but less control. Creates a GET route that redirects to Polar checkout.

```typescript
// src/app/checkout/route.ts
import { Checkout } from "@polar-sh/nextjs"

export const GET = Checkout({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  successUrl: `${process.env.NEXT_PUBLIC_APP_URL}/billing?success=true`,
  server: "sandbox", // or omit for production
})
```

**Usage:** Link to `/checkout?products=PRODUCT_ID&customerEmail=user@example.com&metadata=URL_ENCODED_JSON`

**Supported query params:**
- `products` (required) -- Product ID(s)
- `customerId` -- Polar customer ID
- `customerExternalId` -- Your system's user ID
- `customerEmail` -- Pre-fill email
- `customerName` -- Pre-fill name
- `metadata` -- URL-encoded JSON string (copied to order/subscription)

### 3.3 Pattern C: Embedded Checkout

For in-page checkout without redirect.

```bash
pnpm add @polar-sh/checkout
```

**HTML snippet approach:**
```html
<a href="__CHECKOUT_LINK__" data-polar-checkout data-polar-checkout-theme="light">
  Purchase
</a>
<script defer data-auto-init
  src="https://cdn.jsdelivr.net/npm/@polar-sh/checkout@latest/dist/embed.global.js">
</script>
```

**Programmatic approach (React):**
```tsx
"use client"
import { useEffect, useRef } from "react"
import { PolarEmbedCheckout } from "@polar-sh/checkout"

export function EmbeddedCheckout({ checkoutUrl }: { checkoutUrl: string }) {
  const instanceRef = useRef<PolarEmbedCheckout | null>(null)

  useEffect(() => {
    PolarEmbedCheckout.create(checkoutUrl, {
      theme: "light",
      onLoaded: () => console.log("Checkout loaded"),
      onConfirmed: () => console.log("Payment processing"),
      onSuccess: (event) => {
        console.log("Payment successful", event.detail)
        // Custom success handling
      },
      onClose: () => console.log("Checkout closed"),
    }).then((instance) => {
      instanceRef.current = instance
    })

    return () => instanceRef.current?.close()
  }, [checkoutUrl])

  return null
}
```

**Embedded checkout events:**
| Event | When |
|-------|------|
| `loaded` | Checkout fully initialized |
| `close` | User dismissed checkout |
| `confirmed` | Payment processing started |
| `success` | Purchase completed |

**Gotcha:** Apple Pay / Google Pay require manual domain validation for embedded checkout. Email Polar support with org slug + domain.

### 3.4 Checkout Metadata

Metadata set on checkout is copied to the resulting order AND subscription.

```typescript
const checkout = await polar.checkouts.create({
  products: [productId],
  metadata: {
    userId: "usr_123",       // Key: max 40 chars
    plan: "pro",             // Max 50 key-value pairs
    source: "billing-page",
  },
})
```

### 3.5 Checkout with External Customer ID

Link checkout to your existing user system:

```typescript
const checkout = await polar.checkouts.create({
  products: [productId],
  externalCustomerId: session.user.id, // Your user ID
  customerEmail: session.user.email,
  successUrl: `${baseUrl}/billing?success=true`,
})
```

If a Polar customer with this external ID exists, the order links to them. Otherwise, a new customer is created with this external ID.
