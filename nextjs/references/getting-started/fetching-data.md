# Fetching Data

> Source: nextjs.org/docs/app/getting-started/fetching-data (v16.1.6)

## Server Components

Async Server Components can fetch directly — `fetch`, ORM/DB, filesystem.

```tsx
// fetch API
export default async function Page() {
  const data = await fetch('https://api.vercel.app/blog')
  const posts = await data.json()
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

```tsx
// ORM / database
import { db, posts } from '@/lib/db'
export default async function Page() {
  const allPosts = await db.select().from(posts)
  return <ul>{allPosts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

`fetch` responses not cached by default. Use `{ cache: 'force-cache' }` for Data Cache, or `{ cache: 'no-store' }` to ensure dynamic rendering.

## Client Components

### `use()` API — stream promise from server

```tsx
// Server Component — don't await
import Posts from '@/app/ui/posts'
import { Suspense } from 'react'

export default function Page() {
  const posts = getPosts()  // no await — pass promise
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Posts posts={posts} />
    </Suspense>
  )
}

// Client Component — resolve with use()
'use client'
import { use } from 'react'

export default function Posts({ posts }: { posts: Promise<Post[]> }) {
  const allPosts = use(posts)
  return <ul>{allPosts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

### SWR / React Query

```tsx
'use client'
import useSWR from 'swr'
const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function BlogPage() {
  const { data, error, isLoading } = useSWR('https://api.vercel.app/blog', fetcher)
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  return <ul>{data.map((p: Post) => <li key={p.id}>{p.title}</li>)}</ul>
}
```

## Deduplication & Caching

| Method | Scope | Use case |
|--------|-------|----------|
| Request memoization (auto) | Single render pass | `fetch` GET/HEAD same URL+options deduped |
| Data Cache (`cache: 'force-cache'`) | Across requests | Share data between render pass + incoming requests |
| `React.cache()` | Single request | Dedupe ORM/DB calls (non-fetch) |

```tsx
import { cache } from 'react'
export const getPost = cache(async (id: string) => {
  return db.query.posts.findFirst({ where: eq(posts.id, parseInt(id)) })
})
```

## Streaming

Breaks HTML into chunks, sent progressively. Two approaches:

### `loading.js` — streams entire page

```tsx
// app/blog/loading.tsx
export default function Loading() {
  return <div>Loading...</div>
}
```

Auto-wraps `page.js` in `<Suspense>`. Shows layout + loading state immediately.

### `<Suspense>` — granular streaming

```tsx
import { Suspense } from 'react'

export default function BlogPage() {
  return (
    <div>
      <header><h1>Blog</h1></header>  {/* sent immediately */}
      <Suspense fallback={<BlogListSkeleton />}>
        <BlogList />                   {/* streams when ready */}
      </Suspense>
    </div>
  )
}
```

## Patterns

### Sequential (dependent data)
Await first, then pass result to child. Wrap child in `<Suspense>` to stream.

```tsx
const artist = await getArtist(username)
// Playlists depends on artist.id — sequential, but streams via Suspense
<Suspense fallback={<div>Loading...</div>}>
  <Playlists artistID={artist.id} />
</Suspense>
```

### Parallel (`Promise.all`)
Start both, await together. Use `Promise.allSettled` if one failure shouldn't block.

```tsx
const artistData = getArtist(username)   // start both immediately
const albumsData = getAlbums(username)
const [artist, albums] = await Promise.all([artistData, albumsData])
```

### Preloading
Call `void getItem(id)` early to start fetch before it's needed. Combine with `React.cache` + `server-only` for reusable cached preloaders.
