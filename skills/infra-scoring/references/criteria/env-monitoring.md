# Environment Management (10%) + Monitoring & Observability (15%)

## Category 5: Environment Management — 10%

Score 0-10 based on how many criteria are met:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Env validation at startup | Zod/runtime validation of all env vars (not raw `process.env`) |
| 2 | .env.example documented | All required vars listed with descriptions |
| 3 | Type-safe env access | TypeScript types for env vars (`env.ts` or `env.d.ts`) |
| 4 | Per-environment configs | Different values for dev/staging/prod |
| 5 | No secrets in code | No hardcoded API keys, passwords, tokens in source |
| 6 | Secrets in secure store | Production secrets in Vault, AWS SM, Vercel env, not CI config |
| 7 | .env in .gitignore | `.env` and `.env.local` excluded from version control |
| 8 | Env var naming convention | Consistent prefix/naming (e.g., `NEXT_PUBLIC_`, `DATABASE_`) |
| 9 | Secret rotation process | Documentation or automation for rotating secrets |
| 10 | Env sync verification | Script or CI check that .env.example matches actual usage |

### Scoring Guide

| Score | Criteria Met |
|-------|-------------|
| 10 | All 10 criteria met |
| 8-9 | Validation + types + .env.example + no secrets in code |
| 6-7 | Basic env management, some gaps in documentation/rotation |
| 4-5 | .env.example exists but no validation |
| 2-3 | Minimal env management |
| 0-1 | Raw process.env everywhere, secrets in code |

### Key Files

- `src/lib/env.ts` — Runtime validation
- `src/types/env.d.ts` — Type declarations
- `.env.example` — Documentation
- `.gitignore` — Exclusion list

---

## Category 6: Monitoring & Observability — 15%

Score 0-10 based on how many criteria are met:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Structured logging | JSON-formatted logs with consistent fields (not `console.log`) |
| 2 | Health endpoint | `/api/health` returns 200 + status info |
| 3 | Readiness endpoint | `/api/ready` checks DB + external deps |
| 4 | Error tracking | Sentry, Bugsnag, or equivalent error aggregation |
| 5 | Request logging | API requests logged with method, path, status, duration |
| 6 | Alert rules | Automated alerts on error rate spikes, downtime |
| 7 | Latency tracking | p50/p95/p99 response time metrics |
| 8 | Uptime monitoring | External uptime check (Pingdom, UptimeRobot, Checkly) |
| 9 | Log aggregation | Centralized log storage (Datadog, Logtail, CloudWatch) |
| 10 | Dashboard | Key metrics visible in a dashboard (not CLI-only) |

### Scoring Guide

| Score | Criteria Met |
|-------|-------------|
| 10 | All 10 criteria met — full observability stack |
| 8-9 | Structured logging + health checks + error tracking + alerts |
| 6-7 | Health checks + basic logging, no alerting |
| 4-5 | Health endpoint exists, console-based logging |
| 2-3 | Minimal logging, no health checks |
| 0-1 | No monitoring at all |

### Common Deductions

- `console.log` instead of structured logger → -2
- No health endpoint → -2
- No error tracking service → -1
- No alerting → -1
- Health endpoint returns 200 without checking deps → -1

### Platform Adjustments

**Vercel**: Built-in analytics = +1 toward criterion 7. Vercel Logs = +1 toward criterion 9. Still needs health endpoints and error tracking.
