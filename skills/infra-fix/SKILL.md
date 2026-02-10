---
name: infra-fix
description: Take infra-scoring feedback and implement all fixes systematically. Prioritize by severity, apply code changes, verify, and re-score.
---

# Infrastructure & Deployment Fix

Take an infra-scoring scorecard and systematically implement all fixes. Prioritize by severity * weight, apply code changes, verify, and re-score.

## When to Use

- After running `infra-scoring` and receiving a scorecard with issues
- When infra scores below target (< B+ for production, < A- for enterprise)
- To systematically fix all CRITICAL -> HIGH -> MEDIUM -> LOW items
- Before deploying code that failed an infrastructure quality gate

## Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or security risk | Fix immediately — blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next — moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

## Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| CI Pipeline, CD Pipeline | `references/fix-patterns/ci-cd.md` |
| Production Deploy, Containerization | `references/fix-patterns/deploy-container.md` |
| Environment Management, Monitoring | `references/fix-patterns/env-monitoring.md` |
| Backup/DR, Third-Party Integrations | `references/fix-patterns/backup-integrations.md` |
| IaC, Deployment Security | `references/fix-patterns/iac-security.md` |

## Implementation

Load `references/implementation-workflow.md` for step-by-step process (parse -> prioritize -> fix -> verify -> re-score).

## Quick Reference

### Overview & Best Practices
- `references/overview.md` — How infra-fix works, priority order, score targets
- `references/best-practices.md` — Fix discipline, safe vs dangerous changes

### Workflow
- `references/implementation-workflow.md` — 6-step process, priority matrix
- `references/verification.md` — Post-fix checklist, re-scoring protocol

### Fix Patterns (5 files covering 10 categories)
- `references/fix-patterns/ci-cd.md` — CI pipeline setup, CD automation
- `references/fix-patterns/deploy-container.md` — Production deploy, Docker optimization
- `references/fix-patterns/env-monitoring.md` — Env validation, monitoring stack
- `references/fix-patterns/backup-integrations.md` — Backup strategy, integration resilience
- `references/fix-patterns/iac-security.md` — IaC setup, deployment security
