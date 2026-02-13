# Infrastructure Generate Workflow

## Process

1. **Parse Request** — Extract: component type (Dockerfile, CI/CD, env config, monitoring), target platform
2. **Load Criteria** — Read all 10 infrastructure scoring categories from SKILL.md
3. **Map Criteria to Code**:

| Category | Code Pattern |
|----------|-------------|
| Production Readiness (10%) | Multi-stage Docker, standalone output, health check |
| Container Optimization (12%) | Alpine base, layer caching, non-root user, minimal image |
| CI/CD Pipeline (10%) | GitHub Actions, lint→test→build→deploy stages |
| Env Configuration (10%) | .env.example, runtime validation, no secrets in code |
| Monitoring & Alerting (15%) | Sentry setup, health endpoint, uptime checks |
| Logging (8%) | Structured JSON logs, log levels, request context |
| CDN & Static Assets (8%) | Asset hashing, CDN config, immutable headers |
| SSL & DNS (4%) | HTTPS redirect, HSTS, cert auto-renewal |
| IaC (4%) | Terraform/Pulumi config or docker-compose |
| Security Hardening (4%) | Read-only filesystem, resource limits, no root |

4. **Generate** — Write infrastructure config with all patterns
5. **Self-Check** — Verify all 10 categories
6. **Output** — Config files + compliance checklist

## Quality Contract

- All 10 categories addressed
- Score >= 90 (A-) if audited with infrastructure scoring
- Non-root user in all containers
- No secrets in any config file
- Health check endpoint included
