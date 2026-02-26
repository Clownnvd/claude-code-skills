# Single-Page Applications (SPA)

> Source: https://nextjs.org/docs/app/guides/single-page-applications (v16.1.6)

## Why Next.js for SPAs?

| Benefit | Description |
|---------|-------------|
| Auto code-splitting | Multiple HTML entry points per route (not one giant bundle) |
| Prefetching | `<Link>` prefetches routes for instant transitions |
| Progressive adoption | Start as SPA, add server features (RSC, Server Actions) incrementally |

## Data Fetching Patterns

### Pattern 1: React `use()` + Context Provider

Hoist data fetching to root layout (starts on server, streams to client):

```typescript
// app/layout.tsx
import { UserProvider } from './user-provider'
import { getUser } from './user'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  let userPromise = getUser() // do NOT await
  return (
    <html lang="en">
      <body>
        <UserProvider userPromise={userPromise}>{children}</UserProvider>
      </body>
    </html>
  )
}
```

Create `app/user-provider.ts` (`'use client'`): a context that stores `userPromise`, with `useUser()` hook. Then consume in any client component:

```typescript
'use client'
import { use } from 'react'
import { useUser } from './user-provider'

export function Profile() {
  const { userPromise } = useUser()
  const user = use(userPromise) // suspends until resolved
  return <div>{user.name}</div>
}
```

### Pattern 2: SWR (2.3.0+ / React 19+)

```typescript
// app/layout.tsx (Server Component)
import { SWRConfig } from 'swr'
import { getUser } from './user'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <SWRConfig value={{ fallback: { '/api/user': getUser() } }}>
      {children}
    </SWRConfig>
  )
}
```

```typescript
// app/profile.tsx (Client Component)
'use client'
import useSWR from 'swr'

export function Profile() {
  const fetcher = (url: string) => fetch(url).then((res) => res.json())
  const { data } = useSWR('/api/user', fetcher) // no code changes needed
  return <div>{data?.name}</div>
}
```

### Pattern 3: React Query

See [React Query SSR docs](https://tanstack.com/query/latest/docs/framework/react/guides/advanced-ssr).

## Browser-Only Rendering

Disable prerendering for components needing browser APIs:

```typescript
import dynamic from 'next/dynamic'

const ClientOnly = dynamic(() => import('./component'), { ssr: false })
```

## Shallow Routing

Use `window.history.pushState`/`replaceState` to update URL without navigation. Integrates with `usePathname` and `useSearchParams`:

```typescript
'use client'
import { useSearchParams } from 'next/navigation'

export default function SortProducts() {
  const searchParams = useSearchParams()
  function updateSorting(sortOrder: string) {
    const params = new URLSearchParams(searchParams.toString())
    params.set('sort', sortOrder)
    window.history.pushState(null, '', `?${params.toString()}`)
  }
  return <button onClick={() => updateSorting('asc')}>Sort</button>
}
```

## Server Actions from Client Components

```typescript
// app/actions.ts
'use server'
export async function create() { /* ... */ }

// app/button.tsx
'use client'
import { create } from './actions'
export function Button() {
  return <button onClick={() => create()}>Create</button>
}
```

No API endpoint needed.

## Static Export (Optional)

```typescript
// next.config.ts
import type { NextConfig } from 'next'
const nextConfig: NextConfig = { output: 'export' }
export default nextConfig
```

Generates `out/` folder with per-route HTML files. Server features not supported.

## Quick Reference

| Task | Approach |
|------|----------|
| Server-started data fetch | Pass Promise from layout, unwrap with `use()` |
| SWR integration | `SWRConfig` fallback in Server Component layout |
| Browser-only component | `dynamic(() => import(...), { ssr: false })` |
| Shallow URL update | `window.history.pushState` |
| Server mutations | Import Server Actions in Client Components |
| Full static SPA | `output: 'export'` in config |
| Migration guides | CRA, Vite, Pages Router |
