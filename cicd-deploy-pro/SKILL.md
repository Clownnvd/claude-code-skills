---
name: cicd-deploy-pro
description: "CI/CD & Deployment for Next.js 16 + Prisma + Neon. Vercel, Docker, GitHub Actions, database migrations, rollback, 20 documented errors. Triggers: deploy, vercel, docker, ci/cd, github actions, pipeline, build, production, staging."
---

# CI/CD Deploy Pro -- Deployment for Next.js 16

## When to Use

Trigger on any mention of: deploy, deployment, vercel, docker, github actions, ci/cd, pipeline, build production, staging, preview, rollback, dockerfile, health check, monitoring, postinstall.

## Reference Files

| File | Description |
|------|-------------|
| `references/deployment-targets.md` | Vercel vs Docker vs Node.js vs Cloudflare -- feature comparison matrix, CViet recommendation |
| `references/vercel.md` | Project setup, vercel.json config, env vars, preview deployments, custom domains, Neon integration |
| `references/docker.md` | Multi-stage Dockerfile, standalone output, docker-compose, .dockerignore, image optimization |
| `references/self-hosted.md` | PM2 deployment, ecosystem config, Nginx reverse proxy, Kamal deployment |
| `references/github-actions.md` | 4 workflow YAMLs: CI pipeline, Docker build+push, DB migration, Neon branch management |
| `references/prisma-neon-ci.md` | Build vs runtime DB access, fake URL pattern, Neon connection strings, branching, migration workflow |
| `references/environment-vars.md` | 9 vars classified (type/build/runtime/public), env file strategy, GitHub Actions secrets, NEXT_PUBLIC_ warning |
| `references/postinstall-patches.md` | All 7 patches explained, CI/Vercel/Docker integration, upgrade protocol |
| `references/build-optimization.md` | pnpm store cache, .next/cache, Turbopack, parallel jobs, selective builds, benchmarks |
| `references/health-checks.md` | Health API route, ping route, Sentry setup, Web Vitals, uptime services, structured logging |
| `references/rollback.md` | Vercel instant rollback, Docker tag revert, Git-based rollback, DB rollback, decision matrix |
| `references/errors.md` | 20 errors (CD-001 through CD-020) with exact messages, causes, and fixes |
| `references/cviet-checklist.md` | Pre-deploy, per-release, post-deploy checklists, quick command reference, CI/CD file structure, sources |

## Error Quick Lookup

| ID | Error | Fix |
|----|-------|-----|
| CD-001 | Build fails -- missing DATABASE_URL | Use fake URL: `postgresql://fake:fake@localhost/fake` |
| CD-002 | Missing BETTER_AUTH_SECRET at build | Provide dummy 32-char value at build time |
| CD-003 | `generate is not a function` | Patch 1 via `scripts/postinstall.js` |
| CD-004 | SWC `cacheComponentsEnabled` missing | Patch 2 via `scripts/postinstall.js` |
| CD-005 | Module not found: next-response | Patches 3-4 via `scripts/postinstall.js` |
| CD-006 | `config.compiler` undefined | Patch 5 + `compiler: {}` in next.config.ts |
| CD-007 | picomatch hostname undefined | Patch 6 via `scripts/postinstall.js` |
| CD-008 | `htmlLimitedBots.source` undefined | Patch 7 via `scripts/postinstall.js` |
| CD-009 | `pnpm-lock.yaml` mismatch | Run `pnpm install` locally, commit lockfile |
| CD-010 | Prisma Client not found at runtime (Docker) | Copy `.prisma` + `@prisma` + `prisma/` to runner stage |
| CD-011 | `canvas.node` missing (Docker) | Add `libc6-compat python3 make g++` to deps stage |
| CD-012 | Vercel function timeout on PDF export | Set `maxDuration: 30` in vercel.json |
| CD-013 | Wrong `NEXT_PUBLIC_APP_URL` in preview | Use `VERCEL_URL` system env var |
| CD-014 | pnpm store cache miss in Actions | Run `pnpm/action-setup` BEFORE `actions/setup-node` |
| CD-015 | Build cache not detected | Persist `.next/cache` with `actions/cache@v4` |
| CD-016 | Neon branch connection refused | Verify `create-branch-action` succeeded, check naming |
| CD-017 | Node.js version mismatch | Pin `node-version: '22'` in CI |
| CD-018 | Hydration mismatch after deploy | Wrap dynamic content in `<Suspense>` |
| CD-019 | Memory exceeded during build | Set `NODE_OPTIONS="--max-old-space-size=4096"` |
| CD-020 | `cross-env` not found in CI | Ensure CI uses `pnpm build`, not `pnpm dev` |

## Key Patterns

### Build Command (CI/Vercel)
```bash
BETTER_AUTH_SECRET="..." \
DATABASE_URL="postgresql://fake:fake@localhost/fake" \
NEXT_PUBLIC_APP_URL="https://your-domain.com" \
pnpm build
```

### GitHub Actions CI
```yaml
- uses: pnpm/action-setup@v4
  with: { version: 9 }
- uses: actions/setup-node@v4
  with:
    node-version: 22
    cache: pnpm
- run: pnpm install
- run: pnpm build
  env:
    DATABASE_URL: postgresql://fake:fake@localhost/fake
```

### Docker (Multi-stage)
```dockerfile
FROM node:22-alpine AS deps
RUN corepack enable pnpm
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM node:22-alpine AS builder
COPY --from=deps /app/node_modules ./node_modules
RUN pnpm build

FROM node:22-alpine AS runner
COPY --from=builder /app/.next/standalone ./
CMD ["node", "server.js"]
```
