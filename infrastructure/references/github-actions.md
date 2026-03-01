# GitHub Actions CI/CD Pipelines

> Part of: CI/CD & Deployment Reference -- Next.js 16 + Prisma + Neon (CViet)
> Stack: Next.js 16.1.6 (App Router, Webpack mode) | Prisma 6 + Neon PostgreSQL | pnpm | TypeScript

---

## 5.1 Full Pipeline: Lint + Build + Deploy to Vercel

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: '22'
  PNPM_VERSION: '10'

jobs:
  # ──────────────────────────────────────────────────
  # Job 1: Lint & Type Check
  # ──────────────────────────────────────────────────
  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run postinstall patches
        run: node scripts/postinstall.js

      - name: Generate Prisma client
        run: pnpm db:generate

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm tsc --noEmit

  # ──────────────────────────────────────────────────
  # Job 2: Build
  # ──────────────────────────────────────────────────
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run postinstall patches
        run: node scripts/postinstall.js

      - name: Generate Prisma client
        run: pnpm db:generate

      # Cache .next/cache for faster subsequent builds
      - name: Cache Next.js build
        uses: actions/cache@v4
        with:
          path: .next/cache
          key: nextjs-cache-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}-${{ hashFiles('src/**/*') }}
          restore-keys: |
            nextjs-cache-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}-
            nextjs-cache-${{ runner.os }}-

      - name: Build
        env:
          DATABASE_URL: "postgresql://fake:fake@localhost:5432/fake"
          BETTER_AUTH_SECRET: "ci-build-secret-not-used-at-runtime-min-32-chars"
          NEXT_PUBLIC_APP_URL: "http://localhost:3000"
        run: pnpm build

  # ──────────────────────────────────────────────────
  # Job 3: Deploy (Vercel)
  # ──────────────────────────────────────────────────
  deploy:
    name: Deploy to Vercel
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Deploy to Vercel (Production)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'

  # ──────────────────────────────────────────────────
  # Job 3b: Preview Deploy (PRs)
  # ──────────────────────────────────────────────────
  preview:
    name: Deploy Preview
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'pull_request'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Deploy to Vercel (Preview)
        uses: amondnet/vercel-action@v25
        id: vercel-deploy
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

      - name: Comment PR with preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Preview deployment ready: ${{ steps.vercel-deploy.outputs.preview-url }}`
            })
```

## 5.2 Docker Build + Push Pipeline

```yaml
# .github/workflows/docker.yml
name: Docker Build & Push

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha,prefix=

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            NEXT_PUBLIC_APP_URL=https://cviet.vn
```

## 5.3 Database Migration Pipeline

```yaml
# .github/workflows/migrate.yml
name: Database Migration

on:
  push:
    branches: [main]
    paths:
      - 'prisma/migrations/**'
      - 'prisma/schema.prisma'

jobs:
  migrate:
    name: Run Prisma Migrations
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: '10'

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run postinstall patches
        run: node scripts/postinstall.js

      - name: Deploy migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: pnpm prisma migrate deploy
```

## 5.4 Neon Branch Management for PRs

```yaml
# .github/workflows/neon-branch.yml
name: Neon Database Branching

on:
  pull_request:
    types: [opened, synchronize, reopened, closed]

jobs:
  # Create Neon branch when PR opens
  create-branch:
    if: github.event.action != 'closed'
    runs-on: ubuntu-latest
    outputs:
      db-url: ${{ steps.create.outputs.db_url }}
    steps:
      - name: Create Neon branch
        id: create
        uses: neondatabase/create-branch-action@v5
        with:
          project_id: ${{ secrets.NEON_PROJECT_ID }}
          branch_name: preview/${{ github.event.pull_request.number }}
          api_key: ${{ secrets.NEON_API_KEY }}
          username: ${{ secrets.NEON_DB_USERNAME }}

      - name: Run Prisma migrations on branch
        env:
          DATABASE_URL: ${{ steps.create.outputs.db_url }}
        run: |
          npx prisma migrate deploy

      - name: Comment PR with branch info
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Neon database branch \`preview/${{ github.event.pull_request.number }}\` created.`
            })

  # Delete Neon branch when PR closes
  delete-branch:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - name: Delete Neon branch
        uses: neondatabase/delete-branch-action@v3
        with:
          project_id: ${{ secrets.NEON_PROJECT_ID }}
          branch: preview/${{ github.event.pull_request.number }}
          api_key: ${{ secrets.NEON_API_KEY }}
```

---

> **Sources:**
> - [pnpm GitHub Actions Setup](https://pnpm.io/continuous-integration)
> - [Next.js CI/CD with GitHub Actions (BetterLink Blog)](https://eastondev.com/blog/en/posts/dev/20251220-nextjs-cicd-github-actions/)
> - [Neon Database Branching with GitHub Actions](https://neon.com/docs/guides/branching-github-actions)
