# Infrastructure Generate Workflow

## Process

1. **Parse Request** — Extract: component type (Dockerfile, CI/CD, env config, monitoring), target platform
2. **Load Criteria** — Read all 10 infrastructure scoring categories from SKILL.md
3. **Map Criteria to Code**:

| Category | Code Pattern |
|----------|-------------|
| CI Pipeline — Lint + Test + Build (15%) | GitHub Actions, lint→test→build stages, parallel jobs, caching |
| CD Pipeline — Deploy to Staging (12%) | Auto-deploy on merge, staging env, smoke tests, rollback |
| Production Deploy & Approval (10%) | Manual approval gate, blue-green/canary, health check wait |
| Containerization (12%) | Multi-stage Docker, Alpine base, non-root user, layer caching |
| Environment Management (10%) | .env.example, runtime validation, no secrets in code, per-env config |
| Monitoring & Observability (15%) | Sentry setup, health endpoint, structured logs, uptime checks, dashboards |
| Backup & Disaster Recovery (10%) | Automated backups, PITR, restore testing, RTO/RPO defined |
| Third-Party Integrations (8%) | Webhook retry, circuit breaker, timeout config, fallback |
| Infrastructure as Code (4%) | Terraform/Pulumi or docker-compose, version-controlled infra |
| Security in Deployment (4%) | Read-only filesystem, resource limits, no root, secrets in vault |

4. **Generate** — Write infrastructure config with all patterns
5. **Self-Check** — Verify all 10 categories
6. **Output** — Config files + compliance checklist

## Quality Contract

- All 10 categories addressed
- Score >= 90 (A-) if audited with infrastructure scoring
- Non-root user in all containers
- No secrets in any config file
- Health check endpoint included
