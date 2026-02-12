---
name: auth
description: Auth quality system. 3 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score->fix until target). Better Auth + Next.js patterns.
---

# Auth Quality System

One skill, 3 modes. Score authentication & authorization quality, fix issues, or run the full loop.

## Modes

| Mode | Use When | Workflow |
|------|----------|---------|
| **score** | Audit auth quality | Read auth config -> Score 10 categories -> Scorecard |
| **fix** | Fix issues from scorecard | Parse -> Prioritize -> Fix -> Verify -> Re-score |
| **loop** | End-to-end cycle | Score -> Fix -> Re-score until target |

## Mode: Score

Audit authentication & authorization implementation across 10 weighted categories (0-100).

**When**: Before deploying auth flows, auditing existing quality, reviewing auth PR changes, checking OWASP A07 compliance.

**Steps**: Load `references/scoring/scoring-workflow.md`
1. Gather (auth config, middleware, sessions, OAuth, passwords, headers) -> 2. Score each category 0-10 (baseline 5) -> 3. Weighted sum -> grade -> 4. Scorecard + issues + quick wins

| # | Category | Weight | Criteria Reference |
|---|----------|--------|--------------------|
| 1 | Session Management | 15% | `scoring/criteria/sessions-passwords.md` |
| 2 | Password Security | 12% | `scoring/criteria/sessions-passwords.md` |
| 3 | OAuth & Social Login | 10% | `scoring/criteria/oauth-email.md` |
| 4 | Email Verification | 8% | `scoring/criteria/oauth-email.md` |
| 5 | CSRF & Origin Validation | 12% | `scoring/criteria/csrf-headers.md` |
| 6 | Security Headers | 10% | `scoring/criteria/csrf-headers.md` |
| 7 | Rate Limiting (auth routes) | 12% | `scoring/criteria/ratelimit-audit.md` |
| 8 | Audit Logging | 8% | `scoring/criteria/ratelimit-audit.md` |
| 9 | Authorization (RBAC/route protection) | 8% | `scoring/criteria/authz-2fa.md` |
| 10 | 2FA / MFA | 5% | `scoring/criteria/authz-2fa.md` |

**Anti-Bias**: Start at 5/10 baseline. Penalize missing checklist items. 9-10 requires evidence.

**Grades**: A+ (97-100), A (93-96), A- (90-92), B+ (87-89), B (83-86), B- (80-82), C+ (77-79), C (73-76), D (60-72), F (<60)

## Mode: Fix

Take scorecard output and implement all fixes. Prioritize by severity x weight.

**When**: After scoring, when auth is below target.

**Steps**: Load `references/fix/implementation-workflow.md`
1. Parse scorecard -> 2. Prioritize (Critical->High->Medium->Low) -> 3. Fix -> 4. Verify -> 5. Re-score

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or auth bypass | Fix immediately -- blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next -- moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Session Management, Password Security | `fix/fix-patterns/sessions-passwords.md` |
| OAuth & Social Login, Email Verification | `fix/fix-patterns/oauth-email.md` |
| CSRF & Origin Validation, Security Headers | `fix/fix-patterns/csrf-headers.md` |
| Rate Limiting, Audit Logging | `fix/fix-patterns/ratelimit-audit.md` |
| Authorization (RBAC), 2FA/MFA | `fix/fix-patterns/authz-2fa.md` |

## Mode: Loop

Auto-iterate score->fix until target. Max 5 iterations. Stop on plateau (delta=0 for 2 rounds).

**Score Targets**: B+ (87) production, A- (90) enterprise, A+ (97) gold standard.

## OWASP Authentication Mapping

| OWASP Risk | Covered By |
|---|---|
| A01: Broken Access Control | Authorization, CSRF |
| A02: Cryptographic Failures | Password Security, Session Management |
| A04: Insecure Design | OAuth, Email Verification |
| A05: Security Misconfiguration | Security Headers, Session Management |
| A07: Authentication Failures | Sessions, Passwords, OAuth, 2FA |

## Framework Adjustments

| Stack | Additional Reference |
|-------|---------------------|
| Better Auth + Next.js | `references/better-auth-patterns.md` -- plugin config, session cookies, two-layer auth, databaseHooks |

## Quick Reference -- All Files

### Scoring
- `references/scoring/overview.md` -- Scoring system, grade scale, quality gates
- `references/scoring/best-practices.md` -- Do/Don't for each auth category
- `references/scoring/scoring-workflow.md` -- 6-step audit process, file gathering, scoring rubric
- `references/scoring/criteria/` -- 5 files: sessions-passwords, oauth-email, csrf-headers, ratelimit-audit, authz-2fa
- `references/better-auth-patterns.md` -- Better Auth scoring adjustments, plugin checks

### Fix
- `references/fix/overview.md` -- How fix works, priority order, score targets
- `references/fix/best-practices.md` -- Fix discipline, safe vs dangerous changes, common mistakes
- `references/fix/implementation-workflow.md` -- 6-step process, priority matrix, which refs to load
- `references/fix/verification.md` -- Post-fix checklist, re-scoring protocol, loop mode
- `references/fix/fix-patterns/` -- 5 files: sessions-passwords, oauth-email, csrf-headers, ratelimit-audit, authz-2fa

## Output Templates

- Score: `assets/templates/scorecard.md.template`
- Fix: `assets/templates/fix-report.md.template`
Fill `{{VARIABLE}}` placeholders with actual values.
