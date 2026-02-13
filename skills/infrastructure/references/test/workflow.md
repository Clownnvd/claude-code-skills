# Infrastructure Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| Production Readiness (10%) | Build test | Docker build succeeds, output is standalone |
| Container (12%) | Image test | Non-root user, minimal size, correct layers |
| CI/CD (10%) | Pipeline test | All stages run, failure stops pipeline |
| Env Configuration (10%) | Unit | All required env vars validated at startup |
| Monitoring (15%) | Integration | Health endpoint responds 200, Sentry captures errors |
| Logging (8%) | Unit | Structured logs output correct JSON format |
| CDN (8%) | Integration | Static assets served with correct headers |
| SSL & DNS (4%) | Integration | HTTPS redirect works, HSTS header present |
| IaC (4%) | Syntax | Terraform/compose validates without errors |
| Security (4%) | Image scan | No critical CVEs, no root processes |

2. **Generate Test Files**:
   - `__tests__/infra/docker.test.ts` — Dockerfile build + security
   - `__tests__/infra/health.test.ts` — Health endpoint
   - `__tests__/infra/env.test.ts` — Env validation
   - `__tests__/infra/ci.test.ts` — CI pipeline validation

3. **Output** — Test files + coverage matrix
