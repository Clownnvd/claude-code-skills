# Proxy

> Source: nextjs.org/docs/app/getting-started/proxy (v16.1.6)

## Overview

Starting with Next.js 16, `middleware.ts` is renamed to `proxy.ts`. Functionality is the same — runs code before a request completes, can modify the response by rewriting, redirecting, modifying headers, or responding directly.

## Convention

Create `proxy.ts` at project root (or `src/`), same level as `app` or `pages`.

- Only **one** `proxy.ts` per project
- Break logic into modules and import into main `proxy.ts`
- Runs in **Node.js runtime** (not Edge, unlike old middleware)

## Basic Example

Export as named `proxy` or default export:

```ts
// proxy.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  return NextResponse.redirect(new URL('/home', request.url))
}

export const config = {
  matcher: '/about/:path*',
}
```

## Matcher

The `config.matcher` filters which paths trigger the proxy:

```ts
export const config = {
  matcher: '/about/:path*',           // single path
}

// Multiple paths
export const config = {
  matcher: ['/about/:path*', '/dashboard/:path*'],
}
```

## Use Cases

| Use Case | Approach |
|----------|----------|
| Redirects (simple) | Prefer `redirects` in `next.config.ts` |
| Redirects (complex/conditional) | `proxy.ts` with `NextResponse.redirect()` |
| Rewrites | `NextResponse.rewrite()` |
| Header modification | `NextResponse.next()` with modified headers |
| A/B testing | Rewrite to different pages based on cookie/header |
| Auth optimistic checks | Permission-based redirects |

## What Proxy Is NOT For

- **Slow data fetching** — proxy should be fast, not fetch heavy data
- **Full session management** — use proper auth (e.g., Better Auth)
- **fetch with caching** — `options.cache`, `options.next.revalidate`, `options.next.tags` have no effect in proxy

## Common Patterns

### Redirect

```ts
export function proxy(request: NextRequest) {
  return NextResponse.redirect(new URL('/login', request.url))
}
```

### Rewrite

```ts
export function proxy(request: NextRequest) {
  return NextResponse.rewrite(new URL('/api/proxy', request.url))
}
```

### Modify Headers

```ts
export function proxy(request: NextRequest) {
  const response = NextResponse.next()
  response.headers.set('x-custom-header', 'value')
  return response
}
```

### Auth Check

```ts
export function proxy(request: NextRequest) {
  const token = request.cookies.get('session')?.value
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  return NextResponse.next()
}
```

## Migration from middleware.ts

```bash
npx @next/codemod@canary middleware-to-proxy
```

| middleware.ts | proxy.ts |
|---------------|----------|
| `export function middleware()` | `export function proxy()` |
| Edge Runtime | Node.js Runtime |
| File: `middleware.ts` | File: `proxy.ts` |
| Same `NextRequest`/`NextResponse` APIs | Same APIs |
| Same `config.matcher` | Same matcher |

## Quick Reference

| Feature | Details |
|---------|---------|
| File | `proxy.ts` at project root or `src/` |
| Export | Named `proxy` or default export |
| Runtime | Node.js (not Edge) |
| Matcher | `config.matcher` — string or array of path patterns |
| APIs | `NextRequest`, `NextResponse` from `next/server` |
| Replaces | `middleware.ts` from Next.js 15 |
| Limit | One file per project |
