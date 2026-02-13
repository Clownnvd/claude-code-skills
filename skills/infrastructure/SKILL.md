---
name: infrastructure
description: Infrastructure quality system. 3 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score->fix until target). CI/CD, Docker, monitoring patterns.
license: Complete terms in LICENSE.txt
---

# Infrastructure Quality System

One skill, 3 modes. Score infrastructure and deployment readiness, fix issues, or run the full loop.

## Modes

| Mode | Trigger | What It Does |
|------|---------|--------------|
| **score** | "score my infrastructure", "audit infra" | 10-category audit -> scorecard with grade (A+ to F) |
| **fix** | "fix infra issues", provide a scorecard | Parse scorecard -> prioritize -> apply fixes -> verify |
| **loop** | "score and fix infra until B+", "infra loop" | Run score, then fix, then re-score until target grade reached |

## Mode: Score

Audit infrastructure and deployment against 10 weighted categories. Score 0-100 with letter grade and prioritized issues list.

Load `references/scoring/scoring-workflow.md` for the full audit process.

| # | Category | Weight | Criteria Reference |
|---|----------|--------|--------------------|
| 1 | CI Pipeline (Lint + Test + Build) | 15% | `scoring/criteria/ci-cd.md` |
| 2 | CD Pipeline (Deploy to Staging) | 12% | `scoring/criteria/ci-cd.md` |
| 3 | Production Deploy & Approval | 10% | `scoring/criteria/deploy-container.md` |
| 4 | Containerization | 12% | `scoring/criteria/deploy-container.md` |
| 5 | Environment Management | 10% | `scoring/criteria/env-monitoring.md` |
| 6 | Monitoring & Observability | 15% | `scoring/criteria/env-monitoring.md` |
| 7 | Backup & Disaster Recovery | 10% | `scoring/criteria/backup-integrations.md` |
| 8 | Third-Party Integrations | 8% | `scoring/criteria/backup-integrations.md` |
| 9 | Infrastructure as Code | 4% | `scoring/criteria/iac-security.md` |
| 10 | Security in Deployment | 4% | `scoring/criteria/iac-security.md` |

### Grades

| Grade | Score | Grade | Score | Grade | Score |
|-------|-------|-------|-------|-------|-------|
| A+ | 97-100 | B+ | 87-89 | C+ | 77-79 |
| A | 93-96 | B | 83-86 | C | 73-76 |
| A- | 90-92 | B- | 80-82 | D | 60-72 |
| | | | | F | <60 |

### Issue Severity

| Severity | Criteria | Action |
|----------|----------|--------|
| CRITICAL | Score 0-3 or security risk | Fix before deploy |
| HIGH | Score 4-5, weight >= 12% | Fix in current sprint |
| MEDIUM | Score 4-5, weight < 12% | Fix next sprint |
| LOW | Score 7-8 | Backlog |

## Mode: Fix

Take a scorecard and systematically implement all fixes. Prioritize by severity * weight.

Load `references/fix/implementation-workflow.md` for the full 6-step process.

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or security risk | Fix immediately -- blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next -- moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

### Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| CI Pipeline, CD Pipeline | `fix/fix-patterns/ci-cd.md` |
| Production Deploy, Containerization | `fix/fix-patterns/deploy-container.md` |
| Environment Management, Monitoring | `fix/fix-patterns/env-monitoring.md` |
| Backup/DR, Third-Party Integrations | `fix/fix-patterns/backup-integrations.md` |
| IaC, Deployment Security | `fix/fix-patterns/iac-security.md` |

### Verification

Load `references/fix/verification.md` for post-fix checklist, re-scoring protocol, and comparison template.

## Mode: Loop

Automated score-fix cycle. Runs score -> fix -> re-score until target grade is met.

1. **Score** the infrastructure (Mode: Score)
2. If grade < target, **fix** all CRITICAL + HIGH issues (Mode: Fix)
3. **Re-score** and compare
4. Repeat until target grade reached or no score improvement between iterations
   - Max 5 iterations
   - Stop on plateau (no score improvement between iterations)

Default target: **B+ (87+)**. Override with "loop until A-" or similar.

## Quick Reference -- All Files

### Scoring
- `references/scoring/overview.md` -- Scoring system, output format, files to audit
- `references/scoring/best-practices.md` -- Do/Don't tables for all categories
- `references/scoring/scoring-workflow.md` -- Step-by-step audit process
- `references/scoring/criteria/` -- 5 files covering 10 categories (ci-cd, deploy-container, env-monitoring, backup-integrations, iac-security)

### Fix
- `references/fix/overview.md` -- How fix works, priority order, score targets
- `references/fix/best-practices.md` -- Fix discipline, safe vs dangerous changes
- `references/fix/implementation-workflow.md` -- 6-step process, priority matrix
- `references/fix/verification.md` -- Post-fix checklist, re-scoring protocol
- `references/fix/fix-patterns/` -- 5 files covering 10 categories (ci-cd, deploy-container, env-monitoring, backup-integrations, iac-security)

## Output Templates

- `assets/templates/scorecard.md.template` -- Scorecard output (Mode: Score)
- `assets/templates/fix-report.md.template` -- Fix report output (Mode: Fix)

Fill `{{VARIABLE}}` placeholders with actual values.
