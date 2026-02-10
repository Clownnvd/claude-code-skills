# Auth Fix Best Practices

## Fix Discipline

| Rule | Why |
|------|-----|
| One fix per commit (or grouped by category) | Easy to revert if something breaks |
| Read file before editing | Tool requirement; also ensures context |
| Run `tsc --noEmit` after each file change | Catch type errors immediately |
| Never weaken existing security to fix another issue | Layered security must be additive |
| Test the happy path AND the attack path | A fix that blocks attacks but breaks login is worse |

## Safe vs Dangerous Changes

### Safe (low risk of breakage)
- Adding security headers (middleware)
- Tightening rate limits (lower threshold)
- Adding audit log entries (new code, no changes to existing)
- Adding CSRF origin validation (middleware addition)
- Adding `httpOnly`, `secure`, `sameSite` to cookies
- Adding password strength validation (sign-up only initially)

### Dangerous (verify carefully)
- Changing session expiry (may log out all users)
- Changing cookie name (invalidates existing sessions)
- Adding email verification requirement (blocks unverified users)
- Changing OAuth callback URLs (breaks OAuth flow)
- Adding 2FA requirement (locks out users without 2FA setup)
- Modifying RBAC rules (may revoke access unexpectedly)

## Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Adding `sameSite: "strict"` for OAuth | Use `sameSite: "lax"` — strict blocks OAuth redirects |
| Rate limiting by user ID only | Rate limit by IP for unauthenticated routes |
| Hardcoding allowed origins | Use `env.BETTER_AUTH_URL` or `env.NEXT_PUBLIC_APP_URL` |
| Adding CSP that blocks inline styles | Tailwind uses inline styles; use `unsafe-inline` for style-src or nonce |
| Blocking all requests without Origin header | Some legitimate requests (bookmarks, typed URLs) lack Origin |
| Silent catch in auth middleware | Always log + return proper error response |

## Fix Order Within a Category

1. **Config changes** (Better Auth options) — safest, most impact
2. **Middleware additions** (headers, checks) — moderate impact
3. **API route changes** (validation, response codes) — test-heavy
4. **Schema/database changes** (new columns, migrations) — most risk

## When NOT to Fix

- Score 9-10: Diminishing returns; document as "accepted risk"
- Requires new infrastructure (Redis, email provider): Flag as "requires setup"
- Would break existing users: Flag as "migration needed", provide migration plan
- Better Auth doesn't support it natively: Flag as "framework limitation"
