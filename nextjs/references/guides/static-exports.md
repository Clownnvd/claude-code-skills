# Static Exports

> Source: https://nextjs.org/docs/app/guides/static-exports (v16.1.6)

Next.js can generate a static site / SPA. Running `next build` produces an HTML file per route in an `out` folder, deployable on any static host.

## Configuration

```ts
// next.config.ts
const nextConfig: import('next').NextConfig = {
  output: 'export',
  // trailingSlash: true,        // /me -> /me/ and /me.html -> /me/index.html
  // skipTrailingSlashRedirect: true,
  // distDir: 'dist',            // change output dir from `out`
}
export default nextConfig
```

## Supported Features

| Feature | Notes |
|---|---|
| Server Components | Run at build time, rendered to static HTML |
| Client Components | Pre-rendered to HTML; use `useEffect` for browser APIs (`window`, `localStorage`) |
| Client data fetching | Use SWR or similar in Client Components |
| Image Optimization | Requires custom `loader` (`images: { loader: 'custom', loaderFile: './my-loader.ts' }`) |
| Route Handlers | Only `GET` verb; renders static file (e.g., `app/data.json/route.ts` -> `data.json`) |
| `next/link` | Client-side navigation works like a traditional SPA |

### Custom Image Loader Example

```ts
// my-loader.ts
export default function cloudinaryLoader({
  src, width, quality,
}: { src: string; width: number; quality?: number }) {
  const params = ['f_auto', 'c_limit', `w_${width}`, `q_${quality || 'auto'}`]
  return `https://res.cloudinary.com/demo/image/upload/${params.join(',')}${src}`
}
```

## Unsupported Features

These require a Node.js server and **cannot** be used with static export:

| Feature | Reason |
|---|---|
| Dynamic Routes with `dynamicParams: true` | Needs runtime |
| Dynamic Routes without `generateStaticParams()` | Unknown paths at build |
| Route Handlers relying on `Request` | Needs runtime |
| `cookies()` / `headers()` | Server-only |
| Rewrites / Redirects / Headers (config) | Needs server |
| Incremental Static Regeneration | Needs server |
| Image Optimization (default loader) | Needs server |
| Draft Mode | Needs server |
| Server Actions | Needs server |
| Intercepting Routes | Needs server |
| Proxy | Needs server |

Setting `export const dynamic = 'error'` in root layout enforces the same restrictions.

## Deployment (Nginx Example)

```nginx
server {
  listen 80;
  server_name acme.com;
  root /var/www/out;

  location / {
    try_files $uri $uri.html $uri/ =404;
  }
  location /blog/ {
    rewrite ^/blog/(.*)$ /blog/$1.html break;
  }
  error_page 404 /404.html;
  location = /404.html { internal; }
}
```

Output structure: `/out/index.html`, `/out/404.html`, `/out/blog/post-1.html`, etc.

## Quick Reference

| Task | How |
|---|---|
| Enable static export | `output: 'export'` in `next.config.ts` |
| Custom output dir | `distDir: 'dist'` |
| Trailing slashes | `trailingSlash: true` |
| Image optimization | Custom loader via `images.loaderFile` |
| Static Route Handler | Export `GET` function only |
| Browser APIs | Use `useEffect` in Client Components |
| Build command | `next build` (outputs to `out/`) |
