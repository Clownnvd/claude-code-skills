---
name: security
description: Security quality system. 3 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score->fix until target). OWASP Top 10 mapped.
---

# Security Quality System

One skill, 3 modes. Score security posture, fix vulnerabilities, or run the full loop.

## Modes

| Mode | Use When | Workflow |
|------|----------|----------|
| **score** | Pre-launch audit, after adding routes/inputs, security review prep | Gather files -> score 10 categories -> weighted total -> grade + issues |
| **fix** | Scorecard has issues, score below target, CRITICAL/HIGH items found | Parse scorecard -> prioritize by severity*weight -> apply fixes -> verify |
| **loop** | Want hands-off score->fix cycle until target grade reached | Score -> fix -> re-score -> repeat (max 5 iterations, stop on plateau) |

## Mode: Score

Audit security design against 10 weighted categories (0-100 scale, A+ to F grade).

| # | Category | Weight | Key Signals | OWASP |
|---|----------|--------|-------------|-------|
| 1 | Input Validation & Sanitization | 15% | Zod at boundaries, XSS prevention, injection defense | A03 |
| 2 | Secrets & Environment Management | 12% | No hardcoded secrets, env sync, .env.example | A02, A05 |
| 3 | Dependency Security | 10% | npm audit clean, no known CVEs, lockfile integrity | A06 |
| 4 | Error Handling & Info Disclosure | 12% | No stack leak to client, safe error messages | A09 |
| 5 | Content Security Policy | 10% | CSP header, script-src, no unsafe-eval | A05 |
| 6 | Data Protection & PII | 10% | HTTPS enforced, PII minimization, no internal IDs leaked | A02 |
| 7 | Open Redirect & URL Validation | 8% | Redirect validation, `//` and `/\` blocked | A01 |
| 8 | Webhook & External API Security | 8% | Signature verification, idempotency, replay protection | A08 |
| 9 | Security Monitoring & Logging | 8% | Security events logged, request IDs, anomaly detection | A09 |
| 10 | Supply Chain & Build Security | 7% | Lockfile, CI/CD, poweredByHeader off, source maps | A06 |

### Grade Scale

| Grade | Score | Grade | Score | Grade | Score |
|-------|-------|-------|-------|-------|-------|
| A+ | 97-100 | B+ | 87-89 | C+ | 77-79 |
| A | 93-96 | B | 83-86 | C | 70-76 |
| A- | 90-92 | B- | 80-82 | D | 60-69 |
| | | | | F | <60 |

### Score Workflow
1. Gather files: proxy, API routes, validations, env config, package.json, CSP, webhooks
2. Score each category 0-10 using `references/scoring/criteria/` files
3. Calculate weighted total, assign grade
4. List issues with severity (CRITICAL/HIGH/MEDIUM/LOW) and affected files

## Mode: Fix

Parse scorecard, prioritize by severity * weight, apply fixes, verify.

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or data breach risk | Fix immediately -- blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next -- moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

### Fix Category -> Pattern Reference

| Scorecard Category | Fix Pattern File |
|-------------------|------------------|
| Input Validation, Secrets Management | `references/fix/fix-patterns/input-secrets.md` |
| Dependencies, Error Handling | `references/fix/fix-patterns/deps-errors.md` |
| CSP, Data Protection | `references/fix/fix-patterns/csp-data.md` |
| Redirects, Webhooks | `references/fix/fix-patterns/redirect-webhook.md` |
| Monitoring, Supply Chain | `references/fix/fix-patterns/monitoring-supply.md` |

### Fix Workflow
Load `references/fix/implementation-workflow.md` for 6-step process: parse -> prioritize -> fix -> verify -> re-score.

## Mode: Loop

Auto-iterate score -> fix until target grade reached.
- Default target: B+ (production), A- (enterprise)
- Max 5 iterations
- Stop on plateau (score unchanged after full fix cycle)
- Each iteration: full score -> prioritized fix -> re-score

## Quick Reference -- All Files

### Scoring
- `references/scoring/overview.md` -- Scoring system, output format, quality gates, OWASP mapping
- `references/scoring/best-practices.md` -- Do/Don't tables for all categories
- `references/scoring/scoring-workflow.md` -- Step-by-step audit process
- `references/scoring/criteria/input-secrets.md` -- Input Validation (15%) + Secrets (12%)
- `references/scoring/criteria/deps-errors.md` -- Dependencies (10%) + Error Handling (12%)
- `references/scoring/criteria/csp-data.md` -- CSP (10%) + Data Protection (10%)
- `references/scoring/criteria/redirect-webhook.md` -- Redirects (8%) + Webhooks (8%)
- `references/scoring/criteria/monitoring-supply.md` -- Monitoring (8%) + Supply Chain (7%)

### Fix
- `references/fix/overview.md` -- How fix works, priority order, score targets
- `references/fix/best-practices.md` -- Fix discipline, safe vs dangerous changes
- `references/fix/implementation-workflow.md` -- 6-step process, priority matrix
- `references/fix/verification.md` -- Post-fix checklist, re-scoring protocol, loop mode
- `references/fix/fix-patterns/input-secrets.md` -- Input validation, env sync
- `references/fix/fix-patterns/deps-errors.md` -- Dependency audit, error handling
- `references/fix/fix-patterns/csp-data.md` -- CSP headers, data protection
- `references/fix/fix-patterns/redirect-webhook.md` -- URL validation, webhook security
- `references/fix/fix-patterns/monitoring-supply.md` -- Logging, build security

## Output Templates
- Score: `assets/templates/scorecard.md.template`
- Fix: `assets/templates/fix-report.md.template`
