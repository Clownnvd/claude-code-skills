# Backend for Frontend

> Source: https://nextjs.org/docs/app/guides/backend-for-frontend (v16.1.6)

## Overview

Next.js supports the BFF pattern: public HTTP endpoints that handle requests and return any content type. Not a full backend replacement -- serves as an API layer that is publicly reachable and can return any content type.

## Route Handlers

Create with `route.ts` convention. Supports standard HTTP methods.

```typescript
// app/api/route.ts
export function GET(request: Request) {}

// With error handling
export async function POST(request: Request) {
  try {
    await submit(request)
    return new Response(null, { status: 204 })
  } catch (reason) {
    const message = reason instanceof Error ? reason.message : 'Unexpected error'
    return new Response(message, { status: 500 })
  }
}
```

## Content Types

| File Convention             | Purpose                 |
|-----------------------------|-------------------------|
| `sitemap.xml`               | Sitemap                 |
| `opengraph-image.jpg`       | OG image                |
| `favicon.ico`               | Favicon                 |
| `manifest.json`             | PWA manifest            |
| `robots.txt`                | Robots                  |
| Custom (`app/rss.xml/route.ts`) | Any content type   |

## Request Payloads

```typescript
// JSON body
export async function POST(request: Request) {
  const res = await request.json()
  return Response.json({ res })
}

// FormData body
export async function POST(request: Request) {
  const formData = await request.formData()
  const email = formData.get('email')
  // validate, process, respond
}
```

**Note**: Request body can only be read once. Use `request.clone()` if needed again.

## NextRequest & NextResponse

| Feature              | `NextRequest`                     | `NextResponse`                       |
|----------------------|-----------------------------------|--------------------------------------|
| Extended from        | Web `Request`                     | Web `Response`                       |
| Key additions        | `nextUrl` (parsed URL)            | `next()`, `json()`, `redirect()`, `rewrite()` |
| Cookie access        | `request.cookies`                 | `response.cookies`                   |

```typescript
import { type NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const nextUrl = request.nextUrl
  if (nextUrl.searchParams.get('redirect'))
    return NextResponse.redirect(new URL('/', request.url))
  return NextResponse.json({ pathname: nextUrl.pathname })
}
```

## Webhooks & Callbacks

```typescript
// app/webhook/route.ts -- revalidation webhook
export async function GET(request: NextRequest) {
  const token = request.nextUrl.searchParams.get('token')
  if (token !== process.env.REVALIDATE_SECRET_TOKEN)
    return NextResponse.json({ success: false }, { status: 401 })
  const tag = request.nextUrl.searchParams.get('tag')
  if (!tag) return NextResponse.json({ success: false }, { status: 400 })
  revalidateTag(tag)
  return NextResponse.json({ success: true })
}
```

## Proxy (one per project)

```typescript
// proxy.ts
import { isAuthenticated } from '@lib/auth'

export const config = { matcher: '/api/:function*' }

export function proxy(request: Request) {
  if (!isAuthenticated(request))
    return Response.json({ success: false, message: 'authentication failed' }, { status: 401 })
}
```

## Security Checklist

| Concern            | Guidance                                               |
|--------------------|--------------------------------------------------------|
| Error messages     | Never expose sensitive info to client                  |
| Input validation   | Always validate before passing to other systems        |
| Headers            | Don't pass request headers directly to response        |
| Rate limiting      | Implement in code + host-level                         |
| Payload size       | Validate content type and size                         |
| Credentials        | Rotate regularly; verify before granting access        |

## Caveats

| Scenario                  | Recommendation                                       |
|---------------------------|------------------------------------------------------|
| Server Components         | Fetch data directly, NOT via Route Handlers          |
| Server Actions            | For mutations only; queued sequentially               |
| `export` mode             | Only `GET` with `dynamic: 'force-static'`            |
| Lambda deployments        | No shared state; no filesystem writes; timeout limits |

## Quick Reference

| Pattern                | Implementation                                        |
|------------------------|-------------------------------------------------------|
| Create API endpoint    | `app/api/route.ts` with exported HTTP methods         |
| Custom content type    | `app/rss.xml/route.ts` with `Response` + headers      |
| Proxy requests         | Catch-all `app/api/[...slug]/route.ts`                |
| Auth guard             | `proxy.ts` with `config.matcher`                      |
| Webhook receiver       | Route Handler verifying secret token                  |
| Library integration    | Factory pattern: `export const GET = createHandler()` |
