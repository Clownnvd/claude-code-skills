# Email Scoring -- Overview

## Purpose

Score any email/notification system against 10 weighted categories. Produces a 0-100 score with letter grade, prioritized issues, and actionable fixes.

## 10 Categories

| # | Category | Weight | What It Measures |
|---|----------|--------|-----------------|
| 1 | Transactional Email | 15% | Event-driven triggers, template selection, personalization, delivery confirmation |
| 2 | Email Templates & Rendering | 12% | Component system, responsive design, plain text fallback, dynamic content |
| 3 | Notification Queue & Delivery | 12% | Async processing, retry logic, dead letter queue, delivery guarantees |
| 4 | Email Provider Integration | 12% | SDK init, env validation, error handling, domain verification |
| 5 | Deliverability & Reputation | 10% | Verified domain, sender reputation, list hygiene, content quality |
| 6 | Bounce & Complaint Handling | 10% | Webhook processing, suppression list, automatic unsubscribe, feedback loops |
| 7 | Email Auth (SPF/DKIM/DMARC) | 8% | DNS records, alignment, policy enforcement, monitoring |
| 8 | Rate Limiting & Throttling | 8% | Endpoint protection, per-user limits, queue throttling, burst handling |
| 9 | Analytics & Tracking | 7% | Open/click tracking, delivery metrics, dashboards, alerting |
| 10 | Testing & Preview | 6% | Preview server, render tests, integration tests, email client testing |

Weights sum to 100%. Weighted score = raw (0-10) x weight x 10.

## Grade Scale

| Grade | Score | Grade | Score | Grade | Score |
|-------|-------|-------|-------|-------|-------|
| A+ | 97-100 | B+ | 87-89 | C+ | 77-79 |
| A | 93-96 | B | 83-86 | C | 73-76 |
| A- | 90-92 | B- | 80-82 | D | 60-72 |
| | | | | F | <60 |

## Issue Severity

| Severity | Score Range | Criteria | Action |
|----------|------------|----------|--------|
| CRITICAL | 0-3 | Security risk or blocks delivery | Fix before deploy |
| HIGH | 4-5 | Significant gap | Fix in current sprint |
| MEDIUM | 6-7 | Improvement needed | Fix next sprint |
| LOW | 8 | Minor polish | Backlog |

Score 9-10 = no issue generated for that category.

## Anti-Bias Rules

1. Score ONLY what exists in the codebase. Do not assume configuration outside the repo.
2. Do not give credit for "planned" features or TODO comments.
3. If a category is not applicable (e.g., no email system exists), score it 0 with note "N/A -- not implemented."
4. Do not inflate scores to avoid low grades. A score of 2/10 is correct if only basic functionality exists.
5. Each category must be scored independently. A strong template system does not boost Queue score.
6. Weight-based bias: do not unconsciously score high-weight categories more leniently.

## Scorecard Format

Output uses `assets/templates/scorecard.md.template`. Fill all `{{VARIABLE}}` placeholders.

Required sections:
1. **Category Scores** -- table with all 10 rows
2. **Prioritized Issues** -- sorted CRITICAL > HIGH > MEDIUM > LOW
3. **Provider Notes** -- Resend version, domain status, queue status, webhook status
4. **Quick Wins** -- 3-5 items fixable in under 30 minutes

## Integration Points

| Mode | How Scoring Connects |
|------|---------------------|
| Fix | Scorecard is the input. Fix parses issues and applies patterns. |
| Loop | Score -> Fix -> Re-score. Repeats until target grade. |
| Generate | Criteria inform what generated code must satisfy. |
| Review | Subset of categories applied to 1-2 files. |

## Files to Load

Always load these references when scoring:
- `references/scoring/scoring-workflow.md` -- step-by-step process
- `references/scoring/criteria/*` -- detailed point breakdowns per category
- `references/resend-patterns.md` -- Resend-specific patterns to check
- `references/react-email-patterns.md` -- React Email patterns to check
