# Multi-Zones (Micro-Frontends)

> Source: https://nextjs.org/docs/app/guides/multi-zones (v16.1.6)

## Overview

Multi-Zones split a large app on one domain into separate Next.js applications, each serving specific paths. Benefits: independent deploys, smaller builds, framework flexibility per zone.

- **Same zone navigation** = soft navigation (no reload)
- **Cross-zone navigation** = hard navigation (full page load)

## Architecture Example

| Zone | Paths | App |
|------|-------|-----|
| Default | `/*` (catch-all) | Main website |
| Blog | `/blog/*` | Blog app |
| Dashboard | `/dashboard/*` | Dashboard app |

## Zone Configuration

Each non-default zone needs `assetPrefix` to avoid static file conflicts:

```typescript
// next.config.ts (blog zone)
import type { NextConfig } from 'next'

const config: NextConfig = {
  assetPrefix: '/blog-static',
}
export default config
```

Assets are served at `/blog-static/_next/...`. The default zone (catch-all) needs no `assetPrefix`.

> In Next.js 15+, no additional rewrite for static assets is needed.

## Routing Requests to Zones

Use `rewrites` in the main app to proxy requests to other zones:

```typescript
// next.config.ts (main app)
import type { NextConfig } from 'next'

const config: NextConfig = {
  async rewrites() {
    return [
      { source: '/blog', destination: `${process.env.BLOG_DOMAIN}/blog` },
      { source: '/blog/:path+', destination: `${process.env.BLOG_DOMAIN}/blog/:path+` },
      { source: '/blog-static/:path+', destination: `${process.env.BLOG_DOMAIN}/blog-static/:path+` },
    ]
  },
}
export default config
```

### Dynamic Routing with Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server'

export async function middleware(request: Request) {
  const { pathname, search } = new URL(request.url)
  if (pathname === '/your-path' && myFeatureFlag.isEnabled()) {
    return NextResponse.rewrite(`${rewriteDomain}${pathname}${search}`)
  }
}
```

## Linking Between Zones

Use `<a>` tags (not `<Link>`) for cross-zone links. `<Link>` attempts soft navigation and prefetch, which fails across zones.

## Server Actions

Explicitly allow the user-facing origin:

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  experimental: {
    serverActions: {
      allowedOrigins: ['your-production-domain.com'],
    },
  },
}
export default config
```

## Code Sharing

| Approach | Best For |
|----------|----------|
| Monorepo | Teams sharing code frequently |
| NPM packages | Independent repos, versioned sharing |
| Feature flags | Coordinating releases across zones |

## Quick Reference

| Need | Solution |
|------|----------|
| Avoid asset conflicts | `assetPrefix` on non-default zones |
| Route to zones | `rewrites` in main app's `next.config.ts` |
| Cross-zone links | Use `<a>` tag, not `<Link>` |
| Server Actions | Add `serverActions.allowedOrigins` |
| Share code | Monorepo or NPM packages |
| Feature flags | Coordinate cross-zone releases |
| Example | [with-zones](https://github.com/vercel/next.js/tree/canary/examples/with-zones) |
