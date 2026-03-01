# Better Auth -- Proxy.ts (Next.js 16 Middleware Replacement)

> Section 6 from the comprehensive reference.

---

## 6. Proxy.ts (Next.js 16 Middleware Replacement)

### 6.1 Basic Proxy with Cookie Check

In Next.js 16, `middleware.ts` is replaced by `proxy.ts`. The function name changes from `middleware` to `proxy`.

```typescript
// src/proxy.ts
import { NextRequest, NextResponse } from "next/server"
import { getSessionCookie } from "better-auth/cookies"

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
}
```

**CRITICAL SECURITY NOTE**: `getSessionCookie()` only checks cookie EXISTENCE, NOT validity. It does not verify the signature or check expiration. Always validate the session in the actual page/route handler.

### 6.2 Full Session Validation in Proxy (Next.js 16+)

Next.js 16 proxy runs in Node.js runtime (not Edge), so you can do full database-backed validation:

```typescript
import { NextRequest, NextResponse } from "next/server"
import { auth } from "@/lib/auth"
import { headers } from "next/headers"

export async function proxy(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: await headers()
  })

  if (!session && isProtectedRoute(request.nextUrl.pathname)) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  return NextResponse.next()
}
```

**Trade-off**: Full validation adds a database query to every matched request. For high-traffic apps, prefer cookie-only check in proxy + full validation in the page.

### 6.3 Cookie Cache Check in Proxy

A middle ground -- validates the signed cookie without hitting the database:

```typescript
import { getCookieCache } from "better-auth/cookies"

export async function proxy(request: NextRequest) {
  const session = await getCookieCache(request)

  if (!session && isProtectedRoute(request.nextUrl.pathname)) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  return NextResponse.next()
}
```

Requires `cookieCache.enabled: true` in auth config.

### 6.4 Custom Cookie Prefix in Proxy

If you customized the cookie prefix, pass it to `getSessionCookie`:

```typescript
const session = getSessionCookie(request, {
  cookiePrefix: "my-app",  // matches advanced.cookiePrefix in auth config
})
```
