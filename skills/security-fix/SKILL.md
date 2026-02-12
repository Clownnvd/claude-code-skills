---
name: security-fix
description: Take security-scoring feedback and implement all fixes systematically. Prioritize by severity, apply code changes, verify, and re-score. OWASP Top 10 mapped.
---

# Security Design Fix

Take a security-scoring scorecard and systematically implement all fixes. Prioritize by severity * weight, apply code changes, verify, and re-score.

## When to Use

- After running `security-scoring` and receiving a scorecard with issues
- When security scores below target (< B+ for production, < A- for enterprise)
- To systematically fix all CRITICAL -> HIGH -> MEDIUM -> LOW items
- Before deploying code that failed a security quality gate

## Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or data breach risk | Fix immediately — blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next — moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

## Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Input Validation, Secrets Management | `references/fix-patterns/input-secrets.md` |
| Dependencies, Error Handling | `references/fix-patterns/deps-errors.md` |
| CSP, Data Protection | `references/fix-patterns/csp-data.md` |
| Redirects, Webhooks | `references/fix-patterns/redirect-webhook.md` |
| Monitoring, Supply Chain | `references/fix-patterns/monitoring-supply.md` |

## Implementation

Load `references/implementation-workflow.md` for step-by-step process (parse -> prioritize -> fix -> verify -> re-score).

## Quick Reference

### Overview & Best Practices
- `references/overview.md` — How security-fix works, priority order, score targets
- `references/best-practices.md` — Fix discipline, safe vs dangerous changes

### Workflow
- `references/implementation-workflow.md` — 6-step process, priority matrix
- `references/verification.md` — Post-fix checklist, re-scoring protocol, loop mode

### Fix Patterns (5 files covering 10 categories)
- `references/fix-patterns/input-secrets.md` — Input validation, env sync
- `references/fix-patterns/deps-errors.md` — Dependency audit, error handling
- `references/fix-patterns/csp-data.md` — CSP headers, data protection
- `references/fix-patterns/redirect-webhook.md` — URL validation, webhook security
- `references/fix-patterns/monitoring-supply.md` — Logging, build security

## Output Templates

Use `assets/templates/fix-report.md.template` as the output format when generating fix reports. Fill `{{VARIABLE}}` placeholders with actual values.
