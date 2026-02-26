# Scoring Criteria: Deliverability (10%) + Bounce (10%) + Auth (8%) + Rate Limiting (8%)

## Deliverability & Reputation (10%)

Measures verified domain, sender reputation, list hygiene, and content quality.

### Point Breakdown

| Points | Requirement |
|--------|------------|
| 0 | Sending from unverified domain or default Resend domain |
| 1 | Domain registered but not verified |
| 2 | Domain verified but no SPF/DKIM alignment |
| 3 | SPF/DKIM set up but no DMARC |
| 4 | DMARC at `p=none` (monitor only) |
| 5 | DMARC at `p=quarantine` or `p=reject`, consistent from address |
| 6 | + Suppression list checked before sending |
| 7 | + Bounce rate monitored and below 2% |
| 8 | + List hygiene: inactive addresses pruned, re-engagement campaigns |
| 9 | + Content quality checks (spam score, link validation) |
| 10 | + Dedicated IP, warm-up plan, reputation monitoring service |

### Common Issues

| Score | Issue | Severity |
|-------|-------|----------|
| 0-2 | Unverified domain; emails may go to spam | CRITICAL |
| 3-4 | No DMARC or DMARC at p=none | HIGH |
| 5-6 | No suppression list; sending to bounced addresses | HIGH |
| 7 | No list hygiene or content quality checks | MEDIUM |

---

## Bounce & Complaint Handling (10%)

Measures webhook processing, suppression list, auto-unsubscribe, and feedback loops.

### Point Breakdown

| Points | Requirement |
|--------|------------|
| 0 | No bounce or complaint handling |
| 1 | Errors logged but no webhook for delivery events |
| 2 | Webhook endpoint exists but no signature verification |
| 3 | Webhook verified but only logs; no action on bounces |
| 4 | Hard bounces trigger address removal from send list |
| 5 | + Soft bounce tracking with threshold-based suppression |
| 6 | + Complaint events trigger automatic unsubscribe |
| 7 | + Suppression list checked before every send call |
| 8 | + Bounce/complaint rates tracked per email type |
| 9 | + Automated alerting on bounce rate spikes |
| 10 | + ISP feedback loop processing, proactive list cleaning |

### Common Issues

| Score | Issue | Severity |
|-------|-------|----------|
| 0-1 | No webhook for email events | CRITICAL |
| 2-3 | Webhook exists but no signature verification (security risk) | CRITICAL |
| 4-5 | Hard bounces handled but complaints ignored | HIGH |
| 6-7 | Suppression not checked before sending | MEDIUM |

---

## Email Auth -- SPF/DKIM/DMARC (8%)

Measures DNS records, alignment, policy enforcement, and monitoring.

### Point Breakdown

| Points | Requirement |
|--------|------------|
| 0 | No email authentication records |
| 1 | SPF record exists but incorrect or too permissive |
| 2 | SPF correct; no DKIM |
| 3 | SPF + DKIM configured via Resend |
| 4 | SPF + DKIM + DMARC at `p=none` |
| 5 | DMARC at `p=quarantine` with `rua` reporting |
| 6 | DMARC at `p=reject`, all records aligned |
| 7 | + DMARC aggregate reports monitored |
| 8 | + DNS records documented in project, verification script |
| 9 | + Sub-domain isolation for transactional vs marketing |
| 10 | + Automated DNS validation in CI, BIMI record |

### Common Issues

| Score | Issue | Severity |
|-------|-------|----------|
| 0-2 | Missing SPF/DKIM; high spam risk | CRITICAL |
| 3-4 | No DMARC policy; domain spoofable | HIGH |
| 5-6 | DMARC reports not monitored | MEDIUM |
| 7 | DNS records not documented in project | LOW |

---

## Rate Limiting & Throttling (8%)

Measures endpoint protection, per-user limits, queue throttling, and burst handling.

### Point Breakdown

| Points | Requirement |
|--------|------------|
| 0 | No rate limiting on email-triggering endpoints |
| 1 | Basic global rate limit but bypassable |
| 2 | Per-IP rate limiting on some endpoints |
| 3 | Per-IP + per-user rate limiting on email endpoints |
| 4 | + Rate limit on password reset and verification endpoints |
| 5 | + Queue-level throttling to respect Resend API limits |
| 6 | + Burst protection with sliding window algorithm |
| 7 | + Different limits per email type (transactional vs bulk) |
| 8 | + Rate limit headers returned to clients, retry-after support |
| 9 | + Adaptive rate limiting based on provider feedback |
| 10 | + Distributed rate limiting across multiple instances |

### Common Issues

| Score | Issue | Severity |
|-------|-------|----------|
| 0-2 | No rate limiting; password reset email abuse possible | CRITICAL |
| 3-4 | No queue throttling; may exceed Resend API limits | HIGH |
| 5-6 | No per-email-type differentiation | MEDIUM |
| 7 | No rate limit headers for clients | LOW |
