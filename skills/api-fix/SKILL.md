---
name: api-fix
description: Take api-scoring feedback (scorecard + issues list) and implement all fixes systematically. Prioritize by severity, apply code changes, verify, and re-score. Next.js App Router patterns.
---

# API Fix

Take an api-scoring scorecard and systematically implement all fixes. Prioritize by severity + weight, apply code changes, verify, and re-score.

## When to Use

- After running `api-scoring` and receiving a scorecard with issues
- When API scores below target (< B+ for production, < A- for enterprise)
- To systematically fix all CRITICAL -> HIGH -> MEDIUM -> LOW items
- Before deploying APIs that failed a quality gate

## Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or security hole | Fix immediately — blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next — moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

## Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Security, Auth & AuthZ | `references/fix-patterns/security-auth.md` |
| Input Validation, Error Handling | `references/fix-patterns/input-errors.md` |
| Rate Limiting, Response Design, Performance | `references/fix-patterns/ratelimit-response-perf.md` |
| Observability, Documentation, Testing | `references/fix-patterns/observability-docs-testing.md` |

## Implementation

Load `references/implementation-workflow.md` for step-by-step process (parse -> prioritize -> fix -> verify -> re-score).

## Quick Reference

### Overview & Best Practices
- `references/overview.md` — How api-fix works, priority order, score targets, integration with api-scoring
- `references/best-practices.md` — Fix discipline, safe vs dangerous changes, test guidelines, common mistakes

### Workflow
- `references/implementation-workflow.md` — 6-step process, priority matrix, which refs to load
- `references/verification.md` — Post-fix checklist, re-scoring protocol, comparison template, loop mode

### Fix Patterns (4 files covering 10 categories)
- `references/fix-patterns/security-auth.md` — CSP hardening, CORS, Content-Type, audit logging, BFLA, dep scanning
- `references/fix-patterns/input-errors.md` — Content-Type enforcement, error codes, consistent helpers, webhook responses
- `references/fix-patterns/ratelimit-response-perf.md` — Per-user rate limiting, query timeouts, pagination, caching headers
- `references/fix-patterns/observability-docs-testing.md` — Request logging, X-Request-Id, API docs, integration tests

## Output Templates

Use `assets/templates/fix-report.md.template` as the output format when generating fix reports. Fill `{{VARIABLE}}` placeholders with actual values.
