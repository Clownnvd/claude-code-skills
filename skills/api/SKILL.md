---
name: api
description: API quality system. 3 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score->fix until target). OWASP API Top 10 mapped.
---

# API Quality System

One skill, 3 modes. Score REST/HTTP API quality, fix issues, or run the full loop.

## Modes

| Mode | Use When | Workflow |
|------|----------|---------|
| **score** | Audit API quality | Read routes -> Score 10 categories -> Scorecard |
| **fix** | Fix issues from scorecard | Parse -> Prioritize -> Fix -> Verify -> Re-score |
| **loop** | End-to-end cycle | Score -> Fix -> Re-score until target |

## Mode: Score

Audit any REST/HTTP API codebase across 10 weighted categories (0-100).

**When**: Before deploying API routes, auditing existing quality, reviewing PR changes, checking OWASP compliance.

**Steps**: Load `references/scoring/scoring-workflow.md`
1. Gather (routes, auth, env, tests) -> 2. Score each category 0-10 (baseline 5) -> 3. Weighted sum -> grade -> 4. Scorecard + issues + quick wins

| # | Category | Weight | Criteria Reference |
|---|----------|--------|--------------------|
| 1 | Security | 20% | `scoring/criteria/security-auth.md` |
| 2 | Auth & AuthZ | 15% | `scoring/criteria/security-auth.md` |
| 3 | Input Validation | 12% | `scoring/criteria/input-errors.md` |
| 4 | Error Handling | 10% | `scoring/criteria/input-errors.md` |
| 5 | Rate Limiting | 10% | `scoring/criteria/ratelimit-response-perf.md` |
| 6 | Response Design | 8% | `scoring/criteria/ratelimit-response-perf.md` |
| 7 | Performance | 8% | `scoring/criteria/ratelimit-response-perf.md` |
| 8 | Observability | 7% | `scoring/criteria/observability-docs-testing.md` |
| 9 | Documentation & DX | 5% | `scoring/criteria/observability-docs-testing.md` |
| 10 | Testing | 5% | `scoring/criteria/observability-docs-testing.md` |

**Anti-Bias**: Start at 5/10 baseline. Penalize missing checklist items. 9-10 requires evidence.

**Grades**: A+ (97-100), A (93-96), A- (90-92), B+ (87-89), B (83-86), B- (80-82), C+ (77-79), C (73-76), D (60-72), F (<60)

## Mode: Fix

Take scorecard output and implement all fixes. Prioritize by severity x weight.

**When**: After scoring, when API is below target.

**Steps**: Load `references/fix/implementation-workflow.md`
1. Parse scorecard -> 2. Prioritize (Critical->High->Medium->Low) -> 3. Fix -> 4. Verify -> 5. Re-score

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or security hole | Fix immediately -- blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next -- moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Security, Auth & AuthZ | `fix/fix-patterns/security-auth.md` |
| Input Validation, Error Handling | `fix/fix-patterns/input-errors.md` |
| Rate Limiting, Response Design, Performance | `fix/fix-patterns/ratelimit-response-perf.md` |
| Observability, Documentation, Testing | `fix/fix-patterns/observability-docs-testing.md` |

## Mode: Loop

Auto-iterate score->fix until target. Max 5 iterations. Stop on plateau (delta=0 for 2 rounds).

**Score Targets**: B+ (87) production, A- (90) enterprise, A+ (97) gold standard.

## OWASP API Top 10 Cross-Reference

| OWASP Risk | Covered By |
|---|---|
| API1: BOLA | Auth & AuthZ |
| API2: Broken Auth | Security, Auth & AuthZ |
| API3: BOPLA | Auth & AuthZ, Input Validation |
| API4: Resource Consumption | Rate Limiting, Performance |
| API5: BFLA | Auth & AuthZ |
| API6: Sensitive Flows | Security, Rate Limiting |
| API7: SSRF | Security, Input Validation |
| API8: Misconfiguration | Security, Error Handling, Observability |
| API9: Inventory Mgmt | Observability, Documentation |
| API10: Unsafe API Consumption | Rate Limiting, Input Validation |

## Framework Adjustments

| Stack | Additional Reference |
|-------|---------------------|
| Next.js App Router | `references/nextjs-patterns.md` -- two-layer auth, security headers, webhook patterns, response helpers |

## Quick Reference -- All Files

### Scoring
- `references/scoring/overview.md` -- Scoring system, grade scale, quality gates, OWASP mapping
- `references/scoring/best-practices.md` -- Do/Don't for security, validation, errors, rate limiting, auth, observability, testing
- `references/scoring/scoring-workflow.md` -- 6-step audit process, category mapping, issue format
- `references/scoring/criteria/` -- 4 files: security-auth, input-errors, ratelimit-response-perf, observability-docs-testing
- `references/nextjs-patterns.md` -- Next.js App Router scoring adjustments, anti-pattern penalties

### Fix
- `references/fix/overview.md` -- How fix works, priority order, score targets, integration with scoring
- `references/fix/best-practices.md` -- Fix discipline, safe vs dangerous changes, test guidelines, common mistakes
- `references/fix/implementation-workflow.md` -- 6-step process, priority matrix, which refs to load
- `references/fix/verification.md` -- Post-fix checklist, re-scoring protocol, comparison template, loop mode
- `references/fix/fix-patterns/` -- 4 files: security-auth, input-errors, ratelimit-response-perf, observability-docs-testing

## Output Templates

- Score: `assets/templates/scorecard.md.template`
- Fix: `assets/templates/fix-report.md.template`
Fill `{{VARIABLE}}` placeholders with actual values.
