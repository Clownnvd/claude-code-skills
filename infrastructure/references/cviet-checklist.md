# CViet-Specific Deployment Checklist

> Part of: CI/CD & Deployment Reference -- Next.js 16 + Prisma + Neon (CViet)
> Stack: Next.js 16.1.6 (App Router, Webpack mode) | Prisma 6 + Neon PostgreSQL | pnpm | TypeScript

---

## Pre-Deployment (One-Time Setup)

- [ ] **Neon database created** with production branch
- [ ] **Prisma schema pushed** to production: `DATABASE_URL=<real> pnpm db:push`
- [ ] **Vercel project linked** and connected to GitHub repo
- [ ] **Environment variables set** in Vercel Dashboard (all 9 variables from Section 7.1)
- [ ] **Neon-Vercel integration** installed for preview DB branching
- [ ] **Custom domain** configured (if applicable)
- [ ] **Polar webhook URL** updated to production domain: `https://cviet.vn/api/polar`
- [ ] **Google OAuth redirect URI** updated: `https://cviet.vn/api/auth/callback/google`
- [ ] **Better Auth `trustedOrigins`** includes production domain

## Per-Release Checklist

- [ ] **All tests pass locally** (when tests are added)
- [ ] **`pnpm build` succeeds locally** with fake env vars
- [ ] **`pnpm lint` passes** (no ESLint errors)
- [ ] **TypeScript compiles** (`pnpm tsc --noEmit`)
- [ ] **Database migrations** (if any) are committed in `prisma/migrations/`
- [ ] **No secrets in code** (grep for API keys, passwords)
- [ ] **`NEXT_PUBLIC_APP_URL`** is correct for target environment
- [ ] **Postinstall patches** still apply (check CI build logs for "already patched")

## Post-Deployment Verification

- [ ] **Landing page loads** (`https://cviet.vn`)
- [ ] **Auth flow works** (signup, login, Google OAuth)
- [ ] **Dashboard loads** (requires auth)
- [ ] **CV creation wizard** works (create new CV, save)
- [ ] **AI enhancement** works (Claude API call succeeds)
- [ ] **PDF export** works (download generates valid PDF)
- [ ] **Polar billing** works (checkout flow, webhook)
- [ ] **Health endpoint** responds: `GET /api/health` returns 200
- [ ] **No console errors** in browser DevTools
- [ ] **Web Vitals acceptable** (LCP < 2.5s, FID < 100ms, CLS < 0.1)

## Monitoring Setup

- [ ] **Uptime monitoring** configured for `/api/health`
- [ ] **Error tracking** (Sentry or similar) installed
- [ ] **Vercel Analytics** enabled (free with Vercel)
- [ ] **Vercel Speed Insights** enabled
- [ ] **Alert channels** configured (email, Slack, Discord)

---

## Appendix A: Quick Command Reference

```bash
# ── Local Development ──
pnpm dev                          # Start dev server (webpack mode)
pnpm build                        # Production build
pnpm start                        # Start production server
pnpm lint                         # ESLint
pnpm db:push                      # Push schema to Neon (dev only)
pnpm db:studio                    # Open Prisma Studio
pnpm db:generate                  # Generate Prisma client

# ── CI Build (fake env) ──
DATABASE_URL="postgresql://fake:fake@localhost/fake" \
BETTER_AUTH_SECRET="ci-build-secret-placeholder-32chars!!" \
NEXT_PUBLIC_APP_URL="http://localhost:3000" \
pnpm build

# ── Vercel CLI ──
vercel                            # Deploy preview
vercel --prod                     # Deploy production
vercel ls                         # List deployments
vercel env ls                     # List env vars
vercel rollback                   # Rollback production
vercel promote                    # Undo rollback

# ── Docker ──
docker build -t cviet:latest .
docker run -p 3000:3000 --env-file .env.production cviet:latest
docker compose up -d --build

# ── Database Migrations ──
pnpm prisma migrate dev --name <name>   # Create migration (local only)
pnpm prisma migrate deploy              # Apply migrations (CI/production)
pnpm prisma migrate status              # Check migration status

# ── Neon CLI ──
neonctl branches list
neonctl branches create --name preview/42
neonctl branches delete preview/42
```

## Appendix B: File Structure for CI/CD

```
cviet/
  .github/
    workflows/
      ci.yml                 # Main CI pipeline (lint + build + deploy)
      docker.yml             # Docker build + push to GHCR
      migrate.yml            # Database migration on schema changes
      neon-branch.yml        # Neon branch management for PRs
  scripts/
    postinstall.js           # Next.js 16.1.6 patches (CRITICAL)
  prisma/
    schema.prisma            # Database schema
    migrations/              # Migration files (if using migrate)
  Dockerfile                 # Multi-stage production build
  .dockerignore              # Exclude unnecessary files
  docker-compose.yml         # Docker Compose for production
  vercel.json                # Vercel configuration (optional)
  .env                       # Default values (committed)
  .env.local                 # Local secrets (gitignored)
  .env.production            # Production defaults (committed)
```

---

> **Sources:**
> - [Next.js Deploying Docs](https://nextjs.org/docs/app/getting-started/deploying)
> - [Vercel Deployments Overview](https://vercel.com/docs/deployments/overview)
> - [Neon + Vercel Integration](https://neon.com/docs/guides/vercel)
> - [Neon Database Branching with GitHub Actions](https://neon.com/docs/guides/branching-github-actions)
> - [Prisma Migrate Deploy](https://www.prisma.io/docs/orm/prisma-client/deployment/deploy-database-changes-with-prisma-migrate)
> - [Prisma + Neon Migrations Guide](https://neon.com/docs/guides/prisma-migrations)
> - [pnpm GitHub Actions Setup](https://pnpm.io/continuous-integration)
> - [Next.js CI Build Caching Guide](https://nextjs.org/docs/pages/guides/ci-build-caching)
> - [Vercel Instant Rollback](https://vercel.com/docs/instant-rollback)
> - [Next.js Turbopack Filesystem Cache](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopackFileSystemCache)
> - [Vercel Deployment Protection](https://vercel.com/docs/deployment-protection)
> - [Complete Guide to Deploying Next.js Apps in 2026 (DEV Community)](https://dev.to/zahg_81752b307f5df5d56035/the-complete-guide-to-deploying-nextjs-apps-in-2026-vercel-self-hosted-and-everything-in-between-48ia)
> - [Optimizing Next.js Docker Images with Standalone Mode](https://dev.to/angojay/optimizing-nextjs-docker-images-with-standalone-mode-2nnh)
> - [Next.js CI/CD with GitHub Actions (BetterLink Blog)](https://eastondev.com/blog/en/posts/dev/20251220-nextjs-cicd-github-actions/)
