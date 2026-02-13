# Infrastructure Review Workflow

## Process

1. **Read** — Load target file(s): Dockerfile, docker-compose, CI config, env files
2. **Classify** — Which infrastructure categories apply:
   - Dockerfile → Production Readiness, Container, Security Hardening
   - docker-compose.yml → Production Readiness, Container, Env Config, IaC
   - .github/workflows/*.yml → CI/CD Pipeline, Security
   - .env.* → Env Configuration, Security
   - monitoring config → Monitoring, Logging
3. **Score** — Rate each applicable category 0-10
4. **Annotate** — Cite line numbers and issues
5. **Suggest** — Concrete fixes
6. **Summarize** — Score, priorities, quick wins

## Common Infrastructure Issues

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | Root user in container | Security Hardening | CRITICAL |
| 2 | Secrets in Dockerfile/config | Env Configuration | CRITICAL |
| 3 | No health check | Monitoring | HIGH |
| 4 | Single-stage Docker build | Container Optimization | HIGH |
| 5 | No CI/CD pipeline | CI/CD Pipeline | HIGH |
| 6 | No .env.example | Env Configuration | MEDIUM |
| 7 | No structured logging | Logging | MEDIUM |
| 8 | No resource limits | Container Optimization | MEDIUM |
