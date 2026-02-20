# Data Security

> Source: https://nextjs.org/docs/app/guides/data-security (v16.1.6)

## Data Fetching Approaches

| Approach | Best For | Key Principle |
|---|---|---|
| External HTTP APIs | Existing large apps | Zero Trust -- call APIs with auth tokens from Server Components |
| Data Access Layer (DAL) | New projects | Centralized server-only module with auth checks, returns DTOs |
| Component-level access | Prototypes only | Direct DB queries in Server Components (risk of data leaks) |

## Data Access Layer Pattern

```ts
// data/auth.ts
import { cache } from 'react'
import { cookies } from 'next/headers'

export const getCurrentUser = cache(async () => {
  const token = cookies().get('AUTH_TOKEN')
  const decoded = await decryptAndValidate(token)
  return new User(decoded.id) // Return minimal DTO, not raw data
})
```

```ts
// data/user-dto.ts
import 'server-only'
import { getCurrentUser } from './auth'

export async function getProfileDTO(slug: string) {
  const [rows] = await sql`SELECT * FROM user WHERE slug = ${slug}`
  const currentUser = await getCurrentUser()
  return {
    username: canSeeUsername(currentUser) ? rows[0].username : null,
    phone: canSeePhone(currentUser, rows[0].team) ? rows[0].phone : null,
  }
}
```

## Preventing Data Leaks

| Mechanism | Purpose |
|---|---|
| `import 'server-only'` | Build error if module imported in client |
| `NEXT_PUBLIC_` prefix | Only prefixed env vars exposed to browser |
| React Taint APIs | Prevent objects/values from reaching client |
| Minimal DTOs | Return only fields the user is authorized to see |

### Tainting (Experimental)

```js
// next.config.js
module.exports = { experimental: { taint: true } }
```

Uses `experimental_taintObjectReference` and `experimental_taintUniqueValue` to block objects/values from being sent to client.

## Server Actions Security

| Feature | Detail |
|---|---|
| Encrypted action IDs | Non-deterministic, recalculated between builds |
| Dead code elimination | Unused actions removed from client bundle |
| Closure encryption | Closed-over variables auto-encrypted per build |
| POST-only | Only `POST` method allowed |
| Origin check | `Origin` header compared to `Host`/`X-Forwarded-Host` |

### Input Validation (Always Required)

```ts
'use server'
import { z } from 'zod'

export async function createUser(formData: FormData) {
  const validated = z.object({ email: z.string().email() })
    .safeParse({ email: formData.get('email') })
  if (!validated.success) return { errors: validated.error.flatten().fieldErrors }
}
```

### Auth in Every Action

```ts
'use server'
export function addItem() {
  const { user } = auth()
  if (!user) throw new Error('You must be signed in')
}
```

## Advanced Configuration

| Config | Purpose |
|---|---|
| `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` | Consistent encryption across multiple servers (base64, 16/24/32 bytes) |
| `serverActions.allowedOrigins` | Whitelist origins for CSRF protection |

## Audit Checklist

| Check | What to verify |
|---|---|
| DAL isolation | DB packages/env vars not imported outside DAL |
| `"use client"` files | Props don't contain private data; types not too broad |
| `"use server"` files | Args validated; user re-authorized in every action |
| `[param]` folders | Dynamic params validated |
| `route.ts` / `proxy.ts` | Extra scrutiny -- high privilege files |

## Quick Reference

| Task | How |
|---|---|
| Server-only module | `import 'server-only'` at top of file |
| Cache user per request | `cache()` wrapper from React |
| Validate action input | `z.object({...}).safeParse(data)` |
| Encrypt closures | Automatic per build; set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` for multi-server |
| Allow cross-origin actions | `serverActions.allowedOrigins: ['domain.com']` |
| Prevent mutations in render | Use Server Actions, not side-effects in components |
