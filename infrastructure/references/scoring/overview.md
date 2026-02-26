# Infrastructure & Deployment Scoring — Overview

## Purpose
Objectively score infrastructure and deployment readiness for Next.js applications. Covers CI/CD pipelines, containerization, monitoring, backup, and third-party integration resilience.

## Scope Boundaries
- **This skill**: CI/CD, Docker, monitoring, backup, third-party integrations, IaC, deployment security
- **security-scoring**: Application-level security (input validation, CSP, CSRF, etc.)
- **scalability-scoring**: Runtime performance (bundle size, DB queries, caching, etc.)

## Pipeline Reference Model
```
Code Push → GitHub → CI (lint + test + build) → CD (deploy to staging) → Manual approve → Deploy to production
```

## Files to Audit (ordered by priority)
1. `.github/workflows/` — CI/CD pipeline definitions
2. `Dockerfile` / `docker-compose.yml` — Container configuration
3. `vercel.json` / `fly.toml` / `railway.json` — Platform deploy config
4. `package.json` — Scripts (build, test, lint, typecheck)
5. `src/lib/env.ts` — Environment variable validation
6. `.env.example` — Env var documentation
7. `src/app/api/health/` — Health check endpoints
8. `src/app/api/ready/` — Readiness probes
9. `src/lib/api/logger.ts` — Structured logging
10. `prisma/` — Migration strategy, backup config
11. External service integrations — Stripe, GitHub, Resend, etc.

## Output Format

```markdown
## Infrastructure & Deployment Scorecard — [Project Name]

| # | Category | Weight | Score | Weighted | Issues |
|---|----------|--------|-------|----------|--------|
| 1 | CI Pipeline | 15% | X/10 | Y | ... |
| ... | | | | | |
| **Total** | | **100%** | | **XX/100** | |
| **Grade** | | | | **B+** | |

### Issues List
| # | Severity | Category | File:Line | Issue | Fix |
|---|----------|----------|-----------|-------|-----|
| 1 | CRITICAL | ... | ... | ... | ... |
```

## Framework Adjustments

### Next.js on Vercel
- Automatic CI/CD via Vercel = +1 to CD Pipeline
- Preview deploys per PR = +1 to CD Pipeline
- Edge network = +1 to Monitoring (built-in analytics)
- Serverless = Containerization category weight redistributes to CI/CD and Monitoring

### Next.js Self-Hosted (Docker)
- Full containerization scoring applies
- Must manage own CD pipeline
- Must configure own monitoring stack
