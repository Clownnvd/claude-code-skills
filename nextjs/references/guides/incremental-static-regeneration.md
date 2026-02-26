# Incremental Static Regeneration (ISR)

> Source: https://nextjs.org/docs/app/guides/incremental-static-regeneration (v16.1.6)

ISR updates static content without full rebuilds. Pages are served from cache and regenerated in the background after the revalidation window expires.

## How It Works

1. Pages generated at `next build`
2. Requests served from cache (instant)
3. After `revalidate` seconds, next request still gets cached (stale) page
4. Cache invalidated, new version generated in background
5. Subsequent requests get the fresh page

## Time-Based Revalidation

```tsx
// app/blog/[id]/page.tsx
interface Post { id: string; title: string; content: string }

export const revalidate = 60 // seconds

export async function generateStaticParams() {
  const posts: Post[] = await fetch('https://api.vercel.app/blog').then(r => r.json())
  return posts.map(post => ({ id: String(post.id) }))
}

export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const post: Post = await fetch(`https://api.vercel.app/blog/${id}`).then(r => r.json())
  return <main><h1>{post.title}</h1><p>{post.content}</p></main>
}
```

## On-Demand Revalidation

### By Path

```ts
'use server'
import { revalidatePath } from 'next/cache'

export async function createPost() {
  revalidatePath('/posts') // invalidate entire route
}
```

### By Tag

```tsx
// Fetch with tag
const data = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] },
})
```

```ts
// Invalidate by tag
'use server'
import { revalidateTag } from 'next/cache'

export async function createPost() {
  revalidateTag('posts')
}
```

### With ORM/Database (unstable_cache)

```tsx
import { unstable_cache } from 'next/cache'
import { db, posts } from '@/lib/db'

const getCachedPosts = unstable_cache(
  async () => db.select().from(posts),
  ['posts'],
  { revalidate: 3600, tags: ['posts'] }
)
```

## Route Segment Config

| Option | Type | Description |
|---|---|---|
| `revalidate` | `number \| false` | Seconds before revalidation (`false` = indefinite) |
| `dynamicParams` | `boolean` | Allow params not in `generateStaticParams` |

## Error Handling

On revalidation error, the last successfully generated page continues to be served. Next retry occurs on the next request.

## Debugging

```js
// next.config.js
module.exports = {
  logging: { fetches: { fullUrl: true } },
}
```

```bash
# .env -- log ISR cache hits/misses
NEXT_PRIVATE_DEBUG_CACHE=1
```

## Caveats

- Requires **Node.js runtime** (default)
- Not supported with **Static Export**
- Multiple fetches with different `revalidate` times: lowest wins for the route
- `revalidate: 0` or `no-store` on any fetch opts into dynamic rendering
- Middleware/proxy not executed for on-demand ISR requests
- `revalidatePath` triggers regeneration on *next request*, not immediately

## Platform Support

| Deployment | Supported |
|---|---|
| Node.js server | Yes |
| Docker container | Yes |
| Static export | No |
| Adapters | Platform-specific |

## Quick Reference

| Task | How |
|---|---|
| Time-based ISR | `export const revalidate = 60` in page/layout |
| On-demand by path | `revalidatePath('/route')` |
| On-demand by tag | Tag fetch with `next: { tags: ['x'] }`, then `revalidateTag('x')` |
| Cache DB queries | `unstable_cache(fn, keys, { revalidate, tags })` |
| Debug ISR locally | `NEXT_PRIVATE_DEBUG_CACHE=1` + `next build && next start` |
| Log fetch cache | `logging: { fetches: { fullUrl: true } }` in config |
