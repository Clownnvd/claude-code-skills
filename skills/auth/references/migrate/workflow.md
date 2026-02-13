# Auth Migrate Workflow

## Process

1. **Detect Versions** — Identify current/target versions of auth library (Better Auth, Clerk), Next.js, session store
2. **Map Breaking Changes**:

## Auth Library Migration Map

| From → To | Category Affected | Breaking Change | Migration Action |
|-----------|------------------|-----------------|-----------------|
| Clerk v5 → v6 | Session Management | `auth()` API change | Update all `auth()` call sites |
| Clerk v5 → v6 | Auth & AuthZ | Middleware config | Migrate to proxy.ts pattern |
| Better Auth 0.x → 1.x | Session Management | Session cookie format | Re-issue sessions on upgrade |
| Better Auth | OAuth | Provider config changes | Update OAuth plugin config |
| Next.js 15 → 16 | CSRF | Proxy replaces middleware | Move CSRF check to proxy |
| Next.js 15 → 16 | Security Headers | Header API changes | Update header configuration |

3. **Apply Migrations** — Read affected files, apply changes, preserve auth security
4. **Verify** — TypeScript check, test auth flows manually, verify session persistence
5. **Re-score** — Ensure no auth category regressed

## Safety Rules

- NEVER weaken auth during migration (no removing CSRF, no loosening session config)
- Test login/logout/register flows after every migration step
- Keep session rotation working throughout migration
- Verify rate limiting still active after middleware changes
