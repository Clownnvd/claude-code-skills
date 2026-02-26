# Production Deploy (10%) + Containerization (12%)

## Category 3: Production Deploy & Approval — 10%

Score 0-10 based on how many criteria are met:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Manual approval gate | Production deploy requires explicit human approval |
| 2 | Rollback strategy | Documented or automated rollback to previous version |
| 3 | Deploy checklist | Pre-deploy checklist (DB migrations, env vars, feature flags) |
| 4 | Blue-green or canary | Traffic shifting strategy (not big-bang to 100%) |
| 5 | Low-traffic window | Deploy during off-peak hours or automated scheduling |
| 6 | Post-deploy verification | Smoke tests or health checks after production deploy |
| 7 | Deploy audit trail | Who deployed what, when — logged and searchable |
| 8 | Hotfix process | Emergency deploy path that bypasses normal queue |
| 9 | Feature flags | Can toggle features without redeploy |
| 10 | Incident response plan | Documented steps for failed production deploy |

### Scoring Guide

| Score | Criteria Met |
|-------|-------------|
| 10 | All 10 criteria met |
| 8-9 | Manual approval + rollback + post-deploy checks working |
| 6-7 | Basic approval gate, some verification |
| 4-5 | Deploy process exists but minimal safety |
| 2-3 | Ad-hoc manual deploys with some structure |
| 0-1 | No deploy process or fully uncontrolled |

### Platform Adjustments

**Vercel**: Instant rollback via dashboard = +1 to criterion 2. Git-based deploys = audit trail (criterion 7). Preview → Production promotion = approval gate (criterion 1).

---

## Category 4: Containerization — 12%

Score 0-10 based on how many criteria are met:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Dockerfile exists | Application has a Dockerfile for container builds |
| 2 | Multi-stage build | Separate build and runtime stages (smaller final image) |
| 3 | .dockerignore | Excludes node_modules, .git, .env, test files |
| 4 | Pinned base image | Specific version tag (not `latest`) |
| 5 | Non-root user | Container runs as non-root user (USER directive) |
| 6 | Health check | HEALTHCHECK instruction in Dockerfile |
| 7 | Small image size | Final image < 500MB (Alpine or distroless base) |
| 8 | Layer caching | Package install before code copy for cache efficiency |
| 9 | docker-compose | Multi-container setup for local dev (app + DB + cache) |
| 10 | Security scanning | Container image scanned for CVEs (Trivy, Snyk) |

### Scoring Guide

| Score | Criteria Met |
|-------|-------------|
| 10 | All 10 criteria met |
| 8-9 | Multi-stage, non-root, pinned, health check |
| 6-7 | Dockerfile works but missing security/optimization |
| 4-5 | Basic Dockerfile, single stage |
| 2-3 | Dockerfile exists but poorly configured |
| 0-1 | No Dockerfile |

### Platform Adjustments

**Vercel/Serverless**: Containerization category weight (12%) redistributes:
- +6% to CI Pipeline (becomes 21%)
- +6% to Monitoring (becomes 21%)

Score the category as N/A and redistribute weight. Do NOT penalize serverless projects for missing Docker.

### Common Deductions

- No Dockerfile in serverless project → N/A (redistribute weight)
- Single-stage build with dev deps in prod → -2
- Running as root → -1
- No .dockerignore → -1
- Using `latest` tag → -1
- Image > 1GB → -2
