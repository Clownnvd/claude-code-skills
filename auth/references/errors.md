# Better Auth -- Errors & Fixes Database

> Section 10 from the comprehensive reference. 22 documented errors.

---

## 10. Errors & Fixes Database

### BA-001: `getSessionCookie` Returns null in proxy.ts

**Error**: `getSessionCookie(request)` returns `null` even when user is logged in.
**Cause**: Custom cookie prefix in auth config but not passed to `getSessionCookie`.
**Fix**:
```typescript
// If your auth config has:
advanced: { cookiePrefix: "cviet" }

// Then in proxy.ts:
const session = getSessionCookie(request, { cookiePrefix: "cviet" })
```

---

### BA-002: `redirect_uri_mismatch` with Google OAuth

**Error**: Google returns `Error 400: redirect_uri_mismatch` during OAuth flow.
**Cause**: `BETTER_AUTH_URL` not set, or redirect URI not registered in Google Console.
**Fix**:
1. Set `BETTER_AUTH_URL=http://localhost:3000` in `.env`
2. In Google Cloud Console, add authorized redirect URI:
   `http://localhost:3000/api/auth/callback/google`
3. For production, add: `https://yourdomain.com/api/auth/callback/google`

---

### BA-003: `state_mismatch` Error with Social Providers

**Error**: OAuth callback fails with `state_mismatch` error.
**Cause**: Multiple possible causes:
  - SameSite=Lax cookie not sent on POST callbacks (Apple Sign-In)
  - Better Auth v1.4.4 regression
  - Dual module hazard (two better-auth versions in node_modules)
**Fix**:
1. Check for duplicate installations: `pnpm why @better-auth/core`
2. If using v1.4.4, downgrade to v1.4.3 or upgrade to latest stable
3. For Apple Sign-In, use the workaround for POST-based callbacks
4. Clean reinstall: `rm -rf node_modules pnpm-lock.yaml && pnpm install`

---

### BA-004: `No request state found`

**Error**: `No request state found. Please make sure you are calling this function within a runWithRequestState callback.`
**Cause**: Calling `auth.api.*` methods outside of a proper request context, or dual module hazard.
**Fix**:
1. Ensure you are calling `auth.api.*` inside a route handler, server action, or server component
2. Check for duplicate `better-auth` installations
3. Add `better-auth` to `serverExternalPackages` in `next.config.ts`:
```typescript
const nextConfig: NextConfig = {
  serverExternalPackages: ["better-auth"],
}
```
4. Force resolution in package.json:
```json
{
  "resolutions": {
    "better-call": "1.x.x"
  }
}
```

---

### BA-005: Cookies Not Set After Server Action Sign-In

**Error**: Calling `auth.api.signInEmail()` in a server action succeeds but no session cookie is set.
**Cause**: Missing `nextCookies` plugin. Server actions cannot set cookies on their own.
**Fix**:
```typescript
// src/lib/auth.ts
import { nextCookies } from "better-auth/next-js"

export const auth = betterAuth({
  // ... config
  plugins: [nextCookies()],  // MUST be last plugin
})
```

---

### BA-006: `Cannot resolve "better-auth/cookies"` in proxy.ts

**Error**: Module `better-auth/cookies` cannot be resolved, or `getSessionCookie` is undefined.
**Cause**: Incorrect import path or outdated better-auth version.
**Fix**:
```typescript
// Correct import:
import { getSessionCookie } from "better-auth/cookies"

// If still failing, try:
import { getSessionCookie } from "better-auth/dist/cookies"

// Or install latest:
pnpm add better-auth@latest
```

---

### BA-007: `useSession` Returns Stale Data After Sign-In

**Error**: After calling `signIn.email()`, `useSession()` still shows no session.
**Cause**: React Query / nano-store cache not invalidated.
**Fix**:
```typescript
// Option 1: Use callbackURL to force page reload
await authClient.signIn.email({
  email, password,
  callbackURL: "/dashboard",  // triggers full navigation
})

// Option 2: Manual refresh after sign-in
const { data, error } = await authClient.signIn.email({ email, password })
if (!error) {
  await authClient.getSession({ query: { disableCookieCache: true } })
  router.push("/dashboard")
  router.refresh()  // force RSC re-render
}
```

---

### BA-008: 405 Method Not Allowed on Auth Routes

**Error**: POST requests to `/api/auth/sign-in/email` return 405.
**Cause**: Route handler file not exporting both GET and POST.
**Fix**:
```typescript
// src/app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

// MUST export both GET and POST
export const { GET, POST } = toNextJsHandler(auth)
```

---

### BA-009: `headers()` Must Be Awaited in Next.js 16

**Error**: `TypeError: headers is not iterable` or `TypeError: Cannot read properties of Promise`
**Cause**: In Next.js 16, `headers()` and `cookies()` are async and must be awaited.
**Fix**:
```typescript
// WRONG (Next.js 15 pattern):
const session = await auth.api.getSession({ headers: headers() })

// CORRECT (Next.js 16):
const session = await auth.api.getSession({ headers: await headers() })
```

---

### BA-010: Email Verification Silent Failure

**Error**: User signs up, `sendVerificationEmail` is called, but email provider throws. User is created in DB without verified email.
**Cause**: `sendVerificationEmail` callback executes AFTER user is persisted. No error propagation mechanism.
**Fix**:
1. Wrap email sending in try-catch with logging
2. Set `requireEmailVerification: true` so unverified users cannot log in
3. Provide a "resend verification" button:
```typescript
await authClient.sendVerificationEmail({
  email: "user@example.com",
  callbackURL: "/",
})
```

---

### BA-011: RSC Cannot Refresh Cookie Cache

**Error**: Session cookie cache becomes stale in Server Components.
**Cause**: React Server Components cannot set cookies. Cookie cache refresh only happens via client-side interactions (Server Actions or Route Handlers).
**Fix**:
- Accept slight staleness in RSCs (up to `maxAge` of cookie cache)
- Use a client component to trigger periodic `getSession()` calls
- Set a shorter `cookieCache.maxAge` for critical pages

---

### BA-012: `@better-auth/cli` Broken with Zod v4

**Error**: `npx @better-auth/cli generate` throws import error related to Zod.
**Cause**: Legacy `import * as z from 'zod/v4'` was deprecated.
**Fix**:
```bash
# Use latest CLI version
npx @better-auth/cli@latest generate

# If still failing, pin zod version
pnpm add zod@3.24.0
```

---

### BA-013: TypeScript Type Inference Fails

**Error**: `auth.$Infer.Session` returns `any` or types are not narrowing properly.
**Cause**: `strict: true` not enabled in tsconfig.json.
**Fix**:
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true
    // or at minimum:
    // "strictNullChecks": true
  }
}
```

---

### BA-014: Session Data Missing `user` Fields After OAuth

**Error**: `session.user.name` is null after Google sign-in even though Google profile has it.
**Cause**: Prisma schema `name` field is `String?` (nullable) and the OAuth profile mapping might differ.
**Fix**:
Ensure your Prisma User model includes the correct fields and Better Auth is configured to map them:
```typescript
// Check the raw session
const session = await auth.api.getSession({ headers: await headers() })
console.log(session)  // inspect user object
```
If the Google profile field names differ, use the `mapProfileToUser` option (if available) or a hook.

---

### BA-015: `Prisma.JsonValue` Cast Errors

**Error**: `Type 'JsonValue' is not assignable to type 'CVData'` when reading JSON columns.
**Cause**: Prisma returns `JsonValue` for JSON columns, which is a union type.
**Fix**:
```typescript
// Double-cast through unknown
const cvData = cv.data as unknown as CVData
```

---

### BA-016: Proxy.ts Silently Ignored (Not Working)

**Error**: Auth redirect rules in proxy.ts are not being applied.
**Cause**: File is still named `middleware.ts`, or function is still named `middleware`.
**Fix**:
```typescript
// 1. Rename: middleware.ts --> proxy.ts (or src/proxy.ts)
// 2. Change function name:
export function proxy(request: NextRequest) {  // NOT "middleware"
  // ...
}
```

---

### BA-017: Rate Limit Not Working in Development

**Error**: Rate limiting has no effect during development.
**Cause**: Rate limiting is disabled by default in development mode.
**Fix**:
```typescript
rateLimit: {
  enabled: true,  // force enable in dev
}
```

---

### BA-018: `signUp.email` Returns User Already Exists

**Error**: `{ error: { message: "User already exists" } }` on signup.
**Cause**: Email is already registered (possibly via Google OAuth).
**Fix**:
- Show clear error message: "This email is already registered. Try logging in instead."
- If account linking is desired, guide user to sign in with existing method first

---

### BA-019: `better-auth/cookies` getSessionCookie Returns Null in Edge Runtime

**Error**: `getSessionCookie()` returns null when using Next.js Edge Runtime.
**Cause**: Cookie parsing differences between Edge and Node.js runtimes.
**Fix**:
Next.js 16 proxy runs in Node.js runtime by default, so this is less of an issue. If explicitly using Edge:
```typescript
// Read cookie manually
const token = request.cookies.get("better-auth.session_token")?.value
const hasSession = !!token
```

---

### BA-020: Session Lost After Deploy / Restart

**Error**: All users are logged out after server restart or new deployment.
**Cause**: `BETTER_AUTH_SECRET` changed between deployments. Cookie signatures become invalid.
**Fix**:
- Store `BETTER_AUTH_SECRET` in a persistent secret manager (Vercel env vars, AWS Secrets Manager)
- NEVER generate a new secret per deployment
- If you must rotate, implement gradual rotation

---

### BA-021: Google OAuth Refresh Token Missing

**Error**: `refreshToken` is null in Account table after Google sign-in.
**Cause**: Google only provides refresh token on FIRST authorization. Subsequent sign-ins skip it.
**Fix**:
```typescript
socialProviders: {
  google: {
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    accessType: "offline",
    prompt: "consent",  // force consent screen to get refresh token
  },
}
```

---

### BA-022: Unverified Email Error (403)

**Error**: Sign-in returns HTTP 403 with message about email verification.
**Cause**: `requireEmailVerification: true` is set and user hasn't verified their email.
**Fix** (Client-side handling):
```typescript
const { error } = await authClient.signIn.email({ email, password })
if (error?.status === 403) {
  // Show verification prompt
  setError("Please verify your email. Check your inbox.")
  // Offer resend button
  await authClient.sendVerificationEmail({ email, callbackURL: "/" })
}
```
