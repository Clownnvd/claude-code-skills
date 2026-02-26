# Linking and Navigating

> Source: nextjs.org/docs/app/getting-started/linking-and-navigating (v16.1.6)

## How Navigation Works

1. **Server Rendering** — layouts/pages are RSC by default, rendered on server
2. **Prefetching** — routes preloaded in background before user clicks
3. **Streaming** — server sends parts as ready (via `loading.tsx`)
4. **Client-side transitions** — `<Link>` swaps content without full page reload

## Link Component

```tsx
import Link from 'next/link'

<Link href="/blog">Blog</Link>        // auto-prefetched on viewport/hover
<a href="/contact">Contact</a>         // no prefetching (native anchor)
```

## Prefetching Behavior

| Route type | What's prefetched |
|-----------|-------------------|
| Static | Full route |
| Dynamic (with `loading.tsx`) | Up to loading boundary (partial) |
| Dynamic (no `loading.tsx`) | Skipped |

Disable prefetching:
```tsx
<Link prefetch={false} href="/blog">Blog</Link>
```

Prefetch only on hover (for large lists):
```tsx
'use client'
import Link from 'next/link'
import { useState } from 'react'

function HoverPrefetchLink({ href, children }: { href: string; children: React.ReactNode }) {
  const [active, setActive] = useState(false)
  return (
    <Link href={href} prefetch={active ? null : false} onMouseEnter={() => setActive(true)}>
      {children}
    </Link>
  )
}
```

## Streaming with loading.tsx

Enables immediate navigation + skeleton UI for dynamic routes.

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <LoadingSkeleton />
}
```

Next.js auto-wraps `page.tsx` in `<Suspense>`. Benefits: immediate navigation, interactive layouts, better TTFB/FCP/TTI.

## Optimizing Slow Transitions

### 1. Add `loading.tsx` to dynamic routes
Without it, client waits for full server response — feels unresponsive.

### 2. Use `generateStaticParams` for dynamic segments
Pre-renders at build time instead of dynamic rendering at request time.

```tsx
export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then((res) => res.json())
  return posts.map((post) => ({ slug: post.slug }))
}
```

### 3. `useLinkStatus` for slow networks
Show feedback during pending transitions.

```tsx
'use client'
import { useLinkStatus } from 'next/link'

export default function LoadingIndicator() {
  const { pending } = useLinkStatus()
  return <span aria-hidden className={`link-hint ${pending ? 'is-pending' : ''}`} />
}
```

Debounce with CSS `animation-delay: 100ms` + `opacity: 0` so indicator only shows on slow navigations.

### 4. Reduce bundle size for faster hydration
- Use `@next/bundle-analyzer` to find large deps
- Move logic to server (RSC) where possible

## Native History API

`pushState`/`replaceState` integrate with Next.js Router — sync with `usePathname`/`useSearchParams`.

```tsx
'use client'
import { useSearchParams } from 'next/navigation'

// pushState — adds history entry (back button works)
function updateSorting(sortOrder: string) {
  const params = new URLSearchParams(searchParams.toString())
  params.set('sort', sortOrder)
  window.history.pushState(null, '', `?${params.toString()}`)
}
```

```tsx
'use client'
import { usePathname } from 'next/navigation'

// replaceState — replaces current entry (no back)
function switchLocale(locale: string) {
  const newPath = `/${locale}${pathname}`
  window.history.replaceState(null, '', newPath)
}
```

| Method | Back button | Use case |
|--------|-------------|----------|
| `pushState` | Yes | Sort, filter, pagination |
| `replaceState` | No | Locale switch, theme toggle |
