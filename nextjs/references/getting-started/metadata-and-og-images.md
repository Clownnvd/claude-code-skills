# Metadata and OG Images

> Source: nextjs.org/docs/app/getting-started/metadata-and-og-images (v16.1.6)

## Metadata APIs

Three ways to define metadata:

| Method | Use case |
|--------|----------|
| `metadata` object | Static metadata (title, description) |
| `generateMetadata` function | Dynamic metadata from data (e.g., blog post title) |
| File conventions | favicon.ico, opengraph-image, robots.txt, sitemap.xml |

Only supported in **Server Components**. Next.js auto-generates `<head>` tags.

## Default Fields (always added)

```html
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

## Static Metadata

Export a `Metadata` object from `layout.tsx` or `page.tsx`:

```tsx
// app/blog/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My Blog',
  description: '...',
}

export default function Layout() {}
```

## Dynamic Metadata (`generateMetadata`)

Fetch metadata that depends on data. `params` and `searchParams` are Promises (must await).

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata, ResolvingMetadata } from 'next'

type Props = {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}

export async function generateMetadata(
  { params, searchParams }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const slug = (await params).slug
  const post = await fetch(`https://api.vercel.app/blog/${slug}`).then((res) =>
    res.json()
  )
  return { title: post.title, description: post.description }
}
```

### Streaming Metadata

- Dynamic pages: metadata streams separately, doesn't block UI rendering
- **Disabled for bots** (Twitterbot, Slackbot, Bingbot) — detected via User Agent
- Customize with `htmlLimitedBots` in next.config
- Static pages: metadata resolved at build time (no streaming)

### Memoizing Data Requests

Use `React.cache` to deduplicate fetches between `generateMetadata` and page:

```ts
// app/lib/data.ts — wrap with cache(), use in both generateMetadata and Page
import { cache } from 'react'
export const getPost = cache(async (slug: string) => {
  return db.query.posts.findFirst({ where: eq(posts.slug, slug) })
})
```

## File-based Metadata

| File | Location | Purpose |
|------|----------|---------|
| `favicon.ico` | `app/` root | Browser tab icon, bookmarks |
| `apple-icon.jpg` | `app/` root | Apple touch icon |
| `icon.jpg` | `app/` root | General icon |
| `opengraph-image.jpg` | Any route folder | Social media preview image |
| `twitter-image.jpg` | Any route folder | Twitter card image |
| `robots.txt` | `app/` root | Crawler rules |
| `sitemap.xml` | `app/` root | Search engine sitemap |

- Place `favicon.ico` in `app/` root
- OG images can be placed at any route level — more specific takes precedence
- Supported formats: `jpeg`, `png`, `gif`
- All can be generated programmatically

## Generated OG Images (`ImageResponse`)

Create dynamic OG images with JSX and CSS using `opengraph-image.tsx`:

```tsx
// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og'
import { getPost } from '@/app/lib/data'

export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function Image({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug)
  return new ImageResponse(
    (<div style={{ fontSize: 128, background: 'white', width: '100%', height: '100%',
        display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      {post.title}
    </div>)
  )
}
```

`ImageResponse` supports flexbox, absolute positioning, custom fonts, text wrapping, nested images. No `display: grid`. Uses `@vercel/og` + `satori` + `resvg`.

## Quick Reference

| Export/File | Type | Notes |
|-------------|------|-------|
| `metadata` | `Metadata` object | Static, from layout/page |
| `generateMetadata` | Async function | Dynamic, receives `params`/`searchParams` (Promises) |
| `generateViewport` | Async function | Viewport-specific metadata |
| `ImageResponse` | Constructor | From `next/og`, JSX → PNG |
| `opengraph-image.tsx` | File convention | Dynamic OG per route |
| `opengraph-image.jpg` | File convention | Static OG per route |
| `favicon.ico` | File convention | App root only |
| `robots.txt` | File convention | App root only |
| `sitemap.xml` | File convention | App root only |
