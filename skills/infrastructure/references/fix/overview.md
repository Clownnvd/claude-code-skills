# Infrastructure Fix — Overview

## Purpose

Systematically fix all issues identified by `infra-scoring`. Transforms scorecard issues into code changes, configs, and documentation.

## Priority Matrix

Fix order = severity * category weight. Higher weight categories move total score more.

| Weight Tier | Categories | Impact per +1 |
|------------|------------|---------------|
| High (15%) | CI Pipeline, Monitoring | +1.5 points |
| Medium (12%) | CD Pipeline, Containerization | +1.2 points |
| Standard (10%) | Production Deploy, Environment, Backup | +1.0 points |
| Low (8%) | Third-Party Integrations | +0.8 points |
| Minimal (4%) | IaC, Deployment Security | +0.4 points |

## Score Targets

| Context | Target | Grade |
|---------|--------|-------|
| MVP/Prototype | 70+ | C |
| Production launch | 87+ | B+ |
| Enterprise/regulated | 90+ | A- |

## Loop Constraints

- Max 5 iterations
- Stop on plateau (no score improvement between iterations)

## What This Skill Does NOT Fix

- Application-level security → use `security-fix`
- Database performance → use `db-fix`
- Caching strategy → use `caching-fix`
- API design → use `api-fix`

## Safe vs Dangerous Changes

### Safe (apply freely)
- Adding GitHub Actions workflows
- Creating health/readiness endpoints
- Adding .env.example documentation
- Adding .dockerignore
- Adding structured logging
- Creating backup documentation/runbooks

### Needs Testing
- Dockerfile changes (test build locally)
- CI pipeline changes (test on feature branch)
- Environment variable changes (verify in staging)
- Monitoring agent installation

### Dangerous (confirm with user)
- Production deploy process changes
- Secret rotation
- Database backup schedule changes
- Network/firewall rule changes
- Infrastructure provider changes
