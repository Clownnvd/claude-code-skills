---
name: auth-fix
description: Take auth-scoring feedback (scorecard + issues list) and implement all fixes systematically. Prioritize by severity, apply code changes, verify, and re-score. Better Auth + Next.js patterns.
---

# Auth Fix

Take an auth-scoring scorecard and systematically implement all fixes. Prioritize by severity + weight, apply code changes, verify, and re-score.

## When to Use

- After running `auth-scoring` and receiving a scorecard with issues
- When auth scores below target (< B+ for production, < A- for enterprise)
- To systematically fix all CRITICAL -> HIGH -> MEDIUM -> LOW items
- Before deploying auth flows that failed a quality gate

## Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or auth bypass | Fix immediately — blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next — moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

## Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Session Management, Password Security | `references/fix-patterns/sessions-passwords.md` |
| OAuth & Social Login, Email Verification | `references/fix-patterns/oauth-email.md` |
| CSRF & Origin Validation, Security Headers | `references/fix-patterns/csrf-headers.md` |
| Rate Limiting, Audit Logging | `references/fix-patterns/ratelimit-audit.md` |
| Authorization (RBAC), 2FA/MFA | `references/fix-patterns/authz-2fa.md` |

## Implementation

Load `references/implementation-workflow.md` for step-by-step process (parse -> prioritize -> fix -> verify -> re-score).

## Quick Reference

### Overview & Best Practices
- `references/overview.md` — How auth-fix works, priority order, score targets
- `references/best-practices.md` — Fix discipline, safe vs dangerous changes, common mistakes

### Workflow
- `references/implementation-workflow.md` — 6-step process, priority matrix, which refs to load
- `references/verification.md` — Post-fix checklist, re-scoring protocol, loop mode

### Fix Patterns (5 files covering 10 categories)
- `references/fix-patterns/sessions-passwords.md` — Cookie config, session expiry, password hashing, validation schema
- `references/fix-patterns/oauth-email.md` — Provider config, account linking, verification flow, email templates
- `references/fix-patterns/csrf-headers.md` — Origin validation, CSP hardening, HSTS, Permissions-Policy
- `references/fix-patterns/ratelimit-audit.md` — Strict auth rate limits, distributed store, structured audit logging
- `references/fix-patterns/authz-2fa.md` — Two-layer auth, requireAuth(), RBAC, 2FA plugin setup
