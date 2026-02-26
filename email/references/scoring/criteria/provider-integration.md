# Scoring Criteria: Email Provider Integration (12%) + Analytics & Tracking (7%)

## Email Provider Integration (12%)

Measures SDK initialization, env validation, error handling, and domain verification.

### Point Breakdown

| Points | Requirement |
|--------|------------|
| 0 | No email provider configured |
| 1 | Resend imported but not initialized properly |
| 2 | Client initialized but no env var validation |
| 3 | Env var validated but error handling missing on send calls |
| 4 | Basic error handling but no typed error responses |
| 5 | Typed error handling, env validation, but domain not verified |
| 6 | Verified domain, proper init, error handling, env vars documented |
| 7 | + From address from env var, batch sending support, API rate awareness |
| 8 | + Domain verification status check, multiple domain support |
| 9 | + Provider abstraction layer (swap providers without code changes) |
| 10 | + Multi-provider failover, health checks, circuit breaker pattern |

### What to Check

- `src/lib/resend.ts` -- Is the Resend client initialized with validated API key?
- Error handling -- Does every `resend.emails.send()` check `{ data, error }`?
- Domain -- Is the sending domain verified (not `onboarding@resend.dev`)?
- From address -- Is it loaded from `EMAIL_FROM` env var (not hardcoded)?
- `.env.example` -- Are all required email env vars documented?
- `package.json` -- Is `resend` at a recent version?

### Common Issues

| Score | Issue | Severity |
|-------|-------|----------|
| 0-1 | No email provider configured | CRITICAL |
| 2-3 | No env var validation; runtime crash if key missing | CRITICAL |
| 4-5 | Errors swallowed in catch blocks; no logging | HIGH |
| 6-7 | Hardcoded from address; will break on domain change | MEDIUM |

---

## Analytics & Tracking (7%)

Measures open/click tracking, delivery metrics, dashboards, and alerting.

### Point Breakdown

| Points | Requirement |
|--------|------------|
| 0 | No tracking at all |
| 1 | Only checking Resend dashboard manually |
| 2 | Send attempts logged but no delivery status tracking |
| 3 | Webhook events received but not stored or processed |
| 4 | Delivery events stored (sent, delivered, bounced) |
| 5 | + Open and click events tracked via webhook |
| 6 | + Per-email-type delivery metrics (success rate, open rate) |
| 7 | + Dashboard or API endpoint for email health metrics |
| 8 | + Alerting on delivery rate drops (e.g., bounce rate > 2%) |
| 9 | + Historical trend analysis, funnel metrics (sent->delivered->opened->clicked) |
| 10 | + Real-time monitoring, anomaly detection, automated incident response |

### What to Check

- Webhook handler -- Does it process `email.sent`, `email.delivered`, `email.opened`, `email.clicked`?
- Storage -- Are delivery events persisted to database?
- Metrics -- Can you query delivery rate, open rate, bounce rate per email type?
- Alerts -- Is there alerting when bounce rate exceeds threshold?
- Dashboard -- Is there a UI or API for viewing email metrics?

### Common Issues

| Score | Issue | Severity |
|-------|-------|----------|
| 0-2 | No delivery tracking; blind to email failures | HIGH |
| 3-4 | Webhook events received but not persisted | MEDIUM |
| 5-6 | No alerting on delivery rate drops | MEDIUM |
| 7 | No historical trends or per-type metrics | LOW |
