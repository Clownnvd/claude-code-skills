# Lazy Loading

> Source: https://nextjs.org/docs/app/guides/lazy-loading (v16.1.6)

Lazy loading defers loading of Client Components and libraries, reducing initial JavaScript bundle size. Server Components are automatically code-split.

## Two Approaches

| Method | Use Case |
|--------|----------|
| `next/dynamic` | Composite of `React.lazy()` + `Suspense`, works in both `app/` and `pages/` |
| `React.lazy()` + `Suspense` | Standard React pattern |

## `next/dynamic` Examples

### Importing Client Components

```typescript
'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'

const ComponentA = dynamic(() => import('../components/A'))
const ComponentB = dynamic(() => import('../components/B'))
const ComponentC = dynamic(() => import('../components/C'), { ssr: false })

export default function Page() {
  const [showMore, setShowMore] = useState(false)
  return (
    <div>
      <ComponentA />                           {/* separate bundle, loads immediately */}
      {showMore && <ComponentB />}             {/* loads on demand */}
      <button onClick={() => setShowMore(!showMore)}>Toggle</button>
      <ComponentC />                           {/* client-only, no SSR */}
    </div>
  )
}
```

### Skipping SSR

```typescript
const ComponentC = dynamic(() => import('../components/C'), { ssr: false })
```

> `ssr: false` only works in Client Components. Not allowed in Server Components.

### Custom Loading Component

```typescript
'use client'

import dynamic from 'next/dynamic'

const Heavy = dynamic(() => import('../components/Heavy'), {
  loading: () => <p>Loading...</p>,
})
```

### Named Exports

```typescript
import dynamic from 'next/dynamic'

const Hello = dynamic(() =>
  import('../components/hello').then((mod) => mod.Hello)
)
```

### Importing Server Components

Only child Client Components are lazy-loaded; the Server Component itself is not. Also preloads static assets (CSS):

```typescript
import dynamic from 'next/dynamic'

const ServerComp = dynamic(() => import('../components/ServerComponent'))

export default function Page() {
  return <ServerComp />
}
```

### Loading External Libraries On Demand

```typescript
'use client'

import { useState } from 'react'

export default function Page() {
  const [results, setResults] = useState<any>()

  return (
    <input
      type="text"
      placeholder="Search"
      onChange={async (e) => {
        const { value } = e.currentTarget
        const Fuse = (await import('fuse.js')).default
        const fuse = new Fuse(['Tim', 'Joe', 'Bel', 'Lee'])
        setResults(fuse.search(value))
      }}
    />
  )
}
```

## Quick Reference

| Item | Detail |
|------|--------|
| Import | `import dynamic from 'next/dynamic'` |
| Skip SSR | `{ ssr: false }` (Client Components only) |
| Loading UI | `{ loading: () => <Spinner /> }` |
| Named exports | `.then((mod) => mod.ExportName)` |
| External libs | Use `await import('lib')` inside event handlers |
| Server Components | Auto code-split; `dynamic()` lazy-loads their Client children |
