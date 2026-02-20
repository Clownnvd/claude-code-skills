# Forms

> Source: https://nextjs.org/docs/app/guides/forms (v16.1.6)

React Server Actions handle form submissions. They receive `FormData` automatically via the `action` attribute.

## Basic Form

```tsx
// app/invoices/page.tsx
export default function Page() {
  async function createInvoice(formData: FormData) {
    'use server'
    const rawFormData = {
      customerId: formData.get('customerId'),
      amount: formData.get('amount'),
      status: formData.get('status'),
    }
    // mutate data, revalidate cache
  }
  return <form action={createInvoice}>...</form>
}
```

> **Tip:** For many fields, use `Object.fromEntries(formData)` (note: includes extra `$ACTION_` props).

## Passing Extra Arguments

Use `Function.bind` to prepend arguments:

```tsx
'use client'
import { updateUser } from './actions'

export function UserProfile({ userId }: { userId: string }) {
  const updateUserWithId = updateUser.bind(null, userId)
  return (
    <form action={updateUserWithId}>
      <input type="text" name="name" />
      <button type="submit">Update</button>
    </form>
  )
}
```

```ts
// app/actions.ts
'use server'
export async function updateUser(userId: string, formData: FormData) {}
```

## Server-Side Validation (Zod)

```ts
'use server'
import { z } from 'zod'

const schema = z.object({ email: z.string().email() })

export async function createUser(initialState: any, formData: FormData) {
  const result = schema.safeParse({ email: formData.get('email') })
  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors }
  }
  // mutate data
}
```

## Displaying Errors with `useActionState`

```tsx
'use client'
import { useActionState } from 'react'
import { createUser } from '@/app/actions'

export function Signup() {
  const [state, formAction, pending] = useActionState(createUser, { message: '' })
  return (
    <form action={formAction}>
      <input type="email" name="email" required />
      <p aria-live="polite">{state?.message}</p>
      <button disabled={pending}>Sign up</button>
    </form>
  )
}
```

## Pending States with `useFormStatus`

```tsx
'use client'
import { useFormStatus } from 'react-dom'

export function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending} type="submit">Submit</button>
}
```

> Must be a **child** of `<form>`, not the component defining the form.

## Optimistic Updates

```tsx
'use client'
import { useOptimistic } from 'react'
import { send } from './actions'

type Message = { message: string }

export function Thread({ messages }: { messages: Message[] }) {
  const [optimistic, addOptimistic] = useOptimistic<Message[], string>(
    messages,
    (state, newMsg) => [...state, { message: newMsg }]
  )
  const formAction = async (formData: FormData) => {
    const msg = formData.get('message') as string
    addOptimistic(msg)
    await send(msg)
  }
  return (
    <div>
      {optimistic.map((m, i) => <div key={i}>{m.message}</div>)}
      <form action={formAction}>
        <input type="text" name="message" />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}
```

## Nested Actions & Programmatic Submit

- Use `formAction` prop on `<button>` for multiple actions in one form
- Programmatic: `e.currentTarget.form?.requestSubmit()`

## Quick Reference

| Task | How |
|---|---|
| Basic form | `<form action={serverAction}>` |
| Get form data | `formData.get('field')` or `Object.fromEntries(formData)` |
| Extra args | `action.bind(null, arg)` |
| Server validation | `z.object({}).safeParse()` |
| Show errors | `useActionState(action, initialState)` returns `[state, formAction, pending]` |
| Pending state | `useFormStatus()` in child component or `useActionState` pending |
| Optimistic UI | `useOptimistic(data, updaterFn)` |
| Keyboard submit | `form.requestSubmit()` on keydown |
| Multiple actions | `formAction` prop on `<button>` elements |