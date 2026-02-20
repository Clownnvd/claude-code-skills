---
name: nextjs
description: "Next.js 16 App Router patterns: use cache, proxy.ts, cacheComponents, React 19 hooks, RSC, streaming, PPR, Prisma 7, Better Auth, next-intl"
user_invocable: true
---

# Next.js 16 Skill Index

## Quick Reference

| Category | File | Covers |
|----------|------|--------|
| **Getting Started** | [installation](references/getting-started/installation.md) | create-next-app, manual setup, CLI prompts, TypeScript, linting, aliases |
| **Getting Started** | [project-structure](references/getting-started/project-structure.md) | folders, routing files, metadata files, colocation, organization strategies |
| **Getting Started** | [layouts-and-pages](references/getting-started/layouts-and-pages.md) | pages, layouts, nesting, dynamic segments, searchParams, Link, PageProps/LayoutProps |
| **Getting Started** | [linking-and-navigating](references/getting-started/linking-and-navigating.md) | Link, prefetching, streaming, loading.tsx, useLinkStatus, history API |
| **Getting Started** | [server-and-client-components](references/getting-started/server-and-client-components.md) | RSC vs Client, 'use client', composition, context, server-only, env safety |
| **Getting Started** | [cache-components](references/getting-started/cache-components.md) | PPR, cacheComponents, use cache, cacheLife, Suspense, Activity, migration |
| **Getting Started** | [fetching-data](references/getting-started/fetching-data.md) | fetch, ORM, use() streaming, SWR, deduplication, React.cache, parallel/sequential |
| **Getting Started** | [updating-data](references/getting-started/updating-data.md) | Server Actions, 'use server', forms, revalidate, redirect, refresh, cookies |
| **Getting Started** | [caching-and-revalidating](references/getting-started/caching-and-revalidating.md) | fetch cache, cacheTag, revalidateTag, updateTag, revalidatePath, decision guide |
| **Getting Started** | [error-handling](references/getting-started/error-handling.md) | expected vs uncaught, useActionState, notFound, error.tsx, global-error, reset |
| **Getting Started** | [css](references/getting-started/css.md) | Tailwind setup, CSS Modules, global CSS, external, ordering, dev vs prod |
| **Getting Started** | [images](references/getting-started/images.md) | next/image, local/remote, fill, blur placeholder, remotePatterns, props |
| **Getting Started** | [fonts](references/getting-started/fonts.md) | next/font, Google self-host, local fonts, variable fonts, Tailwind CSS 4 |
| **Getting Started** | [metadata-and-og-images](references/getting-started/metadata-and-og-images.md) | static/dynamic metadata, generateMetadata, file conventions, ImageResponse, OG images |
| **Getting Started** | [route-handlers](references/getting-started/route-handlers.md) | route.ts, HTTP methods, caching, cache components, params, NextRequest/NextResponse |
| **Getting Started** | [proxy](references/getting-started/proxy.md) | proxy.ts (replaces middleware.ts), matcher, redirects, rewrites, headers, auth checks |
| **Getting Started** | [deploying](references/getting-started/deploying.md) | Node.js server, Docker, static export, adapters (Vercel, Cloudflare, etc.) |
| **App Router** | [file-conventions](references/app-router/file-conventions.md) | layout, page, loading, error, not-found, template, route |
| **App Router** | [routing](references/app-router/routing.md) | dynamic routes, route groups, parallel, intercepting, navigation |
| **App Router** | [middleware](references/app-router/middleware.md) | proxy.ts (Next.js 16), middleware.ts (legacy), matcher, auth |
| **Data** | [use-cache](references/data/use-cache.md) | "use cache", cacheLife, cacheTag, updateTag, refresh |
| **Data** | [server-actions](references/data/server-actions.md) | inline/module, revalidation, redirect, security, validation |
| **Data** | [fetching](references/data/fetching.md) | RSC fetching, parallel/sequential, React.cache, Prisma, streaming |
| **Data** | [forms](references/data/forms.md) | useActionState, useFormStatus, useOptimistic, use() |
| **Rendering** | [server-components](references/rendering/server-components.md) | RSC vs Client, composition, 'use client' boundary |
| **Rendering** | [static-dynamic](references/rendering/static-dynamic.md) | SSG, SSR, ISR, cacheComponents migration table |
| **Rendering** | [streaming-ppr](references/rendering/streaming-ppr.md) | Suspense, PPR, loading.tsx, generateStaticParams, Activity |
| **API** | [route-handlers](references/api/route-handlers.md) | GET/POST/PUT/DELETE, params, request/response, CORS, webhooks |
| **API** | [metadata](references/api/metadata.md) | static/dynamic metadata, OG images, robots.txt, sitemap.xml |
| **Optimization** | [images-fonts](references/optimization/images-fonts.md) | next/image, next/font (Google, local, Tailwind CSS 4) |
| **Optimization** | [performance](references/optimization/performance.md) | Turbopack, dynamic imports, tree shaking, bundle analysis |
| **Patterns** | [auth](references/patterns/auth.md) | Better Auth setup, API route, client/server, middleware |
| **Patterns** | [database](references/patterns/database.md) | Prisma 7 config, singleton, queries, transactions, Neon |
| **Patterns** | [i18n](references/patterns/i18n.md) | next-intl setup, URL prefix vs static, translations |

## Next.js 16 Breaking Changes (from 15)

| Change | Next.js 15 | Next.js 16 |
|--------|-----------|-----------|
| Caching | `unstable_cache` | `"use cache"` directive |
| Cache profiles | N/A | `cacheLife('hours')` presets |
| Cache tags | `revalidateTag(tag)` | `cacheTag(tag)` + `updateTag(tag)` |
| Revalidation | `revalidateTag(tag)` | `revalidateTag(tag, cacheLifeProfile)` |
| Fresh read | N/A | `refresh()` for uncached data |
| Middleware | `middleware.ts` (Edge) | `proxy.ts` (Node.js runtime) |
| PPR / dynamicIO | `experimental.ppr`, `experimental.dynamicIO` | `cacheComponents: true` |
| React Compiler | `experimental.reactCompiler` | top-level `reactCompiler: true` |
| Turbopack | opt-in (`--turbopack`) | stable, default for dev + build |
| params/searchParams | sync objects | `Promise` -- must `await` |
| Parallel routes | optional default | explicit `default.tsx` required |
| Node.js | 18.17+ | 20+ required |
| TypeScript | 4.5+ | 5+ required |

## Migration Command

```bash
# Migrate middleware.ts to proxy.ts
npx @next/codemod@canary middleware-to-proxy

# Upgrade to Next.js 16
npx @next/codemod@latest upgrade
```

## next.config.ts (Next.js 16)

```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,    // replaces experimental.ppr + dynamicIO
  reactCompiler: true,      // no longer experimental
  // turbopack is default, no config needed
}

export default nextConfig
```

## Key Conventions

- Server Components are the default -- add `'use client'` only when needed
- Use `"use cache"` at top of file or function for caching
- Use `proxy.ts` for request-level middleware (Node.js runtime)
- Await `params` and `searchParams` in all page/layout components
- Provide `default.tsx` for every parallel route slot
- Use Zod for all input validation in server actions and API routes
- Handle errors with try/catch, never silent returns
