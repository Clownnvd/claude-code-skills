# Fix Patterns: IaC + Deployment Security

## Infrastructure as Code Fixes

### Vercel Configuration (vercel.json)

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "regions": ["sin1"],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    },
    {
      "source": "/(.*)\\.(?:jpg|jpeg|png|gif|webp|svg|ico|woff2)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

### GitHub Repository Configuration

Document in `docs/infrastructure.md`:
```markdown
## Infrastructure

### Hosting: Vercel
- Region: sin1 (Singapore)
- Framework: Next.js
- Auto-deploy: push to main

### Database: Neon PostgreSQL
- Region: ap-southeast-1
- Project: sell-template
- Connection: pooled (serverless driver)

### Services
- Auth: Better Auth (self-hosted)
- Payments: Stripe (one-time)
- Email: Resend
- Rate Limiting: Upstash Redis
- Version Control: GitHub
```

### Environment Parity

Document environment differences:
```markdown
| Variable | Development | Staging | Production |
|----------|------------|---------|------------|
| DATABASE_URL | Local/Neon branch | Neon staging branch | Neon main |
| STRIPE_SECRET_KEY | sk_test_... | sk_test_... | sk_live_... |
| BETTER_AUTH_URL | localhost:3000 | staging.app.com | app.com |
```

---

## Deployment Security Fixes

### Dependency Vulnerability Scanning

```yaml
# .github/workflows/security.yml
name: Security

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "0 6 * * 1"  # Weekly Monday 6am

jobs:
  audit:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm audit --audit-level=high
        continue-on-error: true
      - name: Check for known vulnerabilities
        run: npx better-npm-audit audit --level high
```

### GitHub Dependabot

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 10
    groups:
      production-deps:
        patterns: ["*"]
        exclude-patterns: ["@types/*", "eslint*", "prettier*"]
      dev-deps:
        patterns: ["@types/*", "eslint*", "prettier*"]
```

### Secret Injection (Not Baked)

Vercel handles this natively:
- Secrets set in Vercel Dashboard > Environment Variables
- Injected at runtime, not in build output
- Different values per environment (Production/Preview/Development)

For Docker:
```yaml
# docker-compose.yml — secrets via env_file
services:
  app:
    env_file:
      - .env.production
    # NEVER use 'environment:' with hardcoded secrets
```

### Audit Logging for Deploys

GitHub provides deploy audit trail automatically:
- Commit SHA, author, timestamp
- PR link, review approvals
- Vercel deployment URL + logs

### No Secrets in Logs

```typescript
// Sanitize before logging
function sanitize(obj: Record<string, unknown>): Record<string, unknown> {
  const sensitive = ["password", "token", "secret", "key", "authorization"];
  return Object.fromEntries(
    Object.entries(obj).map(([k, v]) => [
      k,
      sensitive.some((s) => k.toLowerCase().includes(s)) ? "[REDACTED]" : v,
    ])
  );
}
```

### Least Privilege

- GitHub Token: Only `repo` scope needed (for collaborator invite)
- Stripe: Use restricted API keys in production
- Neon: Use role with minimal permissions (no DROP/ALTER in app)
- Vercel: Team members have appropriate role (Viewer/Developer/Admin)
