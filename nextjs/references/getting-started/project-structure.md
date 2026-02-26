# Next.js Project Structure

> Source: nextjs.org/docs/app/getting-started/project-structure (v16.1.6)

## Top-level Folders

| Folder | Purpose |
|--------|---------|
| `app` | App Router |
| `pages` | Pages Router (legacy) |
| `public` | Static assets served at `/` |
| `src` | Optional source folder (separates code from config) |

## Top-level Files

| File | Purpose |
|------|---------|
| `next.config.js` | Next.js configuration |
| `package.json` | Dependencies and scripts |
| `instrumentation.ts` | OpenTelemetry / instrumentation |
| `proxy.ts` | Next.js 16 request proxy (replaces middleware) |
| `.env` / `.env.local` / `.env.development` / `.env.production` | Environment variables (not tracked in VCS) |
| `eslint.config.mjs` | ESLint configuration |
| `next-env.d.ts` | TypeScript declarations (auto-generated, not tracked) |
| `tsconfig.json` / `jsconfig.json` | TypeScript / JavaScript config |

## Routing Files

| File | Extensions | Purpose |
|------|-----------|---------|
| `layout` | `.js` `.jsx` `.tsx` | Shared layout (wraps children) |
| `page` | `.js` `.jsx` `.tsx` | Public route page |
| `loading` | `.js` `.jsx` `.tsx` | Suspense loading UI |
| `not-found` | `.js` `.jsx` `.tsx` | 404 UI |
| `error` | `.js` `.jsx` `.tsx` | Error boundary |
| `global-error` | `.js` `.jsx` `.tsx` | Global error boundary |
| `route` | `.js` `.ts` | API endpoint |
| `template` | `.js` `.jsx` `.tsx` | Re-rendered layout (no state persist) |
| `default` | `.js` `.jsx` `.tsx` | Parallel route fallback |

## Component Render Hierarchy

`layout` → `template` → `error` (boundary) → `loading` (suspense) → `not-found` (boundary) → `page` or nested `layout`

## Route Conventions

### Nested routes
Folders = URL segments. Route is public only when `page` or `route` file exists.

| Path | URL |
|------|-----|
| `app/page.tsx` | `/` |
| `app/blog/page.tsx` | `/blog` |
| `app/blog/authors/page.tsx` | `/blog/authors` |

### Dynamic routes

| Pattern | URL example |
|---------|-------------|
| `[slug]` | `/blog/my-post` |
| `[...slug]` | `/shop/a/b/c` (catch-all) |
| `[[...slug]]` | `/docs` or `/docs/a/b` (optional catch-all) |

### Route groups & private folders

| Pattern | Effect |
|---------|--------|
| `(group)` | Organizational only — omitted from URL |
| `_folder` | Private — excluded from routing entirely |

### Parallel & intercepting routes

| Pattern | Purpose |
|---------|---------|
| `@slot` | Named parallel slot (rendered by parent layout) |
| `(.)folder` | Intercept same level |
| `(..)folder` | Intercept parent level |
| `(..)(..)folder` | Intercept two levels up |
| `(...)folder` | Intercept from root |

## Metadata File Conventions

### App icons
`favicon.ico`, `icon.{ico,jpg,png,svg}`, `icon.{js,ts,tsx}` (generated), `apple-icon.{jpg,png}`, `apple-icon.{js,ts,tsx}` (generated)

### OG / Twitter images
`opengraph-image.{jpg,png,gif}`, `opengraph-image.{js,ts,tsx}`, `twitter-image.{jpg,png,gif}`, `twitter-image.{js,ts,tsx}`

### SEO
`sitemap.xml` or `sitemap.{js,ts}`, `robots.txt` or `robots.{js,ts}`

## Organization Strategies

### Colocation
Files in `app/` are safe to colocate — only `page` and `route` files are publicly accessible.

### Strategy 1: Outside `app/`
Keep `app/` purely for routing. Shared code in root `src/components`, `src/lib`, etc.

### Strategy 2: Inside `app/` top-level
Shared folders (`components/`, `lib/`) at `app/` root level.

### Strategy 3: Split by feature
Globally shared code at root, feature-specific code colocated in route segments.

### Route group patterns

| Pattern | Example |
|---------|---------|
| Group by section | `(marketing)/`, `(shop)/` — separate layouts per group |
| Opt-in layout | Move routes into `(group)` to share a layout |
| Scoped loading | `(overview)/loading.tsx` applies only to that group |
| Multiple root layouts | Remove top-level `layout.js`, add one per route group (each needs `<html>` + `<body>`) |

### Private folder tips
- Prefix with `_` to exclude from routing: `_components/`, `_lib/`
- For URL segments starting with underscore, use `%5F` encoding: `%5FfolderName`
