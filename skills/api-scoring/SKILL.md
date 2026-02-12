---
name: api-scoring
description: Audit REST/HTTP APIs against 10 enterprise criteria (security, auth, input validation, error handling, rate limiting, response design, performance, observability, docs, testing). OWASP API Top 10 mapped.
---

# API Scoring

Score any REST/HTTP API codebase against 10 enterprise-grade criteria. Produce a weighted 0-100 score with letter grade, prioritized issues list, and actionable quick wins.

## When to Use

- Before deploying API routes to production
- Auditing an existing project's API quality
- Reviewing API changes in a pull request
- Checking OWASP API Top 10 compliance
- Quality gate: require B+ (87+) for production, A- (90+) for enterprise/public API

## Scoring Categories

| # | Category | Weight | Criteria Reference |
|---|----------|--------|--------------------|
| 1 | Security | 20% | `criteria/security-auth.md` |
| 2 | Auth & AuthZ | 15% | `criteria/security-auth.md` |
| 3 | Input Validation | 12% | `criteria/input-errors.md` |
| 4 | Error Handling | 10% | `criteria/input-errors.md` |
| 5 | Rate Limiting | 10% | `criteria/ratelimit-response-perf.md` |
| 6 | Response Design | 8% | `criteria/ratelimit-response-perf.md` |
| 7 | Performance | 8% | `criteria/ratelimit-response-perf.md` |
| 8 | Observability | 7% | `criteria/observability-docs-testing.md` |
| 9 | Documentation & DX | 5% | `criteria/observability-docs-testing.md` |
| 10 | Testing | 5% | `criteria/observability-docs-testing.md` |

## Audit Process

Load `references/scoring-workflow.md` for full steps.

1. **Gather** — Read API routes, proxy, auth config, env files, tests
2. **Score** — Each category 0-10, starting at 5 (neutral baseline)
3. **Calculate** — Weighted sum → 0-100 score → letter grade
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
| Next.js App Router | `references/nextjs-patterns.md` — two-layer auth, security headers, webhook patterns, response helpers |

## Issue Severity

| Severity | Criteria | Action |
|----------|----------|--------|
| CRITICAL | Score 0-3 or security hole | Fix before deploy |
| HIGH | Score 4-5, weight >= 12% | Fix in current sprint |
| MEDIUM | Score 4-5, weight < 12% | Fix next sprint |
| LOW | Score 7-8 | Backlog |

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

## Quick Reference — All Files

### Overview & Best Practices
- `references/overview.md` — Scoring system, grade scale, quality gates, OWASP mapping
- `references/best-practices.md` — Do/Don't for security, validation, errors, rate limiting, auth, observability, testing

### Workflow
- `references/scoring-workflow.md` — 6-step audit process, category mapping, issue format

### Criteria (4 files covering 10 categories)
- `references/criteria/security-auth.md` — Security + Auth & AuthZ
- `references/criteria/input-errors.md` — Input Validation + Error Handling
- `references/criteria/ratelimit-response-perf.md` — Rate Limiting + Response Design + Performance
- `references/criteria/observability-docs-testing.md` — Observability + Documentation & DX + Testing

### Framework Specific
- `references/nextjs-patterns.md` — Next.js App Router scoring adjustments, anti-pattern penalties

## Output Templates

Use `assets/templates/scorecard.md.template` as the output format when generating scorecards. Fill `{{VARIABLE}}` placeholders with actual values.
