# Production Checklist

> Source: https://nextjs.org/docs/app/guides/production-checklist (v16.1.6)

## Automatic Optimizations (zero config)

| Feature | Description |
|---------|-------------|
| Server Components | Default; no client JS impact |
| Code-splitting | Automatic per route segment |
| Prefetching | `<Link>` prefetches routes in viewport |
| Static Rendering | Build-time render + cache by default |
| Caching | Data, rendered results, static assets cached |

## During Development

### Routing & Rendering

| Practice | Details |
|----------|---------|
| Use Layouts | Share UI, enable partial rendering |
| Use `<Link>` | Client-side nav + prefetching |
| Error Handling | Custom `error.tsx`, `not-found.tsx` |
| `"use client"` placement | Push boundaries down the tree |
| Dynamic APIs | `cookies`, `searchParams` opt into dynamic rendering; wrap in `<Suspense>` |

### Data Fetching & Caching

| Practice | Details |
|----------|---------|
| Fetch in Server Components | Leverage server-side data fetching |
| Route Handlers | For client-side backend access only (never call from Server Components) |
| Streaming / `<Suspense>` | Progressive UI via `loading.tsx` |
| Parallel fetching | Avoid waterfalls; preload where needed |
| Cache verification | Use `unstable_cache` for non-fetch requests |

### UI & Accessibility

| Practice | Details |
|----------|---------|
| Forms | Server Actions for submission + validation |
| `app/global-error.tsx` | Catch-all error fallback |
| `app/global-not-found.tsx` | 404 for unmatched routes |
| Font Module (`next/font`) | Self-hosted, no layout shift |
| `<Image>` component | Auto-optimize, WebP, no layout shift |
| `<Script>` component | Deferred, non-blocking third-party scripts |
| ESLint `jsx-a11y` | Catch accessibility issues early |

### Security

| Practice | Details |
|----------|---------|
| Tainting | Prevent sensitive data from reaching client |
| Server Actions auth | Verify user authorization |
| Env variables | `.env.*` in `.gitignore`; only `NEXT_PUBLIC_` exposed |
| CSP headers | Protect against XSS, clickjacking |

### Metadata & SEO

| Practice | Details |
|----------|---------|
| Metadata API | Titles, descriptions via `generateMetadata` |
| OG images | `opengraph-image.tsx` for social sharing |
| Sitemaps & Robots | `sitemap.ts`, `robots.ts` |

### Type Safety

Use TypeScript + Next.js TS plugin for compile-time checks.

## Before Production

```bash
next build    # catch build errors
next start    # test production performance
```

| Tool | Purpose |
|------|---------|
| Lighthouse (incognito) | Simulated perf audit |
| `useReportWebVitals` | Real Core Web Vitals data |
| `@next/bundle-analyzer` | Identify large modules |

## Quick Reference

| Category | Key Actions |
|----------|-------------|
| Performance | Layouts, `<Link>`, `<Image>`, `<Script>`, code-split, prefetch |
| Data | Server Components fetch, parallel requests, caching |
| Security | Tainting, CSP, env vars, Server Action auth |
| SEO | Metadata API, OG images, sitemap, robots |
| Pre-launch | `next build` + `next start` + Lighthouse + bundle analysis |
