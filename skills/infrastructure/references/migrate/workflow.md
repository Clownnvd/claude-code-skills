# Infrastructure Migrate Workflow

## Process

1. **Detect Versions** — Node.js, Docker base image, CI runner, deployment platform
2. **Map Breaking Changes**:

| From → To | Category Affected | Breaking Change | Migration Action |
|-----------|------------------|-----------------|-----------------|
| Node 18 → 20 | Production Readiness | Runtime changes | Update Dockerfile base |
| Node 20 → 22 | Production Readiness | ESM changes | Test module resolution |
| Docker Compose v1 → v2 | IaC | CLI command changes | Update compose commands |
| GitHub Actions v3 → v4 | CI/CD | Runner changes | Update action versions |
| pnpm 8 → 9 | Container | Lock file format | Update install commands |
| Alpine 3.18 → 3.19 | Container | Package availability | Test package install |

3. **Apply Migrations** — Update configs, preserve security posture
4. **Verify** — Build passes, deploy succeeds, health check responds
5. **Re-score** — Ensure no infrastructure regression

## Safety Rules

- NEVER remove health checks during migration
- Keep non-root user through all base image changes
- Test full build pipeline after any CI/CD change
- Verify secrets are not exposed in new config format
