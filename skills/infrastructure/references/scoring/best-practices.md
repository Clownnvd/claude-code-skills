# Infrastructure Best Practices

## 1. CI Pipeline

| Do | Don't |
|----|-------|
| Run lint, typecheck, test in parallel | Sequential jobs that waste time |
| Fail fast on lint errors | Allow broken code to reach test phase |
| Cache node_modules/pnpm store | Fresh install every run |
| Use matrix strategy for Node versions | Test on single version only |
| Set timeout limits on jobs | Allow jobs to run indefinitely |

## 2. CD Pipeline

| Do | Don't |
|----|-------|
| Auto-deploy to staging on merge | Manual deploy every time |
| Preview deploys for PRs | Review code without seeing it live |
| Environment-specific configs | Same config for all environments |
| Deployment notifications (Slack/email) | Silent deployments |
| Smoke tests after deploy | Deploy and hope |

## 3. Production Deploy

| Do | Don't |
|----|-------|
| Manual approval gate for production | Auto-deploy to production |
| Rollback strategy documented | No plan for failed deploys |
| Blue-green or canary deploys | Big bang deployments |
| Deploy during low-traffic windows | Deploy during peak hours |
| Post-deploy verification checks | Deploy and forget |

## 4. Containerization

| Do | Don't |
|----|-------|
| Multi-stage Dockerfile | Single stage with dev deps |
| .dockerignore for node_modules, .git | Copy entire project context |
| Pin base image versions | Use `latest` tag |
| Non-root user in container | Run as root |
| Health check in Dockerfile | No container health check |

## 5. Environment Management

| Do | Don't |
|----|-------|
| Validate all env vars at startup | Access process.env directly |
| Document all vars in .env.example | Undocumented secret variables |
| Different configs per environment | Same secrets in dev and prod |
| Rotate secrets regularly | Never-rotated API keys |
| Use secrets manager (Vault, AWS SM) | Env vars in CI config |

## 6. Monitoring & Observability

| Do | Don't |
|----|-------|
| Structured JSON logging | console.log with strings |
| Health + readiness endpoints | No health checks |
| Alert on error rate spikes | Check logs manually |
| Track response times (p50, p95, p99) | No latency metrics |
| Dashboard for key metrics | CLI-only monitoring |

## 7. Backup & Disaster Recovery

| Do | Don't |
|----|-------|
| Automated daily DB backups | Manual backup before changes |
| Test restore regularly | Assume backups work |
| Define RTO/RPO targets | No recovery objectives |
| Off-site backup copies | Single backup location |
| Documented runbooks | Tribal knowledge only |

## 8. Third-Party Integrations

| Do | Don't |
|----|-------|
| Timeout on all external calls | Unbounded fetch requests |
| Retry with exponential backoff | Immediate retry flood |
| Circuit breaker for failing services | Keep calling dead service |
| Graceful degradation | Hard failure on API down |
| Log integration failures | Silent catch blocks |

## 9. Infrastructure as Code

| Do | Don't |
|----|-------|
| Version-controlled infra configs | Manual cloud console changes |
| Reproducible environments | Snowflake servers |
| Plan before apply | Apply without review |

## 10. Security in Deployment

| Do | Don't |
|----|-------|
| Scan container images for CVEs | Deploy unscanned images |
| Inject secrets at runtime | Bake secrets into images |
| Principle of least privilege | Over-permissive IAM roles |
