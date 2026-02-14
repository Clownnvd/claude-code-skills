# Email Fix -- Overview

## Purpose

Take a scorecard from email-scoring and systematically implement fixes. Prioritize by severity * weight. Verify each fix before moving to the next.

## Priority Table

| Priority | Severity | Score Range | Weight | Action |
|----------|----------|-------------|--------|--------|
| 1 | CRITICAL | 0-3 | Any | Fix immediately -- blocks deploy |
| 2 | HIGH | 4-5 | >= 12% | Fix next -- moves score most |
| 3 | HIGH | 4-5 | < 12% | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Any | Fix next sprint |
| 5 | LOW | 8 | Any | Backlog or skip |

## Category -> Fix Pattern Mapping

| Scorecard Category | Fix Pattern File |
|-------------------|-----------------|
| Transactional Email (15%) | `fix-patterns/transactional-delivery.md` |
| Notification Queue & Delivery (12%) | `fix-patterns/transactional-delivery.md` |
| Email Templates & Rendering (12%) | `fix-patterns/templates-rendering.md` |
| Testing & Preview (6%) | `fix-patterns/templates-rendering.md` |
| Email Provider Integration (12%) | `fix-patterns/provider-integration.md` |
| Analytics & Tracking (7%) | `fix-patterns/provider-integration.md` |
| Deliverability & Reputation (10%) | `fix-patterns/security-compliance.md` |
| Bounce & Complaint Handling (10%) | `fix-patterns/security-compliance.md` |
| Email Auth (SPF/DKIM/DMARC) (8%) | `fix-patterns/security-compliance.md` |
| Rate Limiting & Throttling (8%) | `fix-patterns/security-compliance.md` |

## Files Typically Touched

| File | Fix Types |
|------|-----------|
| `src/lib/resend.ts` | Provider init, env validation |
| `src/lib/email.ts` | Service layer, triggers |
| `src/lib/queue.ts` | QStash client, enqueue |
| `src/emails/*.tsx` | Templates, components |
| `src/app/api/queue/email/route.ts` | Worker endpoint |
| `src/app/api/webhooks/resend/route.ts` | Bounce/delivery events |
| `src/middleware.ts` | Rate limiting |
| `.env.example` | Env var documentation |
| `package.json` | Dependencies |

## Score Targets

| Starting Grade | Target After Fix | Expected Improvement |
|---------------|-----------------|---------------------|
| F (0-59) | C+ or higher | +20-30 points |
| D (60-72) | B- or higher | +10-20 points |
| C (73-79) | B or higher | +7-15 points |
| B (80-89) | A- or higher | +5-10 points |

CRITICAL + HIGH fixes typically yield +15-25 points. MEDIUM fixes yield +5-10.
