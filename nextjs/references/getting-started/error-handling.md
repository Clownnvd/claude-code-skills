# Error Handling

> Source: nextjs.org/docs/app/getting-started/error-handling (v16.1.6)

## Two Categories

| Type | Example | How to handle |
|------|---------|---------------|
| Expected errors | Validation failures, failed requests | Return as values, show in UI |
| Uncaught exceptions | Bugs, unexpected crashes | Error boundaries (`error.tsx`) |

## Expected Errors

### Server Functions (`useActionState`)

Model errors as return values — don't throw.

```ts
// app/actions.ts
'use server'
export async function createPost(prevState: any, formData: FormData) {
  const res = await fetch('https://api.vercel.app/posts', {
    method: 'POST',
    body: { title: formData.get('title'), content: formData.get('content') },
  })
  if (!res.ok) {
    return { message: 'Failed to create post' }
  }
}
```

```tsx
// app/ui/form.tsx
'use client'
import { useActionState } from 'react'
import { createPost } from '@/app/actions'

export function Form() {
  const [state, formAction, pending] = useActionState(createPost, { message: '' })
  return (
    <form action={formAction}>
      <input type="text" name="title" required />
      <textarea name="content" required />
      {state?.message && <p aria-live="polite">{state.message}</p>}
      <button disabled={pending}>Create Post</button>
    </form>
  )
}
```

### Server Components

Conditionally render error message or `redirect`.

```tsx
export default async function Page() {
  const res = await fetch('https://...')
  if (!res.ok) return 'There was an error.'
  return '...'
}
```

### Not Found

Call `notFound()` + create `not-found.tsx` in route segment.

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation'

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = getPostBySlug(slug)
  if (!post) notFound()
  return <div>{post.title}</div>
}

// app/blog/[slug]/not-found.tsx
export default function NotFound() {
  return <div>404 - Page Not Found</div>
}
```

## Uncaught Exceptions (Error Boundaries)

### `error.tsx` — nested error boundary

Must be `'use client'`. Catches errors in child components. Errors bubble to nearest parent boundary.

```tsx
// app/dashboard/error.tsx
'use client'
import { useEffect } from 'react'

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => { console.error(error) }, [error])
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

### `global-error.tsx` — root layout errors

Replaces root layout when active — must define its own `<html>` + `<body>`.

```tsx
// app/global-error.tsx
'use client'
export default function GlobalError({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <html><body>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </body></html>
  )
}
```

### Event handler errors

Error boundaries don't catch event handler errors. Handle manually with `try/catch` + `useState`.

```tsx
'use client'
const [error, setError] = useState(null)
const handleClick = () => {
  try { /* risky work */ } catch (e) { setError(e) }
}
```

Exception: errors inside `startTransition` DO bubble to error boundaries.

## Hierarchy

Place `error.tsx` at different levels for granular handling:

`layout` → `template` → `error` (boundary) → `loading` (suspense) → `not-found` (boundary) → `page`
