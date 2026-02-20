# Authentication

> Source: https://nextjs.org/docs/app/guides/authentication (v16.1.6)

## Three Pillars

| Concept              | Purpose                                      |
|----------------------|----------------------------------------------|
| Authentication       | Verify user identity (username/password)     |
| Session Management   | Track auth state across requests             |
| Authorization        | Control route/data access by role            |

## Sign-up Flow (Server Actions + Zod)

```typescript
// app/lib/definitions.ts
import * as z from 'zod'

export const SignupFormSchema = z.object({
  name: z.string().min(2, { error: 'Name must be at least 2 characters long.' }).trim(),
  email: z.email({ error: 'Please enter a valid email.' }).trim(),
  password: z.string().min(8, { error: 'Be at least 8 characters long' })
    .regex(/[a-zA-Z]/, { error: 'Contain at least one letter.' })
    .regex(/[0-9]/, { error: 'Contain at least one number.' })
    .regex(/[^a-zA-Z0-9]/, { error: 'Contain at least one special character.' }).trim(),
})
```

```typescript
// app/actions/auth.ts
export async function signup(state: FormState, formData: FormData) {
  const validatedFields = SignupFormSchema.safeParse({
    name: formData.get('name'), email: formData.get('email'), password: formData.get('password'),
  })
  if (!validatedFields.success) return { errors: validatedFields.error.flatten().fieldErrors }
  const { name, email, password } = validatedFields.data
  const hashedPassword = await bcrypt.hash(password, 10)
  // Insert into DB, create session, redirect
}
```

## Session Management

| Type      | Storage               | Pros              | Cons                     |
|-----------|-----------------------|-------------------|--------------------------|
| Stateless | Cookie (JWT)          | Simple            | Less secure if misused   |
| Database  | DB + encrypted cookie | More secure       | More complex, more I/O   |

### Stateless Session (Jose)

```typescript
// app/lib/session.ts
import 'server-only'
import { SignJWT, jwtVerify } from 'jose'
import { cookies } from 'next/headers'

const encodedKey = new TextEncoder().encode(process.env.SESSION_SECRET)

export async function encrypt(payload: SessionPayload) {
  return new SignJWT(payload).setProtectedHeader({ alg: 'HS256' }).setIssuedAt().setExpirationTime('7d').sign(encodedKey)
}

export async function createSession(userId: string) {
  const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
  const session = await encrypt({ userId, expiresAt })
  const cookieStore = await cookies()
  cookieStore.set('session', session, { httpOnly: true, secure: true, expires: expiresAt, sameSite: 'lax', path: '/' })
}

export async function deleteSession() { (await cookies()).delete('session') }
```

## Authorization

### Data Access Layer (DAL)

```typescript
// app/lib/dal.ts
import 'server-only'
import { cache } from 'react'

export const verifySession = cache(async () => {
  const cookie = (await cookies()).get('session')?.value
  const session = await decrypt(cookie)
  if (!session?.userId) redirect('/login')
  return { isAuth: true, userId: session.userId }
})
```

### Where to Check Auth

| Location         | Method              | Use Case                             |
|------------------|---------------------|--------------------------------------|
| Proxy            | Read cookie only    | Redirect unauthenticated users       |
| Server Component | `verifySession()`   | Role-based UI rendering              |
| Server Action    | `verifySession()`   | Protect mutations                    |
| Route Handler    | `verifySession()`   | Protect API endpoints                |
| Layout           | Avoid auth checks   | Layouts don't re-render on nav       |

**Important**: Do NOT rely on Proxy alone. Always check auth close to data source via DAL.

## Auth Libraries

Auth0, Better Auth, Clerk, Descope, Kinde, Logto, NextAuth.js, Ory, Stack Auth, Supabase, Stytch, WorkOS

## Quick Reference

| Task                   | Pattern                                              |
|------------------------|------------------------------------------------------|
| Validate form          | Zod schema + `safeParse` in Server Action            |
| Create session         | JWT with Jose, set `httpOnly` cookie                 |
| Protect route          | DAL `verifySession()` with `React.cache`             |
| Role-based UI          | Check `session.user.role` in Server Components       |
| Logout                 | Delete session cookie, redirect                      |
| Session refresh        | Re-set cookie with new expiry in proxy/middleware     |
| DTO pattern            | Return only needed fields, never full user object    |
