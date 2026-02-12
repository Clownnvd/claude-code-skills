# Fix Patterns: Authorization (RBAC) + 2FA/MFA

## Authorization Fixes

### Fix: Two-Layer Auth Pattern
```
Layer 1: Proxy (Node Runtime)
├── Fast cookie check: "better-auth.session_token" (or prefixed)
├── Redirect to /sign-in if missing
├── Preserve callbackUrl in search params
└── Apply security headers

Layer 2: API Routes (Node Runtime)
├── requireAuth(): full session verification with DB
├── Returns 401 with error code if invalid
└── Provides session.user for route handlers
```

### Fix: Proxy Cookie Check
```typescript
// src/proxy.ts
const protectedPaths = ["/dashboard", "/api/user", "/api/checkout"];

function isProtectedPath(pathname: string): boolean {
  return protectedPaths.some((p) => pathname.startsWith(p));
}

// In proxy handler:
if (isProtectedPath(pathname)) {
  const sessionCookie = request.cookies.get(
    "better-auth.session_token"
  )?.value;

  if (!sessionCookie || sessionCookie.length < 20) {
    const signInUrl = new URL("/sign-in", request.url);
    signInUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(signInUrl);
  }
}
```

### Fix: requireAuth() Helper
```typescript
// src/lib/auth.ts or src/lib/auth/require-auth.ts
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

export async function requireAuth() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    return { error: "UNAUTHORIZED" as const, session: null };
  }

  return { error: null, session };
}
```

### Fix: Role-Based Access (if needed)
```typescript
// For simple buyer/admin roles:
// Option 1: Better Auth admin plugin
plugins: [admin()],

// Option 2: Custom role field on user
// Add role: "user" | "admin" to User model
// Check in requireAuth:
export async function requireAdmin() {
  const { error, session } = await requireAuth();
  if (error) return { error, session: null };
  if (session.user.role !== "admin") {
    return { error: "FORBIDDEN" as const, session: null };
  }
  return { error: null, session };
}
```

### Fix: Callback URL Validation
```typescript
function isValidCallbackUrl(url: string): boolean {
  // Block open redirect attacks
  if (url.startsWith("//") || url.startsWith("/\\")) return false;
  if (!url.startsWith("/")) return false;
  // Must be relative path only
  try {
    new URL(url, "http://localhost");
    return true;
  } catch {
    return false;
  }
}
```

## 2FA/MFA Fixes

### Fix: Add 2FA Plugin (Better Auth)
```typescript
import { twoFactor } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    twoFactor({
      issuer: "King Template",
      // TOTP (authenticator app)
      totpOptions: {
        period: 30,
        digits: 6,
      },
    }),
  ],
});
```

### Fix: 2FA Client Setup
```typescript
// Client-side: enable 2FA for user
import { createAuthClient } from "better-auth/react";

const client = createAuthClient({
  plugins: [twoFactorClient()],
});

// Enable 2FA
const { data } = await client.twoFactor.enable();
// data.totpURI — show as QR code

// Verify 2FA during login
await client.twoFactor.verifyTotp({ code: "123456" });
```

### Fix: 2FA Enforcement (Optional)
```typescript
// For enterprise: require 2FA for admin users
// In requireAdmin():
if (session.user.role === "admin" && !session.user.twoFactorEnabled) {
  return { error: "2FA_REQUIRED" as const, session: null };
}
```

### Scoring Note
2FA is worth 5% of total score. For a template product:
- Having the plugin installed + documented = 8/10
- Full 2FA flow (setup, verify, recovery codes) = 10/10
- No 2FA at all = 3/10 (acceptable for simple products)
