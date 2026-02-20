# Caching and Revalidating

> Source: nextjs.org/docs/app/getting-started/caching-and-revalidating (v16.1.6)

## `fetch`

Not cached by default. Routes with `fetch` are still pre-rendered (HTML cached).

```tsx
// Cache individual request
const data = await fetch('https://...', { cache: 'force-cache' })

// Time-based revalidation
const data = await fetch('https://...', { next: { revalidate: 3600 } })

// Tag for on-demand invalidation
const data = await fetch('https://...', { next: { tags: ['user'] } })
```

To guarantee dynamic rendering, use `connection()` from `next/server`.

## `cacheTag`

Tag cached data inside `use cache` scopes — works with DB queries, filesystem, any server-side work.

```tsx
import { cacheTag } from 'next/cache'

export async function getProducts() {
  'use cache'
  cacheTag('products')
  const products = await db.query('SELECT * FROM products')
  return products
}
```

Requires [Cache Components](/docs/app/getting-started/cache-components) (`cacheComponents: true`).

## `revalidateTag`

Revalidate cache entries by tag. Usable in Server Actions + Route Handlers.

```tsx
import { revalidateTag } from 'next/cache'

export async function updateUser(id: string) {
  // mutate data...
  revalidateTag('user', 'max')  // stale-while-revalidate (recommended)
}
```

| Signature | Behavior |
|-----------|----------|
| `revalidateTag(tag, 'max')` | Stale-while-revalidate — serves stale, fetches fresh in background |
| `revalidateTag(tag)` | Legacy — immediately expires (deprecated) |

## `updateTag`

Immediately expire cache — **Server Actions only**. For read-your-own-writes scenarios.

```tsx
import { updateTag } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  'use server'
  const post = await db.post.create({
    data: { title: formData.get('title'), content: formData.get('content') }
  })
  updateTag('posts')
  updateTag(`post-${post.id}`)
  redirect(`/posts/${post.id}`)
}
```

## `updateTag` vs `revalidateTag`

| | `updateTag` | `revalidateTag` |
|--|-------------|-----------------|
| Where | Server Actions only | Server Actions + Route Handlers |
| Timing | Immediate expiry | Stale-while-revalidate (with `'max'`) |
| Use case | Read-your-own-writes | Background refresh, eventual consistency |

## `revalidatePath`

Revalidate an entire route path. Usable in Server Actions + Route Handlers.

```tsx
import { revalidatePath } from 'next/cache'

export async function updateUser(id: string) {
  // mutate data...
  revalidatePath('/profile')
}
```

## `unstable_cache` (Legacy)

Deprecated — use `use cache` + `cacheTag` instead.

```tsx
import { unstable_cache } from 'next/cache'

const getCachedUser = unstable_cache(
  async () => getUserById(userId),
  [userId],                          // cache key
  { tags: ['user'], revalidate: 3600 }  // options
)
```

## Quick Decision Guide

| Scenario | API |
|----------|-----|
| Cache a `fetch` request | `fetch('...', { cache: 'force-cache' })` |
| Time-based revalidation for fetch | `fetch('...', { next: { revalidate: N } })` |
| Cache DB/ORM/non-fetch work | `'use cache'` + `cacheTag(tag)` |
| Invalidate after mutation (immediate) | `updateTag(tag)` in Server Action |
| Invalidate after mutation (background) | `revalidateTag(tag, 'max')` |
| Invalidate entire route | `revalidatePath('/path')` |
| Tag a fetch for on-demand invalidation | `fetch('...', { next: { tags: ['x'] } })` |
