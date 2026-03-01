# Better Auth -- CViet Project Patterns

> Section 12 from the comprehensive reference.

---

## 12. CViet Project Patterns

### 12.1 Project-Specific Auth Configuration

CViet uses the following specific patterns:

**Auth Config** (`src/lib/auth.ts`):
```typescript
import { betterAuth } from "better-auth"
import { prismaAdapter } from "better-auth/adapters/prisma"
import { db } from "@/lib/db"

export const auth = betterAuth({
  database: prismaAdapter(db, { provider: "postgresql" }),
  emailAndPassword: { enabled: true },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  trustedOrigins: [process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"],
})

export type Session = typeof auth.$Infer.Session
```

**Client** (`src/lib/auth-client.ts`):
```typescript
"use client"
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
})

export const { signIn, signUp, signOut, useSession, getSession } = authClient
```

**Proxy** (`src/proxy.ts`):
```typescript
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

### 12.2 Extended Prisma Schema

CViet extends the standard Better Auth schema with:
- `User.polarCustomerId` -- Polar payment integration
- `User.plan` (enum: FREE | PRO) -- subscription tier
- `User.aiUsageThisMonth` / `aiUsageResetAt` -- AI usage tracking
- `CV` model -- the core business data

### 12.3 Client-Side Validation

CViet uses Zod schemas for client-side validation before auth calls:

```typescript
// src/lib/validations.ts
export const loginSchema = z.object({
  email: z.string().email("Email khong hop le"),
  password: z.string().min(8, "Mat khau toi thieu 8 ky tu"),
})

export const signupSchema = z.object({
  name: z.string().min(2, "Ten toi thieu 2 ky tu").max(50),
  email: z.string().email("Email khong hop le"),
  password: z.string()
    .min(8, "Mat khau toi thieu 8 ky tu")
    .regex(/[A-Z]/, "Phai co it nhat 1 chu hoa")
    .regex(/[0-9]/, "Phai co it nhat 1 chu so"),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Mat khau xac nhan khong khop",
  path: ["confirmPassword"],
})
```

### 12.4 Auth Error Handling Pattern (Vietnamese)

```typescript
const { error: authError } = await authClient.signIn.email({
  email, password,
  callbackURL: "/dashboard",
})
if (authError) {
  setError(authError.message || "Email hoac mat khau khong dung")
} else {
  router.push("/dashboard")
}
```

### 12.5 Google OAuth UI Pattern

CViet implements Google OAuth as the primary CTA with email/password as fallback, using a divider with "HOAC" (Vietnamese for "OR").

### 12.6 Route Protection Strategy

CViet uses a two-layer approach:
1. **Proxy** (optimistic): Cookie existence check for fast redirects
2. **Page/API** (authoritative): Full `auth.api.getSession()` for data access

Protected routes: `/dashboard/*`, `/cv/*`, `/billing/*`
Public routes: `/`, `/login`, `/signup`, landing pages
