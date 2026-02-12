# CI Pipeline (15%) + CD Pipeline (12%)

## Category 1: CI Pipeline — 15%

Score 0-10 based on how many criteria are met:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | CI pipeline exists | `.github/workflows/` has at least one workflow triggered on push/PR |
| 2 | Lint gate | Pipeline runs `eslint` or equivalent linter, fails on errors |
| 3 | Type-check gate | Pipeline runs `tsc --noEmit` or equivalent, fails on errors |
| 4 | Test gate | Pipeline runs test suite, fails on test failures |
| 5 | Build gate | Pipeline runs `next build` or equivalent, fails on build errors |
| 6 | Parallel jobs | Lint, typecheck, test, build run as parallel jobs (not sequential steps) |
| 7 | Dependency caching | `actions/cache` or `pnpm store` cache configured, not fresh install every run |
| 8 | Fail-fast strategy | Pipeline stops early on first failure (no wasted compute) |
| 9 | Timeout limits | Jobs have `timeout-minutes` set (not unbounded) |
| 10 | Branch protection | CI required to pass before merge (branch protection or status checks) |

### Scoring Guide

| Score | Criteria Met |
|-------|-------------|
| 10 | All 10 criteria met |
| 9 | 9 criteria met |
| 8 | 8 criteria met |
| 7 | 7 criteria met — missing minor items (timeout, fail-fast) |
| 6 | 6 criteria met — basic CI exists with gaps |
| 5 | 5 criteria met — CI exists but incomplete |
| 3-4 | Pipeline exists but missing lint/test/build gates |
| 1-2 | Minimal pipeline (only build, no quality gates) |
| 0 | No CI pipeline at all |

### Common Deductions

- No `.github/workflows/` → score 0
- Pipeline exists but no lint step → -1
- Pipeline exists but no test step → -1
- Sequential steps instead of parallel jobs → -1
- No dependency caching → -1
- No timeout on jobs → -1

---

## Category 2: CD Pipeline — 12%

Score 0-10 based on how many criteria are met:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Auto-deploy on merge | Merging to main triggers deploy to staging/preview |
| 2 | Preview deploys | PRs get unique preview URLs (Vercel preview, Netlify deploy preview) |
| 3 | Staging environment | Separate staging environment exists before production |
| 4 | Environment-specific configs | Different env vars per environment (dev/staging/prod) |
| 5 | Deploy notifications | Team notified on deploy (Slack, email, GitHub status) |
| 6 | Smoke tests post-deploy | Automated health check after deploy completes |
| 7 | Rollback capability | Can quickly revert to previous deployment |
| 8 | Deploy logs accessible | Deployment logs visible to team (not black-box deploys) |
| 9 | Zero-downtime deploys | No service interruption during deployment |
| 10 | Deploy frequency tracking | Can measure deployment frequency (DORA metric) |

### Scoring Guide

| Score | Criteria Met |
|-------|-------------|
| 10 | All 10 criteria met |
| 9 | 9 criteria met |
| 8 | 8 criteria met |
| 7 | 7 criteria — auto-deploy + previews + staging working |
| 6 | 6 criteria — basic CD with some gaps |
| 5 | 5 criteria — CD works but missing monitoring/rollback |
| 3-4 | Auto-deploy exists but no previews or staging |
| 1-2 | Manual deploy with some automation |
| 0 | Fully manual deployment process |

### Platform Adjustments

**Vercel**: Auto-deploy on push = +1 to criterion 1. Preview deploys per PR = +1 to criterion 2. Built-in rollback = +1 to criterion 7. Zero-downtime by default = +1 to criterion 9.

**Self-hosted**: Must configure all criteria manually. No free preview deploys.
