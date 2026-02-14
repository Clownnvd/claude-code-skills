# Scoring Criteria: Transactional Email (15%) + Notification Queue & Delivery (12%)

## Transactional Email (15%)

Measures event-driven email triggers, template selection, personalization, and delivery confirmation.

### Point Breakdown

| Points | Requirement |
|--------|------------|
| 0 | No transactional email implemented |
| 1 | Single hardcoded email call exists somewhere |
| 2 | Multiple send calls but no service layer or abstraction |
| 3 | Service layer exists but missing key triggers (signup, password reset) |
| 4 | Core triggers implemented but no personalization or dynamic content |
| 5 | Personalized emails for main flows but inconsistent patterns |
| 6 | Consistent service layer, typed payloads, all key triggers present |
| 7 | + Delivery confirmation via webhook, idempotent triggers |
| 8 | + Comprehensive trigger coverage, scheduled emails, template versioning |
| 9 | + A/B testing support, send-time optimization, audit trail |
| 10 | + Full lifecycle management, preference center, multi-channel fallback |

### What to Check

- `src/lib/email.ts` -- Does a service layer exist with named functions per email type?
- API routes -- Are emails triggered from business events (not UI handlers)?
- Template selection -- Are templates chosen based on event type and user locale?
- Personalization -- Do templates receive typed props with user-specific data?
- Idempotency -- Can the same event re-fire without duplicate emails?

### Common Issues

| Score | Issue | Severity |
|-------|-------|----------|
| 0-2 | No transactional emails exist | CRITICAL |
| 3 | Missing critical triggers (password reset, email verification) | CRITICAL |
| 4-5 | No service layer; send calls scattered across routes | HIGH |
| 6-7 | No delivery confirmation; fire-and-forget pattern | MEDIUM |

---

## Notification Queue & Delivery (12%)

Measures async processing, retry logic, dead letter queue, and delivery guarantees.

### Point Breakdown

| Points | Requirement |
|--------|------------|
| 0 | No queue; emails sent synchronously in request cycle |
| 1 | Basic setTimeout or background job but no real queue |
| 2 | Queue exists but no retry logic or error handling |
| 3 | Queue with basic retry but no exponential backoff |
| 4 | Retry with backoff but no dead letter queue |
| 5 | Dead letter queue exists but no monitoring or alerting |
| 6 | Full queue pipeline: enqueue -> process -> retry -> DLQ with logging |
| 7 | + QStash signature verification on worker, message deduplication |
| 8 | + Priority queues, delay scheduling, batch processing |
| 9 | + Queue health monitoring, throughput metrics, auto-scaling |
| 10 | + At-least-once delivery guarantee, exactly-once semantics where needed |

### What to Check

- `src/lib/queue.ts` -- Does a queue client exist (QStash preferred)?
- Worker endpoints -- Do they verify signatures and handle errors?
- Retry config -- Is `retries` set with reasonable backoff?
- Dead letter -- What happens to messages that exhaust retries?
- Synchronous calls -- Any `resend.emails.send()` in API route handlers?

### Common Issues

| Score | Issue | Severity |
|-------|-------|----------|
| 0 | No queue; synchronous email sending blocks requests | CRITICAL |
| 1-3 | Queue exists but no retry or error handling | HIGH |
| 4-5 | No dead letter queue; failed emails silently dropped | HIGH |
| 6-7 | No signature verification on worker endpoints | MEDIUM |
