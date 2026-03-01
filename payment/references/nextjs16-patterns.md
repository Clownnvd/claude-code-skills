# Polar -- Next.js 16 Specific Patterns

> Section 8 from the Polar Payment SDK Comprehensive Reference.
> Covers proxy.ts behavior, async APIs, webhook route exclusion, Server Actions for checkout, and next.config.ts.

---

## 8. Next.js 16 Specific Patterns

### 8.1 proxy.ts Does NOT Affect API Routes

Next.js 16 renamed `middleware.ts` to `proxy.ts`, but API routes (`/api/*`) are NOT affected. Webhook routes work normally:

```typescript
// src/proxy.ts -- auth guard
export function proxy(request: NextRequest) {
  const session = getSessionCookie(request)
  const isProtected =
    request.nextUrl.pathname.startsWith("/dashboard") ||
    request.nextUrl.pathname.startsWith("/cv") ||
    request.nextUrl.pathname.startsWith("/billing")

  if (isProtected && !session) {
    return NextResponse.redirect(new URL("/login", request.url))
  }
  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*", "/cv/:path*", "/billing/:path*"],
  // NOTE: /api/polar/* is NOT matched -- webhooks pass through
}
```

### 8.2 Async APIs in Route Handlers

Next.js 16 requires awaiting `headers()`, `cookies()`, `params`:

```typescript
// CORRECT (Next.js 16)
export async function POST(req: NextRequest) {
  const session = await auth.api.getSession({ headers: await headers() })
  // ...
}

// WRONG (will crash)
export async function POST(req: NextRequest) {
  const session = await auth.api.getSession({ headers: headers() }) // Missing await
}
```

### 8.3 Webhook Route Excluded from Proxy

Ensure your `proxy.ts` matcher does NOT include `/api/polar`:

```typescript
export const config = {
  matcher: ["/dashboard/:path*", "/cv/:path*", "/billing/:path*"],
  // DO NOT add: "/api/:path*" -- would block webhooks
}
```

### 8.4 Server Actions for Checkout

Alternative to API route -- use Server Actions:

```typescript
// src/actions/checkout.ts
"use server"
import { polar } from "@/lib/polar"
import { auth } from "@/lib/auth"
import { headers } from "next/headers"
import { redirect } from "next/navigation"

export async function createCheckout() {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) redirect("/login")

  const checkout = await polar.checkouts.create({
    products: [process.env.POLAR_PRO_PRODUCT_ID!],
    successUrl: `${process.env.NEXT_PUBLIC_APP_URL}/billing?success=true`,
    customerEmail: session.user.email,
    metadata: { userId: session.user.id },
  })

  redirect(checkout.url)
}
```

### 8.5 next.config.ts -- No Special Polar Config Needed

```typescript
// next.config.ts
import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  serverExternalPackages: ["@react-pdf/renderer"], // Not needed for Polar
  compiler: {}, // Required for Next.js 16.1.6 (prevents undefined access)
}

export default nextConfig
```
