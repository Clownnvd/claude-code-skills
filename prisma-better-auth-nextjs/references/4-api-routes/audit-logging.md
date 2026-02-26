# Step 4.3: Audit Logging

> Source: King Template codebase — structured auth event logging

## Overview

Log authentication events for security auditing. JSON in production (for log aggregation), readable in development.

## Implementation (`src/lib/auth/audit-log.ts`)

```typescript
type AuditEvent =
  | "sign_in"
  | "sign_up"
  | "sign_out"
  | "login_failed"
  | "password_changed"
  | "password_reset_request"
  | "password_reset_complete"
  | "email_verified"
  | "email_changed"
  | "oauth_link"
  | "oauth_unlink"
  | "session_revoked"
  | "2fa_enabled"
  | "2fa_disabled"
  | "purchase_completed"
  | "github_invited";

interface AuditEntry {
  level: "info" | "warn";
  event: AuditEvent;
  userId: string;
  provider?: string;
  ip?: string;
  timestamp: string;
}

export function logAuthEvent(
  event: AuditEvent,
  userId: string,
  extra?: { provider?: string; ip?: string }
): void {
  const entry: AuditEntry = {
    level: ["password_reset_request", "login_failed", "session_revoked"]
      .includes(event) ? "warn" : "info",
    event,
    userId,
    provider: extra?.provider,
    ip: extra?.ip,
    timestamp: new Date().toISOString(),
  };

  if (process.env.NODE_ENV === "production") {
    console.info(JSON.stringify(entry));
  } else {
    console.info(
      `[AUTH] ${entry.event} user=${entry.userId}` +
      `${entry.provider ? ` provider=${entry.provider}` : ""}`
    );
  }
}
```

## Integration with Better Auth (`src/lib/auth.ts`)

```typescript
export const auth = betterAuth({
  // ...

  databaseHooks: {
    user: {
      create: {
        after: async (user) => {
          logAuthEvent("sign_up", user.id);
        },
      },
    },
    session: {
      create: {
        after: async (session) => {
          logAuthEvent("sign_in", session.userId, {
            ip: session.ipAddress ?? undefined,
          });
        },
      },
      delete: {
        after: async (session) => {
          logAuthEvent("sign_out", session.userId);
        },
      },
    },
    account: {
      create: {
        after: async (account) => {
          logAuthEvent("oauth_link", account.userId, {
            provider: account.providerId,
          });
        },
      },
      delete: {
        after: async (account) => {
          logAuthEvent("oauth_unlink", account.userId, {
            provider: account.providerId,
          });
        },
      },
    },
  },
});
```

## Key Patterns

| Pattern | Details |
|---------|---------|
| No PII | Only `userId` + event type — never email, name, etc. |
| Level escalation | `warn` for security-sensitive events (failed login, password reset) |
| Production format | Structured JSON for Datadog/CloudWatch/etc. |
| Dev format | Readable `[AUTH] sign_in user=abc123` |
| Hook integration | `databaseHooks` fire automatically on DB operations |

## Events by Category

| Category | Events |
|----------|--------|
| Auth flow | `sign_in`, `sign_up`, `sign_out`, `login_failed` |
| Password | `password_changed`, `password_reset_request`, `password_reset_complete` |
| Email | `email_verified`, `email_changed` |
| OAuth | `oauth_link`, `oauth_unlink` |
| Security | `session_revoked`, `2fa_enabled`, `2fa_disabled` |
| Business | `purchase_completed`, `github_invited` |
