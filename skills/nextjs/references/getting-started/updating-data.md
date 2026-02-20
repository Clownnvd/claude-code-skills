# Updating Data (Server Functions / Server Actions)

> Source: nextjs.org/docs/app/getting-started/updating-data (v16.1.6)

## Terminology

- **Server Function** — async function running on server, callable from client via network
- **Server Action** — Server Function used for form submissions/mutations (uses POST)

Actions auto-wrap in `startTransition` when passed to `<form action>` or `<button formAction>`.

## Creating Server Functions

### Inline `'use server'` (per function)

```ts
// app/lib/actions.ts
export async function createPost(formData: FormData) {
  'use server'
  const title = formData.get('title')
  // Update data → revalidate cache
}
```

### File-level `'use server'` (all exports)

```ts
// app/actions.ts
'use server'
export async function createPost() { /* ... */ }
export async function deletePost() { /* ... */ }
```

**Server Components**: can inline `'use server'` functions. Progressive enhancement — works without JS.
**Client Components**: cannot define, but can import from `'use server'` files.

### Pass as props
`<ClientComponent updateItemAction={updateItem} />` → use in `<form action={updateItemAction}>`.

## Invoking

| Method | Where | How |
|--------|-------|-----|
| `<form action={fn}>` | Server + Client | Auto receives `FormData`. Progressive enhancement. |
| `<button formAction={fn}>` | Server + Client | Per-button action override |
| Event handler (`onClick`) | Client only | `await serverFn()` in async handler |
| `useEffect` | Client only | Wrap in `startTransition(async () => { await serverFn() })` |

## After Mutation Patterns

### Pending state (`useActionState`)

```tsx
'use client'
import { useActionState, startTransition } from 'react'

const [state, action, pending] = useActionState(createPost, false)
<button onClick={() => startTransition(action)}>
  {pending ? <Spinner /> : 'Create'}
</button>
```

### Refresh (re-render current page)

```ts
'use server'
import { refresh } from 'next/cache'

export async function updatePost(formData: FormData) {
  // update data...
  refresh()  // re-renders page, does NOT revalidate tagged data
}
```

### Revalidate cache

```ts
import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  'use server'
  // update data...
  revalidatePath('/posts')
}
```

Also: `revalidateTag(tag)` for tag-based invalidation.

### Redirect

```ts
'use server'
import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  // update data...
  revalidatePath('/posts')
  redirect('/posts')  // throws — code after won't execute
}
```

Call `revalidatePath`/`revalidateTag` BEFORE `redirect`.

### Cookies

```ts
'use server'
import { cookies } from 'next/headers'

export async function exampleAction() {
  const cookieStore = await cookies()
  cookieStore.get('name')?.value      // read
  cookieStore.set('name', 'Delba')    // set → triggers page re-render
  cookieStore.delete('name')          // delete → triggers page re-render
}
```

Setting/deleting cookies re-renders current page + layouts on server. Client state preserved.

## Key Notes

- Actions use `POST` only — cannot be invoked via GET
- Client dispatches actions one at a time (sequential, not parallel)
- For parallel work: fetch in Server Components or do parallel work inside a single action
- Client Components queue form submissions before hydration completes
