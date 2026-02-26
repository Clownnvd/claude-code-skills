# Backup & Disaster Recovery (10%) + Third-Party Integrations (8%)

## Category 7: Backup & Disaster Recovery — 10%

Score 0-10 based on how many criteria are met:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Automated DB backups | Daily automated backups (provider-managed or cron) |
| 2 | Backup testing | Regular restore tests (not just assume backups work) |
| 3 | Point-in-time recovery | Can restore to specific timestamp (WAL/binlog) |
| 4 | Off-site backup copies | Backups stored in different region/provider |
| 5 | RTO/RPO defined | Recovery Time/Point Objectives documented |
| 6 | Migration strategy | Prisma migrations versioned, rollback migrations exist |
| 7 | Seed data script | `prisma db seed` or equivalent for fresh environments |
| 8 | Data export capability | Can export user data (GDPR compliance) |
| 9 | Disaster recovery runbook | Documented step-by-step recovery process |
| 10 | Recovery drill schedule | Regular practice of recovery procedures |

### Scoring Guide

| Score | Criteria Met |
|-------|-------------|
| 10 | All 10 criteria met — enterprise DR |
| 8-9 | Automated backups + PITR + migrations + seed |
| 6-7 | Provider-managed backups + migrations working |
| 4-5 | Basic backups exist, no testing or runbooks |
| 2-3 | Migrations exist but no backup strategy |
| 0-1 | No backup strategy |

### Platform Adjustments

**Neon PostgreSQL**: Automatic branching = PITR (criterion 3). Daily backups included in plan (criterion 1). Still needs: backup testing, off-site copies, runbooks.

**Vercel + Neon**: Provider handles infrastructure backup, but application-level data export and migration strategy still required.

---

## Category 8: Third-Party Integrations — 8%

Score 0-10 based on how many criteria are met:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Timeout on external calls | All fetch/SDK calls have timeout (AbortController or lib config) |
| 2 | Retry with backoff | Failed calls retry with exponential backoff |
| 3 | Circuit breaker | Stop calling failing service after threshold |
| 4 | Graceful degradation | App works (degraded) when external service is down |
| 5 | Error logging | Integration failures logged with context (not silent catch) |
| 6 | Health check per integration | Can verify each external service is reachable |
| 7 | Webhook idempotency | Webhook handlers check-before-create (no duplicate processing) |
| 8 | Webhook signature verification | Verify webhook authenticity (HMAC, Stripe signature) |
| 9 | Rate limit awareness | Respect provider rate limits (not flood external APIs) |
| 10 | Fallback responses | Sensible defaults when external data unavailable |

### Scoring Guide

| Score | Criteria Met |
|-------|-------------|
| 10 | All 10 criteria met — resilient integrations |
| 8-9 | Timeout + retry + logging + webhook security |
| 6-7 | Timeout + logging, no retry/circuit breaker |
| 4-5 | Basic error handling, some timeout coverage |
| 2-3 | External calls with minimal error handling |
| 0-1 | Raw fetch with no timeout, no error handling |

### Key Integrations to Check

For this project specifically:
- **Stripe**: Checkout, webhooks, payment verification
- **GitHub API**: Collaborator invite
- **Resend**: Email sending
- **Neon**: Database connection (via Prisma)
- **Upstash**: Rate limiting (Redis)

### Common Deductions

- No timeout on Stripe/GitHub/Resend calls → -2
- Silent catch blocks on API errors → -1
- Webhook handler without signature verification → -2
- No idempotency in webhook processing → -1
- Leaking external API errors to client → -1
