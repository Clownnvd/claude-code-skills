# Security Design Scoring — Overview

## Purpose
Objectively score application security design in Next.js App Router applications. Covers OWASP Top 10 areas NOT handled by auth-scoring (which covers auth flows, sessions, CSRF, rate limiting).

## Scope Boundaries
- **This skill**: Input validation, secrets, dependencies, info disclosure, CSP, data protection, redirects, webhooks, monitoring, supply chain
- **auth-scoring**: Sessions, passwords, OAuth, CSRF, security headers, rate limiting, audit logging, RBAC, 2FA
- **api-scoring**: API design, response format, performance, testing

## Scoring System
- 10 categories, each scored 0-10
- Weighted sum produces 0-100 total
- Each deduction must cite specific file + line + reason

## Grade Scale

| Grade | Score | Deploy? |
|-------|-------|---------|
| A+/A/A- | 90-100 | Yes — enterprise-grade |
| B+/B/B- | 80-89 | Yes — production-ready |
| C+/C | 70-79 | Conditional — fix HIGH items first |
| D | 60-69 | No — major issues |
| F | <60 | No — critical issues |

## OWASP Top 10 (2025) Mapping

| OWASP | Category in This Skill |
|-------|----------------------|
| A01: Broken Access Control | Open Redirect (7), Data Protection (6) |
| A02: Cryptographic Failures | Secrets (2), Data Protection (6) |
| A03: Injection | Input Validation (1) |
| A04: Insecure Design | Webhook Security (8), Supply Chain (10) |
| A05: Security Misconfiguration | CSP (5), Secrets (2) |
| A06: Vulnerable Components | Dependencies (3), Supply Chain (10) |
| A07: Auth Failures | (covered by auth-scoring) |
| A08: Software/Data Integrity | Webhook Security (8), Supply Chain (10) |
| A09: Logging/Monitoring | Error Handling (4), Monitoring (9) |
| A10: SSRF | Input Validation (1), Redirect (7) |

## Output Format

```markdown
## Security Design Scorecard — [Project Name]

| # | Category | Weight | Score | Weighted | Issues |
|---|----------|--------|-------|----------|--------|
| 1 | Input Validation | 15% | X/10 | Y | ... |
| ... | | | | | |
| **Total** | | **100%** | | **XX/100** | |
| **Grade** | | | | **B+** | |

### Issues List
| # | Severity | Category | File:Line | Issue | Fix |
|---|----------|----------|-----------|-------|-----|
| 1 | CRITICAL | ... | ... | ... | ... |
```

## Files to Audit (ordered by priority)

1. `src/lib/validations/**` — Zod schemas, input validation
2. `.env.example` + `src/lib/env.ts` — secrets, env sync
3. `package.json` + `pnpm-lock.yaml` — dependency audit
4. `src/lib/api/response.ts` — error response shapes
5. `src/middleware.ts` — CSP, security headers, redirects
6. `src/app/api/webhooks/**` — webhook verification
7. `src/lib/api/logger.ts` — security logging
8. `src/app/api/**/route.ts` — input handling per route
9. `next.config.js` — poweredByHeader, headers, source maps
10. `prisma/schema.prisma` — data model, sensitive fields
