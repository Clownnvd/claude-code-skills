# Auth Generate Workflow

## Process

1. **Parse Request** — Extract: auth flow type (login, register, OAuth, password reset), framework (Better Auth/Clerk), requirements
2. **Load Criteria** — Read all 10 auth scoring categories from SKILL.md
3. **Map Criteria to Code**:

| Category | Code Pattern |
|----------|-------------|
| Session Management (15%) | Secure cookie config, httpOnly, sameSite, expiry, rotation |
| Password Security (12%) | bcrypt/argon2, min length 12, strength meter, breach check |
| OAuth & Social Login (10%) | State parameter, PKCE, token validation, account linking |
| Email Verification (8%) | Signed token, expiry, rate-limited resend |
| CSRF & Origin (12%) | Double-submit cookie, origin header check, SameSite |
| Security Headers (10%) | CSP, X-Frame-Options, HSTS, Referrer-Policy |
| Rate Limiting (12%) | Per-IP + per-user, exponential backoff, lockout after N failures |
| Audit Logging (8%) | Login/logout/failure events, IP, user-agent, timestamp |
| Authorization (8%) | RBAC middleware, route protection, permission checks |
| 2FA/MFA (5%) | TOTP setup, backup codes, recovery flow |

4. **Generate** — Write auth configuration + middleware + route handlers
5. **Self-Check** — Verify all 10 categories
6. **Output** — Code + compliance checklist + integration notes

## Quality Contract

- All 10 categories addressed with concrete code
- Score >= 90 (A-) if audited with auth scoring
- No plaintext passwords, no JWT without rotation, no missing CSRF
- Copy-paste ready with all imports
