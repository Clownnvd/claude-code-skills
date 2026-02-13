# Auth Review Workflow

## Process

1. **Read** — Load target auth file(s): config, middleware, route handlers, session management
2. **Classify** — Determine which of 10 auth categories apply to this file type:
   - Auth config → Sessions, Passwords, OAuth, 2FA
   - Middleware → CSRF, Headers, Rate Limiting, Authorization
   - Route handlers → All categories may apply
3. **Score** — Rate each applicable category 0-10
4. **Annotate** — For each deduction, cite exact line + explain + severity
5. **Suggest** — Concrete fix for each issue
6. **Summarize** — Score, top 3 priorities, quick wins

## Common Auth Issues (check these first)

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | Session not httpOnly | Session Management | CRITICAL |
| 2 | No CSRF protection | CSRF & Origin | CRITICAL |
| 3 | Weak password policy | Password Security | HIGH |
| 4 | No rate limit on login | Rate Limiting | HIGH |
| 5 | No audit logging | Audit Logging | MEDIUM |
| 6 | Missing security headers | Security Headers | MEDIUM |
| 7 | No account lockout | Rate Limiting | HIGH |
| 8 | RBAC not enforced | Authorization | HIGH |
