# Prefetching

> Source: https://nextjs.org/docs/app/guides/prefetching (v16.1.6)

## How It Works

Next.js code-splits by route and prefetches resources before navigation. Only current route code loads initially; other routes load in background. Result: instant-feeling page transitions with no full reload.

## Static vs Dynamic Prefetching

| Aspect | Static Page | Dynamic Page |
|--------|-------------|--------------|
| Prefetched | Yes, full route | No, unless `loading.js` exists |
| Client Cache TTL | 5 min (default) | Off, unless `staleTimes` configured |
| Server roundtrip on click | No | Yes, streamed after shell |

## Prefetch Patterns

### Automatic Prefetch (default)

```typescript
import Link from 'next/link'

export default function NavLink() {
  return <Link href="/about">About</Link>
}
```

| Context | Prefetched Payload | Client Cache TTL |
|---------|-------------------|------------------|
| No `loading.js` | Entire page | Until app reload |
| With `loading.js` | Layout to first loading boundary | 30s (configurable via `staleTimes`) |

Only runs in production. Disable with `prefetch={false}`.

### Manual Prefetch

```typescript
'use client'
import { useRouter } from 'next/navigation'

export function PricingCard() {
  const router = useRouter()

  return (
    <div onMouseEnter={() => router.prefetch('/pricing')}>
      <a href="/pricing">View Pricing</a>
    </div>
  )
}
```

### Hover-Triggered Prefetch

```typescript
'use client'
import Link from 'next/link'
import { useState } from 'react'

export function HoverPrefetchLink({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  const [active, setActive] = useState(false)

  return (
    <Link
      href={href}
      prefetch={active ? null : false}
      onMouseEnter={() => setActive(true)}
    >
      {children}
    </Link>
  )
}
```

`prefetch={null}` restores default (static) prefetching once user shows intent.

### Extending Link with onInvalidate

Use `router.prefetch(href, { onInvalidate: poll })` in a `useEffect` to re-prefetch when cache goes stale. Use `<a>` with `onClick` calling `e.preventDefault()` + `router.push(href)` for navigation.

### Disabled Prefetch

```typescript
<Link prefetch={false} href={`/blog/${post.id}`}>{post.title}</Link>
```

## Prefetch Scheduling (internal priority)

1. Links in viewport
2. Links showing user intent (hover/touch)
3. Newer links replace older ones
4. Links scrolled off-screen are discarded

## Partial Prerendering (PPR)

When enabled: static shell prefetched and streamed immediately; dynamic data streams when ready. `revalidateTag`/`revalidatePath` silently refresh prefetches.

## Troubleshooting: Side Effects During Prefetch

Side effects (e.g., `trackPageView()`) in layouts/pages fire during prefetch. Fix: move to `useEffect` in a Client Component so they only run on actual visit.

## Quick Reference

| Need | Solution |
|------|----------|
| Default prefetch | `<Link href="...">` (automatic) |
| Manual prefetch | `router.prefetch('/path')` |
| Hover-only prefetch | `prefetch={active ? null : false}` + `onMouseEnter` |
| Disable prefetch | `<Link prefetch={false}>` |
| Re-prefetch on stale | `router.prefetch(href, { onInvalidate: callback })` |
| Avoid side effects | Use `useEffect` for analytics, not top-level calls |
| Configure cache TTL | `staleTimes` in `next.config.ts` |
