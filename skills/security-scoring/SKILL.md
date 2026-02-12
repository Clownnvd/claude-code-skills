---
name: security-scoring
description: Audit application security design against 10 enterprise criteria (input validation, secrets, dependencies, info disclosure, CSP, data protection, redirects, webhooks, monitoring, supply chain). OWASP Top 10 mapped.
---

# Security Design Scoring

Audit application security design against 10 weighted categories. Produces scorecard with grade (A+ to F), per-category scores, issues list with severity, and fix recommendations. Complements auth-scoring (auth flows) and api-scoring (API design).

## When to Use

- Before production launch — verify security posture
- After adding new API routes or user input handling
- During security review or penetration testing prep
- As input to `security-fix` skill

## Scoring Categories

| # | Category | Weight | Key Signals | OWASP |
|---|----------|--------|-------------|-------|
| 1 | Input Validation & Sanitization | 15% | Zod at boundaries, XSS prevention, injection defense | A03 |
| 2 | Secrets & Environment Management | 12% | No hardcoded secrets, env sync, .env.example | A02, A05 |
| 3 | Dependency Security | 10% | npm audit clean, no known CVEs, lockfile integrity | A06 |
| 4 | Error Handling & Info Disclosure | 12% | No stack leak to client, safe error messages, structured logging | A09 |
| 5 | Content Security Policy | 10% | CSP header, script-src, frame-ancestors, no unsafe-eval | A05 |
| 6 | Data Protection & PII | 10% | HTTPS enforced, PII minimization, Prisma select, no internal IDs leaked | A02 |
| 7 | Open Redirect & URL Validation | 8% | Redirect validation, `//` and `/\` blocked, URL parsing | A01 |
| 8 | Webhook & External API Security | 8% | Signature verification, idempotency, replay protection, timeout | A08 |
| 9 | Security Monitoring & Logging | 8% | Security events logged, request IDs, anomaly detection | A09 |
| 10 | Supply Chain & Build Security | 7% | Lockfile, CI/CD, poweredByHeader off, source maps | A06 |

## Audit Process

1. **Gather files**: proxy, API routes, validations, env config, package.json, CSP, webhook handlers
2. **Score each category** 0-10 using criteria in `references/criteria/` files
3. **Calculate weighted total** (0-100)
4. **Assign grade** using scale below
5. **List issues** with severity (CRITICAL/HIGH/MEDIUM/LOW) and affected files

## Grade Scale

| Grade | Score | Meaning |
|-------|-------|---------|
| A+ | 97-100 | Exceptional |
| A | 93-96 | Enterprise-grade |
| A- | 90-92 | Near-enterprise |
| B+ | 87-89 | Professional |
| B | 83-86 | Production-ready |
| B- | 80-82 | Acceptable |
| C+ | 77-79 | Needs improvement |
| C | 70-76 | Minimum viable |
| D | 60-69 | Below standard |
| F | <60 | Critical issues |

## Quick Reference

### Criteria (5 files covering 10 categories)
- `references/criteria/input-secrets.md` — Input Validation (15%) + Secrets Management (12%)
- `references/criteria/deps-errors.md` — Dependencies (10%) + Error Handling (12%)
- `references/criteria/csp-data.md` — CSP (10%) + Data Protection (10%)
- `references/criteria/redirect-webhook.md` — Redirects (8%) + Webhooks (8%)
- `references/criteria/monitoring-supply.md` — Monitoring (8%) + Supply Chain (7%)

### Reference
- `references/overview.md` — Scoring system, output format, quality gates, OWASP mapping
- `references/scoring-workflow.md` — Step-by-step audit process
- `references/best-practices.md` — Do/Don't tables for all categories

## Output Templates

Use `assets/templates/scorecard.md.template` as the output format when generating scorecards. Fill `{{VARIABLE}}` placeholders with actual values.
