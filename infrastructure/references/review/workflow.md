# Infrastructure Review Workflow

## Process

1. **Read** — Load target file(s): Dockerfile, docker-compose, CI config, env files
2. **Classify** — Which infrastructure categories apply:
   - Dockerfile → Containerization, Production Deploy, Security in Deployment
   - docker-compose.yml → Containerization, Environment Management, Infrastructure as Code
   - .github/workflows/*.yml → CI Pipeline, CD Pipeline, Security in Deployment
   - .env.* → Environment Management, Security in Deployment
   - monitoring config → Monitoring & Observability, Backup & Disaster Recovery
3. **Score** — Rate each applicable category 0-10
4. **Annotate** — Cite line numbers and issues
5. **Suggest** — Concrete fixes
6. **Summarize** — Score, priorities, quick wins

## Common Infrastructure Issues

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | Root user in container | Security in Deployment | CRITICAL |
| 2 | Secrets in Dockerfile/config | Environment Management | CRITICAL |
| 3 | No health check | Monitoring & Observability | HIGH |
| 4 | Single-stage Docker build | Containerization | HIGH |
| 5 | No CI pipeline | CI Pipeline | HIGH |
| 6 | No .env.example | Environment Management | MEDIUM |
| 7 | No structured logging | Monitoring & Observability | MEDIUM |
| 8 | No resource limits | Containerization | MEDIUM |
