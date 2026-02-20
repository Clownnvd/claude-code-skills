# Route Handlers

> Source: nextjs.org/docs/app/getting-started/route-handlers (v16.1.6)

## Convention

Define in `route.ts` inside `app/`. Uses Web Request/Response APIs.

```ts
// app/api/route.ts
export async function GET(request: Request) {}
```

- Can be nested anywhere in `app/`, like `page.tsx` and `layout.tsx`
- **Cannot** coexist with `page.tsx` at the same route segment
- Equivalent of old `pages/api/` API Routes

## Supported HTTP Methods

`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`

Unsupported methods return `405 Method Not Allowed`.

## Extended APIs

`NextRequest` and `NextResponse` from `next/server` extend native Request/Response with helpers.

## Route Resolution

| Page | Route | Result |
|------|-------|--------|
| `app/page.tsx` | `app/route.ts` | Conflict |
| `app/page.tsx` | `app/api/route.ts` | Valid |
| `app/[user]/page.tsx` | `app/api/route.ts` | Valid |

Each `route.ts` takes over all HTTP verbs for that route. No layouts or client-side navigation.

## Route Context & Params

Use `RouteContext` helper for typed params (auto-generated during `next dev`/`next build`):

```ts
// app/users/[id]/route.ts
import type { NextRequest } from 'next/server'

export async function GET(_req: NextRequest, ctx: RouteContext<'/users/[id]'>) {
  const { id } = await ctx.params
  return Response.json({ id })
}
```

## Caching

**Not cached by default.** Opt-in for GET only:

```ts
// app/items/route.ts
export const dynamic = 'force-static'

export async function GET() {
  const res = await fetch('https://data.mongodb-api.com/...', {
    headers: { 'Content-Type': 'application/json', 'API-Key': process.env.DATA_API_KEY! },
  })
  const data = await res.json()
  return Response.json({ data })
}
```

Other HTTP methods are **never** cached, even alongside a cached GET.

## With Cache Components

When `cacheComponents: true`, GET handlers follow same model as UI routes:

| Behavior | When |
|----------|------|
| **Prerendered** (static) | No dynamic/runtime data access |
| **Request-time** (dynamic) | Uses `Math.random()`, `headers()`, `cookies()`, `connection()`, request properties, DB queries |
| **Cached dynamic** | Uses `use cache` in a helper function |

### Static (prerendered at build)

```ts
export async function GET() {
  return Response.json({ projectName: 'Next.js' })
}
```

### Dynamic (request-time)

```ts
import { headers } from 'next/headers'

export async function GET() {
  const headersList = await headers()
  return Response.json({ userAgent: headersList.get('user-agent') })
}
```

### Cached with `use cache`

`use cache` **cannot** be used directly in Route Handler body — extract to helper:

```ts
import { cacheLife } from 'next/cache'

export async function GET() {
  const products = await getProducts()
  return Response.json(products)
}

async function getProducts() {
  'use cache'
  cacheLife('hours')
  return await db.query('SELECT * FROM products')
}
```

## Prerendering Stops When

GET handler accesses: network requests, DB queries, async file system ops, `req.url`/`request.headers`/`request.cookies`/`request.body`, `cookies()`, `headers()`, `connection()`, or non-deterministic operations.

## Special Route Handlers

`sitemap.ts`, `opengraph-image.tsx`, `icon.tsx`, and other metadata files are **static by default** unless they use Dynamic APIs or dynamic config.

## Quick Reference

| Feature | Details |
|---------|---------|
| File | `route.ts` in any `app/` directory |
| Methods | GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS |
| Caching | Not cached by default; `force-static` for GET |
| Cache Components | Static/dynamic/cached same as UI routes |
| `use cache` | Must be in helper function, not handler body |
| Params | `await ctx.params` — Promises in Next.js 16 |
| Conflict | Cannot have `route.ts` + `page.tsx` at same segment |
| No layouts | Route handlers don't participate in layout hierarchy |
