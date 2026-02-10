---
name: infra-scoring
description: Audit infrastructure & deployment against 10 enterprise criteria (CI/CD, containerization, monitoring, backup, third-party integrations). Next.js + Vercel/Docker patterns.
---

# Infrastructure & Deployment Scoring

Audit infrastructure and deployment readiness against 10 weighted categories. Produces scorecard with grade (A+ to F), per-category scores, issues list with severity, and fix recommendations.

## When to Use

- Before production launch — verify deployment posture
- After adding CI/CD pipelines, Docker configs, or monitoring
- When evaluating production readiness
- As input to `infra-fix` skill

## Scoring Categories

| # | Category | Weight | Key Signals |
|---|----------|--------|-------------|
| 1 | CI Pipeline (Lint + Test + Build) | 15% | GitHub Actions, lint/test/build gates, parallel jobs |
| 2 | CD Pipeline (Deploy to Staging) | 12% | Automated deploy on merge, staging environment, preview deploys |
| 3 | Production Deploy & Approval | 10% | Manual approval gate, rollback strategy, blue-green/canary |
| 4 | Containerization | 12% | Dockerfile, multi-stage build, .dockerignore, image size |
| 5 | Environment Management | 10% | Env var validation, secrets rotation, per-environment configs |
| 6 | Monitoring & Observability | 15% | Structured logging, health checks, alerting, APM, dashboards |
| 7 | Backup & Disaster Recovery | 10% | DB backups, backup testing, RTO/RPO targets, runbooks |
| 8 | Third-Party Integrations | 8% | Timeout, retry, circuit breaker, fallback, health checks |
| 9 | Infrastructure as Code | 4% | Terraform/Pulumi/CDK, version-controlled infra, reproducible |
| 10 | Security in Deployment | 4% | Image scanning, secret injection, network policies, SBOM |

## Audit Process

1. **Gather files**: CI/CD configs, Dockerfiles, monitoring setup, env management, backup scripts
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
- `references/criteria/ci-cd.md` — CI Pipeline (15%) + CD Pipeline (12%)
- `references/criteria/deploy-container.md` — Production Deploy (10%) + Containerization (12%)
- `references/criteria/env-monitoring.md` — Environment Mgmt (10%) + Monitoring (15%)
- `references/criteria/backup-integrations.md` — Backup/DR (10%) + Third-Party (8%)
- `references/criteria/iac-security.md` — IaC (4%) + Deployment Security (4%)

### Reference
- `references/overview.md` — Scoring system, output format, files to audit
- `references/scoring-workflow.md` — Step-by-step audit process
- `references/best-practices.md` — Do/Don't tables for all categories
