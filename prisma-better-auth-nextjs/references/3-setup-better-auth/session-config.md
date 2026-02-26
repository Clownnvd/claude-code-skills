# Step 3.7: Session & Cookie Configuration

> Source: King Template codebase — production session management

## Auth Config (`src/lib/auth.ts`)

```typescript
export const auth = betterAuth({
  // ...

  // Trusted origins — prevents CORS errors on non-standard ports
  trustedOrigins: process.env.BETTER_AUTH_URL
    ? [process.env.BETTER_AUTH_URL]
    : ["http://localhost:3000"],

  // Session configuration
  session: {
    expiresIn: 60 * 60 * 24 * 7,  // 7 days
    updateAge: 60 * 60 * 24,       // Refresh token daily
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60,              // 5 min cache (reduces DB lookups)
    },
  },

  // Cookie security
  advanced: {
    cookiePrefix: "king",                              // Custom prefix
    useSecureCookies: process.env.NODE_ENV === "production",
    defaultCookieSameSite: "lax" as const,
  },
});
```

## Session Settings Explained

| Setting | Value | Why |
|---------|-------|-----|
| `expiresIn` | 7 days | Balance between UX (not logging in daily) and security |
| `updateAge` | 1 day | Refresh session token daily (sliding window) |
| `cookieCache.enabled` | `true` | Caches session in cookie to reduce DB lookups |
| `cookieCache.maxAge` | 5 min | How long cookie cache is valid before re-checking DB |

## Cookie Security Settings

| Setting | Value | Why |
|---------|-------|-----|
| `cookiePrefix` | `"king"` | Namespace cookies to avoid conflicts |
| `useSecureCookies` | `true` in prod | `Secure` flag: HTTPS only in production |
| `defaultCookieSameSite` | `"lax"` | Prevents CSRF while allowing navigation links |

## trustedOrigins

| Scenario | Config |
|----------|--------|
| Default port 3000 | Not needed (Better Auth defaults to it) |
| Custom port (e.g., 3001) | `trustedOrigins: ["http://localhost:3001"]` |
| Production | `trustedOrigins: [process.env.BETTER_AUTH_URL]` |
| Multiple origins | `trustedOrigins: ["https://app.com", "http://localhost:3000"]` |

## Environment Variables

```env
BETTER_AUTH_URL=http://localhost:3000  # or https://yourdomain.com
```

## Client-Side Session Access

```typescript
import { useSession } from "@/lib/auth-client";

function Dashboard() {
  const { data: session, isPending } = useSession();

  if (isPending) return <p>Loading...</p>;
  if (!session?.user) return <p>Not authenticated</p>;

  return <p>Welcome, {session.user.name}</p>;
}
```
