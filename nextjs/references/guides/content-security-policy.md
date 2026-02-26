# Content Security Policy

> Source: https://nextjs.org/docs/app/guides/content-security-policy (v16.1.6)

## Overview

CSP guards against XSS, clickjacking, and code injection. Specify allowed origins for scripts, styles, images, fonts, frames, etc.

## Nonce-based CSP (Dynamic Rendering)

A nonce is a unique random string per request. Pages using nonces **must be dynamically rendered**.

### Proxy Setup

```typescript
// proxy.ts
import { NextRequest, NextResponse } from 'next/server'

export function proxy(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64')
  const isDev = process.env.NODE_ENV === 'development'
  const cspHeader = `
    default-src 'self';
    script-src 'self' 'nonce-${nonce}' 'strict-dynamic'${isDev ? " 'unsafe-eval'" : ''};
    style-src 'self' 'nonce-${nonce}';
    img-src 'self' blob: data:;
    font-src 'self';
    object-src 'none';
    base-uri 'self';
    form-action 'self';
    frame-ancestors 'none';
    upgrade-insecure-requests;
  `.replace(/\s{2,}/g, ' ').trim()

  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-nonce', nonce)
  requestHeaders.set('Content-Security-Policy', cspHeader)

  const response = NextResponse.next({ request: { headers: requestHeaders } })
  response.headers.set('Content-Security-Policy', cspHeader)
  return response
}

export const config = {
  matcher: [{
    source: '/((?!api|_next/static|_next/image|favicon.ico).*)',
    missing: [
      { type: 'header', key: 'next-router-prefetch' },
      { type: 'header', key: 'purpose', value: 'prefetch' },
    ],
  }],
}
```

### How Nonces Work

1. Proxy generates nonce, sets `Content-Security-Policy` + `x-nonce` headers
2. Next.js extracts nonce from CSP header during rendering
3. Nonce auto-applied to: framework scripts, page bundles, inline styles/scripts, `<Script>` components

### Force Dynamic Rendering

```typescript
import { connection } from 'next/server'
export default async function Page() {
  await connection()
  // page content
}
```

### Reading the Nonce

```typescript
import { headers } from 'next/headers'
import Script from 'next/script'

export default async function Page() {
  const nonce = (await headers()).get('x-nonce')
  return <Script src="https://www.googletagmanager.com/gtag/js" strategy="afterInteractive" nonce={nonce} />
}
```

## Without Nonces (Static-compatible)

```javascript
// next.config.js
const isDev = process.env.NODE_ENV === 'development'
const cspHeader = `
  default-src 'self';
  script-src 'self' 'unsafe-inline'${isDev ? " 'unsafe-eval'" : ''};
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data:;
  font-src 'self'; object-src 'none'; base-uri 'self';
  form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests;
`
module.exports = {
  async headers() {
    return [{ source: '/(.*)', headers: [{ key: 'Content-Security-Policy', value: cspHeader.replace(/\n/g, '') }] }]
  },
}
```

## SRI (Experimental, Webpack only)

Hash-based CSP alternative -- allows static generation:

```javascript
// next.config.js
module.exports = {
  experimental: { sri: { algorithm: 'sha256' } },  // or sha384, sha512
}
```

| Feature       | Nonces                    | SRI (Experimental)          |
|---------------|---------------------------|-----------------------------|
| Rendering     | Dynamic only              | Static compatible           |
| CDN caching   | Not by default            | Yes                         |
| Performance   | SSR per request           | Build-time hashes           |
| Bundler       | Webpack + Turbopack       | Webpack only (App Router)   |

## Common CSP Directives

| Directive             | Recommended Value                        |
|-----------------------|------------------------------------------|
| `default-src`         | `'self'`                                 |
| `script-src`          | `'self' 'nonce-X' 'strict-dynamic'`     |
| `style-src`           | `'self' 'nonce-X'`                       |
| `img-src`             | `'self' blob: data:`                     |
| `font-src`            | `'self'`                                 |
| `object-src`          | `'none'`                                 |
| `frame-ancestors`     | `'none'`                                 |

## Quick Reference

| Task                         | Solution                                           |
|------------------------------|----------------------------------------------------|
| Add nonce-based CSP          | Generate in `proxy.ts`, set headers                |
| Read nonce in component      | `(await headers()).get('x-nonce')`                 |
| Force dynamic rendering      | `await connection()` from `next/server`            |
| Static CSP (no nonce)        | `headers()` in `next.config.js`                    |
| Hash-based CSP               | `experimental.sri` in config (webpack only)        |
| Third-party scripts          | Add domains to CSP + pass `nonce` prop             |
| Dev mode                     | Add `'unsafe-eval'` to `script-src`                |
