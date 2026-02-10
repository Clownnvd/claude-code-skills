# Fix Patterns: Security + Auth & AuthZ

Covers api-scoring categories 1 (Security, 20%) and 2 (Auth & AuthZ, 15%).

## CSP Hardening (unsafe-inline/unsafe-eval)

### Problem
```typescript
"Content-Security-Policy": "script-src 'self' 'unsafe-inline' 'unsafe-eval' ..."
```

### Fix: Use nonces or strict-dynamic
```typescript
import { randomBytes } from "crypto";

function generateNonce() { return randomBytes(16).toString("base64"); }

// In proxy.ts:
const nonce = generateNonce();
response.headers.set(
  "Content-Security-Policy",
  `script-src 'self' 'nonce-${nonce}' 'strict-dynamic' https://js.stripe.com; ...`
);
// Pass nonce to pages via header for inline scripts
response.headers.set("X-Nonce", nonce);
```

**Alternative (if nonces too complex):** Remove `'unsafe-eval'`, keep `'unsafe-inline'` with `strict-dynamic`.

## CORS Explicit Allowlist

### Problem: No explicit CORS (relying on browser same-origin default)

### Fix: Add CORS headers in proxy
```typescript
const ALLOWED_ORIGINS = [process.env.NEXT_PUBLIC_APP_URL];

if (req.method === "OPTIONS") {
  return new NextResponse(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": origin,
      "Access-Control-Allow-Methods": "GET,POST,PATCH,DELETE",
      "Access-Control-Allow-Headers": "Content-Type,Authorization",
      "Access-Control-Max-Age": "86400",
    },
  });
}
```

## Content-Type Enforcement

### Problem: No check that request body is actually JSON

### Fix: Validate Content-Type at route entry
```typescript
// In a shared helper or per-route
function requireJson(req: NextRequest): NextResponse | null {
  const ct = req.headers.get("content-type");
  if (!ct || !ct.includes("application/json")) {
    return errorResponse("Content-Type must be application/json", 415);
  }
  return null;
}
```

## Audit Logging for Auth Events

### Problem: No logging of login, logout, failed auth attempts

### Fix: Add auth hooks in Better Auth config
```typescript
export const auth = betterAuth({
  // ...existing config
  hooks: {
    after: [
      {
        matcher: (ctx) => ctx.path.startsWith("/sign-in"),
        handler: async (ctx) => {
          logger.info({
            event: "auth_attempt",
            method: ctx.path,
            success: !ctx.responseError,
            ip: ctx.request?.headers.get("x-forwarded-for"),
            timestamp: new Date().toISOString(),
          });
        },
      },
    ],
  },
});
```

## BFLA: Admin Separation

### Problem: Single role, no admin vs user separation

### Fix: Add role check helper
```typescript
export async function requireAdmin() {
  const session = await requireAuth();
  if (session.user.role !== "ADMIN") {
    throw new Error("Forbidden: Admin access required");
  }
  return session;
}
```

**Note**: Only add if admin endpoints exist. Single-role apps (all users equal) score neutral.

## Dependency Scanning in CI

### Problem: No automated CVE scanning

### Fix: Add npm audit to CI pipeline
```yaml
# .github/workflows/security.yml
- name: Security audit
  run: npm audit --audit-level=high
```

Or use `pnpm audit` / Snyk / Socket.dev integration.
