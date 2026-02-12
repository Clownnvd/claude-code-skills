# Fix Patterns: CI Pipeline + CD Pipeline

## CI Pipeline Fixes

### Add GitHub Actions CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
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
      - run: pnpm lint

  typecheck:
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
      - run: pnpm typecheck

  test:
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
      - run: pnpm test:run

  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    needs: [lint, typecheck, test]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm build
    env:
      # Add required build env vars here
      SKIP_ENV_VALIDATION: "true"
```

Key patterns:
- **Parallel jobs**: lint, typecheck, test run simultaneously
- **Build depends on gates**: `needs: [lint, typecheck, test]`
- **pnpm cache**: `actions/setup-node` with `cache: pnpm`
- **Timeout**: Each job has `timeout-minutes`
- **Concurrency**: Cancel in-progress runs for same ref

### Add Branch Protection

Via GitHub Settings > Branches > Branch protection rules:
- Require status checks: lint, typecheck, test, build
- Require PR reviews before merge
- Dismiss stale reviews on new pushes

---

## CD Pipeline Fixes

### Vercel Auto-Deploy (already built-in)

If using Vercel, CD is largely automatic:
- Push to main → deploy to production
- PR → preview deploy with unique URL
- Rollback via Vercel dashboard

### Add Deploy Notifications

```yaml
# Add to .github/workflows/ci.yml or separate deploy.yml
  notify:
    runs-on: ubuntu-latest
    needs: [build]
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Notify deployment
        run: |
          echo "Deployed commit ${{ github.sha }}"
          # Add Slack/Discord webhook notification here
```

### Add Smoke Test After Deploy

```yaml
  smoke-test:
    runs-on: ubuntu-latest
    needs: [deploy]
    steps:
      - name: Health check
        run: |
          for i in 1 2 3 4 5; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${{ vars.DEPLOY_URL }}/api/health)
            if [ "$STATUS" = "200" ]; then
              echo "Health check passed"
              exit 0
            fi
            sleep 10
          done
          echo "Health check failed"
          exit 1
```

### Environment-Specific Configs

Use Vercel environment variables:
- **Production**: Set in Vercel dashboard under Production
- **Preview**: Set under Preview environment
- **Development**: Use `.env.local` locally

Or GitHub Actions environments:
```yaml
jobs:
  deploy-staging:
    environment: staging
    # Uses staging secrets

  deploy-production:
    environment: production
    # Uses production secrets, requires approval
```
