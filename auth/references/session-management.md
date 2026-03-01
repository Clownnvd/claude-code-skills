# Better Auth -- Session Management Patterns

> Section 3 from the comprehensive reference.

---

## 3. Session Management Patterns

### 3.1 Server Components -- Getting Session

```typescript
import { auth } from "@/lib/auth"
import { headers } from "next/headers"
import { redirect } from "next/navigation"

export default async function ProtectedPage() {
  const session = await auth.api.getSession({
    headers: await headers()  // MUST await in Next.js 16
  })

  if (!session) {
    redirect("/login")
  }

  return <div>Welcome, {session.user.name}</div>
}
```

**CRITICAL**: In Next.js 16, `headers()` is async and MUST be awaited.

### 3.2 Server Actions -- Getting & Setting Session

```typescript
"use server"

import { auth } from "@/lib/auth"
import { headers } from "next/headers"

export async function getProfile() {
  const session = await auth.api.getSession({
    headers: await headers()
  })
  if (!session) throw new Error("Unauthorized")
  return session.user
}
```

For server actions that need to SET cookies (e.g., signIn), use the `nextCookies` plugin:

```typescript
// src/lib/auth.ts
import { nextCookies } from "better-auth/next-js"

export const auth = betterAuth({
  // ... config
  plugins: [nextCookies()],  // MUST be LAST plugin
})
```

Then in server actions:

```typescript
"use server"
import { auth } from "@/lib/auth"

export async function serverSignIn(email: string, password: string) {
  const result = await auth.api.signInEmail({
    body: { email, password }
  })
  return result
}
```

### 3.3 Route Handlers -- Getting Session

```typescript
import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"

export async function GET(request: Request) {
  const session = await auth.api.getSession({
    headers: request.headers
  })

  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }

  // ... use session.user.id
}
```

### 3.4 Client Components -- useSession Hook

```typescript
"use client"
import { useSession } from "@/lib/auth-client"

export function UserProfile() {
  const { data: session, isPending } = useSession()

  if (isPending) return <div>Loading...</div>
  if (!session) return <div>Not logged in</div>

  return <div>{session.user.name}</div>
}
```

**WARNING**: Do NOT use `useSession` in `layout.tsx` -- it causes performance issues.
Use `getSession` instead for one-time checks.

### 3.5 Session with `use cache` Directive

The `use cache` directive conflicts with cookie/header access. Extract headers BEFORE the cache boundary:

```typescript
// WRONG -- will crash
async function getCachedData() {
  "use cache"
  const session = await auth.api.getSession({
    headers: await headers()  // ERROR: can't use headers() inside "use cache"
  })
}

// CORRECT -- extract cookies first, pass as argument
async function getCachedUserData(headerString: string) {
  "use cache"
  // Use the pre-extracted header string
  const session = await auth.api.getSession({
    headers: new Headers({ cookie: headerString })
  })
  return session
}

// In server component:
export default async function Page() {
  const cookieHeader = (await cookies()).toString()
  const data = await getCachedUserData(cookieHeader)
}
```

### 3.6 Cookie Caching (Performance Optimization)

Reduces database hits by caching session data in a signed cookie:

```typescript
export const auth = betterAuth({
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60,        // 5 minutes -- balance between freshness and performance
      strategy: "compact",    // smallest size, signed but readable
    },
  },
})
```

**Strategies**:
| Strategy | Size | Security | Use Case |
|----------|------|----------|----------|
| `compact` | Smallest | Signed | Internal apps, high performance |
| `jwt` | Medium | Signed | JWT compatibility, third-party tools |
| `jwe` | Largest | Encrypted | Maximum security, sensitive data |

**Caveat**: Revoked sessions may persist until cookie expires. For immediate revocation, disable cookie caching or use a very short maxAge.

### 3.7 Stateless Sessions (No Database)

```typescript
export const auth = betterAuth({
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 7 * 24 * 60 * 60,  // 7 days
      strategy: "jwe",
      refreshCache: true,          // auto-refresh at 80% of maxAge
    },
    account: {
      storeStateStrategy: "cookie",
      storeAccountCookie: true,
    },
  },
})
```

### 3.8 Session Freshness

Some operations require a "fresh" session (recently authenticated):

```typescript
export const auth = betterAuth({
  session: {
    freshAge: 60 * 5,  // session is "fresh" for 5 minutes after login
    // Set to 0 to disable freshness checks
  },
})
```
