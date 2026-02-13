# Infrastructure Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| CI Pipeline (15%) | Pipeline test | Lint, test, build stages all run, failure stops pipeline |
| CD Pipeline (12%) | Pipeline test | Auto-deploy to staging on merge, smoke tests pass |
| Production Deploy & Approval (10%) | Build test | Approval gate exists, rollback works, health check wait |
| Containerization (12%) | Image test | Non-root user, minimal size, multi-stage build, correct layers |
| Environment Management (10%) | Unit | All required env vars validated at startup, .env.example present |
| Monitoring & Observability (15%) | Integration | Health endpoint 200, Sentry captures, structured logs |
| Backup & Disaster Recovery (10%) | Integration | Backup runs, restore tested, RTO/RPO documented |
| Third-Party Integrations (8%) | Integration | Webhook retry, circuit breaker, timeout handling |
| Infrastructure as Code (4%) | Syntax | Terraform/compose validates without errors |
| Security in Deployment (4%) | Image scan | No critical CVEs, no root processes, secrets in vault |

2. **Generate Test Files**:
   - `__tests__/infra/docker.test.ts` — Dockerfile build + security
   - `__tests__/infra/health.test.ts` — Health endpoint
   - `__tests__/infra/env.test.ts` — Env validation
   - `__tests__/infra/ci.test.ts` — CI pipeline validation

3. **Output** — Test files + coverage matrix
