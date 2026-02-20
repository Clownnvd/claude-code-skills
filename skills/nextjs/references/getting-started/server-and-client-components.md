# Server and Client Components

> Source: nextjs.org/docs/app/getting-started/server-and-client-components (v16.1.6)

## When to Use

| Need | Component |
|------|-----------|
| Fetch data (DB, API, secrets) | Server |
| Reduce client JS bundle | Server |
| State, event handlers (`onClick`, `onChange`) | Client |
| Lifecycle (`useEffect`) | Client |
| Browser APIs (`localStorage`, `window`) | Client |
| Custom hooks with state/effects | Client |

## How It Works

### Server
- RSC rendered into RSC Payload (compact binary)
- Client Components + RSC Payload used to pre-render HTML

### Client (first load)
1. HTML shown immediately (non-interactive preview)
2. RSC Payload reconciles Server + Client component trees
3. JS hydrates Client Components (attaches event handlers)

### Subsequent navigations
- RSC Payload prefetched + cached
- Client Components rendered on client only (no server HTML)

## `'use client'` Directive

Marks file as Client Component boundary. All imports and children become client bundle.

```tsx
'use client'
import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

**Key**: Add `'use client'` only to specific interactive components, not entire layouts.

## Composition Patterns

### Pass data via props (Server → Client)
Props must be serializable by React.

```tsx
// app/[id]/page.tsx (Server)
import LikeButton from '@/app/ui/like-button'
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const post = await getPost(id)
  return <LikeButton likes={post.likes} />
}

// app/ui/like-button.tsx (Client)
'use client'
export default function LikeButton({ likes }: { likes: number }) { /* ... */ }
```

### Interleave via children (Server inside Client)
Pass Server Components as `children` to Client Components.

```tsx
// app/ui/modal.tsx (Client)
'use client'
export default function Modal({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}

// app/page.tsx (Server)
import Modal from './ui/modal'
import Cart from './ui/cart'  // Server Component
export default function Page() {
  return <Modal><Cart /></Modal>
}
```

### Context providers
React context not supported in Server Components. Wrap in Client Component:

```tsx
// app/theme-provider.tsx
'use client'
import { createContext } from 'react'
export const ThemeContext = createContext({})
export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  return <ThemeContext.Provider value="dark">{children}</ThemeContext.Provider>
}

// app/layout.tsx (Server) — render provider as deep as possible
import ThemeProvider from './theme-provider'
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html><body><ThemeProvider>{children}</ThemeProvider></body></html>
}
```

### Share data: React.cache + Context + use()

```tsx
// lib/user.ts — cached fetcher (deduped per request)
import { cache } from 'react'
export const getUser = cache(async () => {
  const res = await fetch('https://api.example.com/user')
  return res.json()
})

// Layout: pass promise (don't await) to provider
const userPromise = getUser()
<UserProvider userPromise={userPromise}>{children}</UserProvider>

// Client: resolve with use()
const user = use(userPromise)  // inside <Suspense>
```

`React.cache` scoped to current request only — no cross-request sharing.

### Third-party components without `'use client'`
Wrap in your own Client Component:

```tsx
// app/carousel.tsx
'use client'
import { Carousel } from 'acme-carousel'
export default Carousel
```

## Environment Safety

| Prefix | Available on |
|--------|-------------|
| `NEXT_PUBLIC_` | Client + Server |
| No prefix | Server only (empty string on client) |

Prevent accidental client import of server code:

```ts
import 'server-only'  // build error if imported in Client Component
export async function getData() { /* uses process.env.API_KEY */ }
```

Opposite: `import 'client-only'` for modules using `window` etc.

Both packages are optional — Next.js handles them internally for better error messages.
