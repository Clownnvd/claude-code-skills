# Redirecting

> Source: https://nextjs.org/docs/app/guides/redirecting (v16.1.6)

## API Overview

| API | Purpose | Where | Status Code |
|-----|---------|-------|-------------|
| `redirect()` | After mutation/event | Server Components, Server Actions, Route Handlers | 307 (default) / 303 (Server Action) |
| `permanentRedirect()` | After mutation/event | Server Components, Server Actions, Route Handlers | 308 |
| `useRouter()` | Client-side event handler | Client Components | N/A |
| `redirects` in config | Path-based redirect | `next.config.ts` | 307 or 308 |
| `NextResponse.redirect` | Conditional redirect | Middleware (`proxy.ts`) | Any |

## `redirect()`

```typescript
'use server'
import { redirect } from 'next/navigation'
import { revalidatePath } from 'next/cache'

export async function createPost(id: string) {
  try {
    // Call database
  } catch (error) {
    // Handle errors
  }
  revalidatePath('/posts')
  redirect(`/post/${id}`) // must be OUTSIDE try/catch (throws internally)
}
```

| Note | Detail |
|------|--------|
| Throws | Call outside `try/catch` |
| Server Action | Returns 303 instead of 307 |
| Client Components | Allowed during render, NOT in event handlers |
| External URLs | Accepted (absolute URLs) |

## `permanentRedirect()`

```typescript
'use server'
import { permanentRedirect } from 'next/navigation'
import { revalidateTag } from 'next/cache'

export async function updateUsername(username: string, formData: FormData) {
  // ... update DB
  revalidateTag('username')
  permanentRedirect(`/profile/${username}`) // 308 permanent
}
```

## `useRouter()` (Client-Side)

```typescript
'use client'
import { useRouter } from 'next/navigation'

export default function Page() {
  const router = useRouter()
  return (
    <button type="button" onClick={() => router.push('/dashboard')}>
      Dashboard
    </button>
  )
}
```

Prefer `<Link>` when no programmatic navigation is needed.

## `redirects` in `next.config.ts`

```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  async redirects() {
    return [
      { source: '/about', destination: '/', permanent: true },
      { source: '/blog/:slug', destination: '/news/:slug', permanent: true },
    ]
  },
}
export default nextConfig
```

- Supports path, header, cookie, query matching
- Runs **before** middleware
- Platform limits may apply (e.g., Vercel: 1024 redirects)

## `NextResponse.redirect` in Middleware

```typescript
import { NextResponse, NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const isAuthenticated = false // your auth check
  if (!isAuthenticated) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  return NextResponse.next()
}

export const config = { matcher: '/dashboard/:path*' }
```

Runs **after** `redirects` in config, **before** rendering.

## Redirects at Scale (1000+)

Use middleware + Bloom filter for large redirect maps:

1. Store redirects in DB or JSON key-value map
2. Use Bloom filter in middleware to check existence quickly
3. On match, forward to Route Handler that reads actual redirect data
4. Route Handler returns destination + status code

## Quick Reference

| Scenario | Use |
|----------|-----|
| After Server Action / mutation | `redirect()` or `permanentRedirect()` |
| Client event handler | `useRouter().push()` |
| Known path remapping | `redirects` in `next.config.ts` |
| Conditional (auth, geo, etc.) | `NextResponse.redirect` in middleware |
| 1000+ redirects | Middleware + Bloom filter + Route Handler |
| Permanent URL change | `permanentRedirect()` (308) or `permanent: true` in config |
