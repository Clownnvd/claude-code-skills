# Fix Patterns: Rate Limiting + Audit Logging

## Rate Limiting Fixes

### Fix: Strict Auth Rate Limits
```typescript
// src/lib/rate-limit.ts
export const AUTH_RATE_LIMITS = {
  // Strict: login, register, password reset
  strict: { windowMs: 15 * 60 * 1000, max: 5 },
  // Standard: session checks, profile reads
  standard: { windowMs: 15 * 60 * 1000, max: 100 },
  // Verification: email resend
  verification: { windowMs: 60 * 60 * 1000, max: 3 },
} as const;
```

### Fix: IP Extraction (Proxy-Safe)
```typescript
export function getClientIp(request: Request): string {
  const xff = request.headers.get("x-forwarded-for");
  if (xff) {
    const ips = xff.split(",").map((ip) => ip.trim());
    // Use LAST IP (set by trusted proxy), not first (client-spoofable)
    return ips[ips.length - 1];
  }
  return request.headers.get("x-real-ip") ?? "unknown";
}
```

### Fix: Apply Rate Limiting to All Auth Routes
```typescript
// In proxy.ts or individual route handlers
// POST /api/auth/sign-in — strict
// POST /api/auth/sign-up — strict
// POST /api/auth/forgot-password — strict
// POST /api/auth/reset-password — strict
// POST /api/auth/change-password — strict
// GET  /api/auth/session — standard
// POST /api/auth/send-verification-email — verification
// POST /api/checkout/* — strict
// POST /api/webhooks/* — no rate limit (server-to-server)
```

### Fix: Rate Limit Response
```typescript
// Return 429 with Retry-After header
if (isRateLimited) {
  return new Response(
    JSON.stringify({ error: "Too many requests", code: "RATE_LIMITED" }),
    {
      status: 429,
      headers: {
        "Retry-After": String(retryAfterSeconds),
        "Content-Type": "application/json",
      },
    }
  );
}
```

### Fix: Distributed Rate Limiting (Enhancement)
For multi-instance deployments, use external store:
```typescript
// Redis-based (if available), otherwise in-memory is acceptable
// for single-instance deployments (Vercel serverless)
// Flag as "requires Redis" if not available
```

## Audit Logging Fixes

### Fix: Database Hooks for Auth Events
```typescript
// In auth.ts betterAuth() config
databaseHooks: {
  user: {
    create: {
      after: async (user) => {
        await auditLog("user.created", {
          userId: user.id,
          email: user.email,
        });
      },
    },
  },
  session: {
    create: {
      after: async (session) => {
        await auditLog("session.created", {
          userId: session.userId,
          // Do NOT log IP here — get from request context
        });
      },
    },
  },
},
```

### Fix: Structured Audit Log Function
```typescript
// src/lib/auth/audit-log.ts
import { logger } from "@/lib/api/logger";

type AuditEvent =
  | "user.created" | "user.updated" | "user.deleted"
  | "session.created" | "session.revoked"
  | "login.failed" | "login.success"
  | "password.changed" | "password.reset"
  | "email.verified" | "email.changed"
  | "oauth.linked" | "oauth.unlinked"
  | "purchase.completed" | "github.invited";

export async function auditLog(
  event: AuditEvent,
  metadata: Record<string, unknown>
): Promise<void> {
  logger.info({ event, ...metadata, timestamp: new Date().toISOString() });
}
```

### Fix: Log Security-Relevant Events
Must log (at minimum):
1. Login success/failure (with IP, user agent)
2. Password change/reset
3. Email verification
4. OAuth account linking
5. Session revocation
6. Purchase completion
7. Admin actions (if RBAC exists)
