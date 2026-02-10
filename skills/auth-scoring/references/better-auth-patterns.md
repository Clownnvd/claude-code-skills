# Better Auth + Next.js — Scoring Adjustments

## Better Auth Config Checklist

Check `auth.ts` (or wherever `betterAuth()` is called):

| Feature | Config Key | Score Impact |
|---------|-----------|-------------|
| Email + password | `emailAndPassword.enabled` | Required for score > 3 |
| Email verification | `emailVerification.sendOnSignUp` | +1 if enabled |
| Verification auto-enable | `requireEmailVerification: Boolean(process.env.RESEND_API_KEY)` | +1 for env-gated |
| OAuth providers | `socialProviders.{google,github}` | +1 per provider |
| Env-gated providers | `enabled: Boolean(process.env.CLIENT_ID && ...)` | +1 for clean disable |
| Account linking | `account.accountLinking.enabled` | +1 |
| Trusted providers | `account.accountLinking.trustedProviders` | +1 if explicit list |
| Database hooks | `databaseHooks.user.create.after` | +1 for audit logging |
| Session hooks | `databaseHooks.session.create.after` | +1 for login tracking |

## Two-Layer Auth Pattern (Next.js)

```
Layer 1: Middleware (Edge Runtime)
├── Fast cookie check: `better-auth.session_token`
├── Redirect to /sign-in if missing
├── Preserve callbackUrl in search params
└── Apply security headers

Layer 2: API Routes (Node Runtime)
├── requireAuth(): full session verification with DB
├── Returns 401 with error code if invalid
└── Provides session.user for route handlers
```

### Scoring

| Implementation | Score Bonus |
|---------------|------------|
| Both layers implemented | +2 to Authorization |
| Only middleware | 0 (default) |
| Only API routes | -1 to Authorization |
| Neither | -3 to Authorization |

## Session Cookie Checks

Better Auth uses `better-auth.session_token` cookie. Verify:
- Cookie name checked in middleware
- Token length validation (> 20 chars = valid format)
- No custom session parsing (let Better Auth handle it)

## Plugin Scoring Bonuses

| Plugin | Category Bonus |
|--------|---------------|
| `twoFactor()` | 2FA: +3 |
| `admin()` | Authorization: +1 |
| `passkey()` | Password Security: +1 |
| `organization()` | Authorization: +1 (multi-tenant) |

## Anti-Patterns (Score Penalties)

| Anti-Pattern | Penalty |
|-------------|---------|
| `process.env.GOOGLE_CLIENT_ID \|\| "disabled"` without `enabled` flag | -1 OAuth |
| Manual JWT parsing instead of Better Auth session | -2 Sessions |
| No `databaseHooks` for audit events | -1 Audit Logging |
| `trustedProviders: ["*"]` or missing | -1 OAuth |
| Session token in URL or localStorage | -3 Sessions |
| Password validation differs between sign-up and change | -2 Passwords |
