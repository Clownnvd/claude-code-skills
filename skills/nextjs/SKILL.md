---
name: nextjs
description: "Next.js 16 App Router patterns: use cache, proxy.ts, cacheComponents, React 19 hooks, RSC, streaming, PPR, Prisma 7, Better Auth, next-intl"
license: Complete terms in LICENSE.txt
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
| **Guide** | [analytics](references/guides/analytics.md) | useReportWebVitals, Web Vitals metrics, Google Analytics |
| **Guide** | [authentication](references/guides/authentication.md) | sign-up, sessions (JWT/DB), DAL pattern, auth checks |
| **Guide** | [backend-for-frontend](references/guides/backend-for-frontend.md) | Route Handlers as API, webhooks, proxy, security |
| **Guide** | [caching](references/guides/caching.md) | 4 mechanisms, static/dynamic, Data Cache, Router Cache |
| **Guide** | [ci-build-caching](references/guides/ci-build-caching.md) | .next/cache for 11 CI providers |
| **Guide** | [content-security-policy](references/guides/content-security-policy.md) | nonce-based CSP, proxy setup, SRI |
| **Guide** | [css-in-js](references/guides/css-in-js.md) | styled-jsx, styled-components, registry pattern |
| **Guide** | [custom-server](references/guides/custom-server.md) | next() setup, caveats, static optimization |
| **Guide** | [data-security](references/guides/data-security.md) | DAL, server-only, taintUniqueValue, Server Actions |
| **Guide** | [debugging](references/guides/debugging.md) | VS Code launch.json, browser DevTools, WebStorm |
| **Guide** | [draft-mode](references/guides/draft-mode.md) | route handler setup, CMS integration, isEnabled |
| **Guide** | [environment-variables](references/guides/environment-variables.md) | .env load order, NEXT_PUBLIC_, runtime vs build-time |
| **Guide** | [forms](references/guides/forms.md) | Server Actions, Zod, useActionState, useOptimistic |
| **Guide** | [incremental-static-regeneration](references/guides/incremental-static-regeneration.md) | time-based, on-demand, revalidatePath/Tag |
| **Guide** | [instrumentation](references/guides/instrumentation.md) | instrumentation.ts, register(), onRequestError |
| **Guide** | [internationalization](references/guides/internationalization.md) | locale routing, dictionaries, server/client i18n |
| **Guide** | [json-ld](references/guides/json-ld.md) | structured data, schema.org, script injection |
| **Guide** | [lazy-loading](references/guides/lazy-loading.md) | next/dynamic, React.lazy, named exports, SSR skip |
| **Guide** | [local-development](references/guides/local-development.md) | HTTPS, Turbopack, Docker, memory, absolute imports |
| **Guide** | [mcp](references/guides/mcp.md) | Next.js MCP server, IDE integration, tools |
| **Guide** | [mdx](references/guides/mdx.md) | @next/mdx, remote MDX, custom components, plugins |
| **Guide** | [memory-usage](references/guides/memory-usage.md) | webpack workers, heap profiling, cache/sourcemaps |
| **Guide** | [migrating](references/guides/migrating.md) | Pages→App Router, CRA→Next, Vite→Next |
| **Guide** | [multi-tenant](references/guides/multi-tenant.md) | subdomain, path-based, custom domains |
| **Guide** | [multi-zones](references/guides/multi-zones.md) | micro-frontends, assetPrefix, rewrites, cross-zone |
| **Guide** | [open-telemetry](references/guides/open-telemetry.md) | @vercel/otel, NodeSDK, spans, custom attributes |
| **Guide** | [package-bundling](references/guides/package-bundling.md) | bundle analyzer, optimizePackageImports, externals |
| **Guide** | [prefetching](references/guides/prefetching.md) | auto, manual, hover, extended, PPR integration |
| **Guide** | [production-checklist](references/guides/production-checklist.md) | optimizations, best practices, pre-launch checks |
| **Guide** | [progressive-web-apps](references/guides/progressive-web-apps.md) | manifest, push notifications, service worker |
| **Guide** | [redirecting](references/guides/redirecting.md) | redirect(), permanentRedirect(), config, proxy |
| **Guide** | [sass](references/guides/sass.md) | .scss/.sass, sassOptions, sass-embedded, variables |
| **Guide** | [scripts](references/guides/scripts.md) | next/script, loading strategies, event handlers |
| **Guide** | [self-hosting](references/guides/self-hosting.md) | reverse proxy, image optimization, caching, CDN |
| **Guide** | [single-page-applications](references/guides/single-page-applications.md) | SPA patterns, use(), SWR, shallow routing, static export |
| **Guide** | [static-exports](references/guides/static-exports.md) | output: 'export', supported/unsupported features |
| **Guide** | [tailwind-v3-css](references/guides/tailwind-v3-css.md) | Tailwind v3 setup, config, directives |
| **Guide** | [testing](references/guides/testing.md) | Vitest, Jest, Playwright, Cypress, test types |
| **Guide** | [cypress](references/guides/cypress.md) | E2E + component testing, cypress.config.ts, CI scripts |
| **Guide** | [jest](references/guides/jest.md) | next/jest, jest-dom, snapshot testing, module aliases |
| **Guide** | [playwright](references/guides/playwright.md) | E2E, multi-browser, webServer, playwright.config.ts |
| **Guide** | [vitest](references/guides/vitest.md) | unit testing, @vitejs/plugin-react, vite-tsconfig-paths |
| **Guide** | [third-party-libraries](references/guides/third-party-libraries.md) | @next/third-parties, GTM, GA, Maps, YouTube |
| **Guide** | [upgrading](references/guides/upgrading.md) | v14→v15→v16, codemods, upgrade workflow |
| **Guide** | [videos](references/guides/videos.md) | video/iframe embed, Suspense, Vercel Blob, Mux |

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
