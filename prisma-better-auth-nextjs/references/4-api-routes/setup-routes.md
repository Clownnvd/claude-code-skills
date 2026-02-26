# Step 4: Set Up the API Routes

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Create Auth API Route

Better Auth uses a catch-all route to handle all auth endpoints.

```typescript
// src/app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { POST, GET } = toNextJsHandler(auth);
```

## Create Auth Client

The auth client provides React hooks and methods for client-side auth.

```typescript
// src/lib/auth-client.ts
import { createAuthClient } from "better-auth/react";

export const { signIn, signUp, signOut, useSession } = createAuthClient();
```

## API Endpoints Provided

Better Auth auto-registers these endpoints under `/api/auth/`:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/sign-up/email` | POST | Register with email/password |
| `/api/auth/sign-in/email` | POST | Sign in with email/password |
| `/api/auth/sign-out` | POST | Sign out (invalidate session) |
| `/api/auth/get-session` | GET | Get current session |

## Client Exports

| Export | Type | Usage |
|--------|------|-------|
| `signUp` | function | `signUp.email({ name, email, password })` |
| `signIn` | function | `signIn.email({ email, password })` |
| `signOut` | function | `signOut()` |
| `useSession` | hook | `const { data: session, isPending } = useSession()` |

## Next Step

Proceed to [5-pages/sign-up.md](../5-pages/sign-up.md).
