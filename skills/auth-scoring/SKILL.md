---
name: auth-scoring
description: Audit authentication & authorization against 10 enterprise criteria (Better Auth, sessions, OAuth, RBAC, passwords, email verification, rate limiting, CSRF, security headers, audit logging). OWASP mapped.
---

# Auth Scoring

Score authentication & authorization implementation against 10 enterprise-grade criteria. Produce a weighted 0-100 score with letter grade, prioritized issues list, and actionable quick wins. Better Auth + Next.js App Router patterns.

## When to Use

- Before deploying auth flows to production
- Auditing an existing project's auth quality
- Reviewing auth changes in a pull request
- Checking OWASP authentication compliance (A07:2025)
- Quality gate: require B+ (87+) for production, A- (90+) for enterprise

## Scoring Categories

| # | Category | Weight | Criteria Reference |
|---|----------|--------|--------------------|
| 1 | Session Management | 15% | `criteria/sessions-passwords.md` |
| 2 | Password Security | 12% | `criteria/sessions-passwords.md` |
| 3 | OAuth & Social Login | 10% | `criteria/oauth-email.md` |
| 4 | Email Verification | 8% | `criteria/oauth-email.md` |
| 5 | CSRF & Origin Validation | 12% | `criteria/csrf-headers.md` |
| 6 | Security Headers | 10% | `criteria/csrf-headers.md` |
| 7 | Rate Limiting (auth routes) | 12% | `criteria/ratelimit-audit.md` |
| 8 | Audit Logging | 8% | `criteria/ratelimit-audit.md` |
| 9 | Authorization (RBAC/route protection) | 8% | `criteria/authz-2fa.md` |
| 10 | 2FA / MFA | 5% | `criteria/authz-2fa.md` |

## Audit Process

Load `references/scoring-workflow.md` for full steps.

1. **Gather** — Read auth config, middleware, session handling, OAuth setup, password validation, security headers
2. **Score** — Each category 0-10, starting at 5 (neutral baseline)
3. **Calculate** — Weighted sum -> 0-100 score -> letter grade
4. **Report** — Scorecard table + prioritized issues list + quick wins

## Grades

| Grade | Range | Production Ready? |
|-------|-------|-------------------|
| A+/A/A- | 90-100 | Enterprise-grade |
| B+/B | 83-89 | Production-ready |
| B- | 80-82 | Acceptable with caveats |
| C+/C | 73-79 | Needs work first |
| D/F | <73 | Not ready |

## Framework Adjustments

| Stack | Additional Reference |
|-------|---------------------|
| Better Auth + Next.js | `references/better-auth-patterns.md` — plugin config, session cookies, two-layer auth, databaseHooks |

## OWASP Authentication Mapping

| OWASP Risk | Covered By |
|---|---|
| A01: Broken Access Control | Authorization, CSRF |
| A02: Cryptographic Failures | Password Security, Session Management |
| A04: Insecure Design | OAuth, Email Verification |
| A05: Security Misconfiguration | Security Headers, Session Management |
| A07: Authentication Failures | Sessions, Passwords, OAuth, 2FA |

## Quick Reference — All Files

### Overview & Best Practices
- `references/overview.md` — Scoring system, grade scale, quality gates
- `references/best-practices.md` — Do/Don't for each auth category

### Workflow
- `references/scoring-workflow.md` — 6-step audit process, file gathering, scoring rubric

### Criteria (5 files covering 10 categories)
- `references/criteria/sessions-passwords.md` — Session Management + Password Security
- `references/criteria/oauth-email.md` — OAuth & Social Login + Email Verification
- `references/criteria/csrf-headers.md` — CSRF & Origin Validation + Security Headers
- `references/criteria/ratelimit-audit.md` — Rate Limiting (auth) + Audit Logging
- `references/criteria/authz-2fa.md` — Authorization (RBAC) + 2FA/MFA

### Framework Specific
- `references/better-auth-patterns.md` — Better Auth scoring adjustments, plugin checks

## Output Templates

Use `assets/templates/scorecard.md.template` as the output format when generating scorecards. Fill `{{VARIABLE}}` placeholders with actual values.
