# Cache Components (PPR)

> Source: nextjs.org/docs/app/getting-started/cache-components (v16.1.6)

## Enable

```ts
// next.config.ts
const nextConfig: NextConfig = { cacheComponents: true }
```

Replaces `experimental.ppr` + `experimental.dynamicIO`. Edge Runtime not supported.

## How It Works

Prerendering creates a **static HTML shell**. Content types:

| Type | Behavior | In static shell? |
|------|----------|-----------------|
| Static (sync I/O, imports, pure computation) | Auto-prerendered | Yes |
| Cached (`use cache`) | Cached at build/revalidation | Yes |
| Dynamic (fetch, DB, async I/O) | Wrap in `<Suspense>` — streams at request time | Fallback only |
| Runtime (`cookies()`, `headers()`, `searchParams`) | Must wrap in `<Suspense>` — cannot use `use cache` | Fallback only |

Uncached data outside `<Suspense>` → build error: `Uncached data was accessed outside of <Suspense>`.

## Defer to Request Time (Suspense)

```tsx
import { Suspense } from 'react'

async function DynamicContent() {
  const data = await fetch('https://api.example.com/data')
  return <div>{/* ... */}</div>
}

export default function Page() {
  return (
    <>
      <h1>Part of static shell</h1>
      <Suspense fallback={<p>Loading...</p>}>
        <DynamicContent />
      </Suspense>
    </>
  )
}
```

### Runtime data (cookies, headers, searchParams)

```tsx
import { cookies, headers } from 'next/headers'

async function RuntimeData({ searchParams }) {
  const cookieStore = await cookies()
  const headerStore = await headers()
  const search = await searchParams
  return <div>Personalized content</div>
}
// Must wrap in <Suspense> — cannot be cached with use cache
```

### Non-deterministic operations (`Math.random()`, `Date.now()`, `crypto.randomUUID()`)

Use `await connection()` from `next/server` to defer, then wrap in `<Suspense>`.

## Using `use cache`

Cache async functions/components. Arguments + closed-over values = cache key.

```tsx
import { cacheLife } from 'next/cache'

export default async function Page() {
  'use cache'
  cacheLife('hours')
  const users = await db.query('SELECT * FROM users')
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
}
```

### cacheLife profiles

| Profile | Usage |
|---------|-------|
| `'hours'` / `'days'` / `'weeks'` / `'max'` | Named presets |
| `{ stale, revalidate, expire }` | Custom (seconds) |

### With runtime data (workaround)

Read runtime data in uncached component, pass values as props to cached component:

```tsx
async function ProfileContent() {
  const session = (await cookies()).get('session')?.value
  return <CachedContent sessionId={session} />  // sessionId = cache key
}
async function CachedContent({ sessionId }: { sessionId: string }) {
  'use cache'
  const data = await fetchUserData(sessionId)
  return <div>{data}</div>
}
```

### Tagging and revalidating

```tsx
import { cacheTag, updateTag, revalidateTag } from 'next/cache'

// Tag cached data
async function getCart() { 'use cache'; cacheTag('cart'); /* ... */ }

// updateTag — expire + refresh in same request (immediate)
async function updateCart(itemId: string) { 'use server'; updateTag('cart') }

// revalidateTag — stale-while-revalidate (eventual consistency)
async function createPost(post: FormData) { 'use server'; revalidateTag('posts', 'max') }
```

## Composing: Static + Cached + Dynamic

`<header>` (static, auto) + `<BlogPosts>` (`use cache`, in shell) + `<UserPreferences>` (runtime, `<Suspense>` streams).

## Activity Component

With `cacheComponents`, navigation uses React `<Activity>` — previous routes set to `"hidden"`, state preserved, effects cleaned up on hide/show.

## Migration from Route Segment Configs

| Old config | Replacement |
|-----------|-------------|
| `dynamic = 'force-dynamic'` | Remove (all pages dynamic by default) |
| `dynamic = 'force-static'` | `'use cache'` + `cacheLife('max')` |
| `revalidate = 3600` | `'use cache'` + `cacheLife('hours')` |
| `fetchCache = 'force-cache'` | `'use cache'` (auto-caches all fetches in scope) |
| `runtime = 'edge'` | Not supported — Node.js only |
