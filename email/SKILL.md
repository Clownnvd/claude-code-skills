---
name: email
description: Email quality system. 7 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score->fix until target). Resend + React Email + Upstash patterns.
license: Complete terms in LICENSE.txt
---

# Email Quality System

One skill, 7 modes. Score email/notification design, fix issues, or run the full loop.

## Modes

| Mode | Trigger | What It Does |
|------|---------|--------------|
| **score** | "score my email", "audit notifications" | 10-category audit -> scorecard with grade (A+ to F) |
| **fix** | "fix email issues", provide a scorecard | Parse scorecard -> prioritize -> apply fixes -> verify |
| **loop** | "score and fix until B+", "email loop" | Run score, then fix, then re-score until target grade reached |
| **generate** | Create new code | Load criteria -> Generate meeting all 10 -> Self-check |
| **review** | Quick 1-2 file check | Read files -> Score applicable categories -> Annotate + fix |
| **migrate** | Framework upgrade | Detect versions -> Map breaking changes -> Migrate -> Verify |
| **test** | Generate test cases | Map categories to assertions -> Generate test files |

## Mode: Score

Audit any email system against 10 weighted categories. Score 0-100 with letter grade and prioritized issues list.

Load `references/scoring/scoring-workflow.md` for the full 6-step process.

| # | Category | Weight | Criteria Reference |
|---|----------|--------|--------------------|
| 1 | Transactional Email | 15% | `scoring/criteria/transactional-delivery.md` |
| 2 | Email Templates & Rendering | 12% | `scoring/criteria/templates-rendering.md` |
| 3 | Notification Queue & Delivery | 12% | `scoring/criteria/transactional-delivery.md` |
| 4 | Email Provider Integration | 12% | `scoring/criteria/provider-integration.md` |
| 5 | Deliverability & Reputation | 10% | `scoring/criteria/security-compliance.md` |
| 6 | Bounce & Complaint Handling | 10% | `scoring/criteria/security-compliance.md` |
| 7 | Email Auth (SPF/DKIM/DMARC) | 8% | `scoring/criteria/security-compliance.md` |
| 8 | Rate Limiting & Throttling | 8% | `scoring/criteria/security-compliance.md` |
| 9 | Analytics & Tracking | 7% | `scoring/criteria/provider-integration.md` |
| 10 | Testing & Preview | 6% | `scoring/criteria/templates-rendering.md` |

### Grades

| Grade | Score | Grade | Score | Grade | Score |
|-------|-------|-------|-------|-------|-------|
| A+ | 97-100 | B+ | 87-89 | C+ | 77-79 |
| A | 93-96 | B | 83-86 | C | 73-76 |
| A- | 90-92 | B- | 80-82 | D | 60-72 |
| | | | | F | <60 |

### Issue Severity

| Severity | Criteria | Action |
|----------|----------|--------|
| CRITICAL | Score 0-3 or security risk | Fix before deploy |
| HIGH | Score 4-5 | Fix in current sprint |
| MEDIUM | Score 6-7 | Fix next sprint |
| LOW | Score 8 | Backlog |

## Mode: Fix

Take a scorecard and systematically implement all fixes. Prioritize by severity * weight.

Load `references/fix/implementation-workflow.md` for the full 6-step process.

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or security risk | Fix immediately -- blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next -- moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

### Fix Category -> Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Transactional Email, Notification Queue | `fix/fix-patterns/transactional-delivery.md` |
| Email Templates, Testing & Preview | `fix/fix-patterns/templates-rendering.md` |
| Email Provider, Analytics & Tracking | `fix/fix-patterns/provider-integration.md` |
| Deliverability, Bounce, Auth, Rate Limiting | `fix/fix-patterns/security-compliance.md` |

### Verification

Load `references/fix/verification.md` for post-fix checklist, re-scoring protocol, and comparison template.

## Mode: Loop

Automated score-fix cycle. Runs score -> fix -> re-score until target grade is met.

1. **Score** the email system (Mode: Score)
2. If grade < target, **fix** all CRITICAL + HIGH issues (Mode: Fix)
3. **Re-score** and compare
4. Repeat until target grade reached or no score improvement between iterations

Default target: **B+ (87+)**. Override with "loop until A-" or similar.
- Max 5 iterations
- Stop on plateau (score unchanged after full fix cycle)

## Mode: Generate

Generate code meeting all 10 categories at 9-10/10. Load `references/generate/workflow.md`.
Parse request -> Load criteria -> Generate with all patterns -> Self-check -> Output (`assets/templates/generated-code.md.template`)

## Mode: Review

Quick 1-2 file review. Load `references/review/workflow.md`.
Read files -> Score applicable categories -> Annotate line numbers -> Suggest fixes (`assets/templates/review-report.md.template`)

## Mode: Migrate

Upgrade code for framework changes. Load `references/migrate/workflow.md`.
Detect versions -> Map breaking changes -> Apply migrations -> Verify (`assets/templates/migration-report.md.template`)

## Mode: Test

Generate tests from scoring criteria. Load `references/test/workflow.md`.
Map categories to assertions -> Generate tests -> Output suite (`assets/templates/test-suite.md.template`)

## Stack Adjustments

| Stack | Additional Reference |
|-------|---------------------|
| Resend SDK | `references/resend-patterns.md` -- client init, send, batch, domains, webhooks |
| React Email | `references/react-email-patterns.md` -- components, templates, preview, rendering |
| Upstash QStash | `references/resend-patterns.md` -- queue-based delivery, retry, dead letter |

## Quick Reference -- All Files

### Scoring
- `references/scoring/overview.md` -- Scoring system, grade scale, scorecard format
- `references/scoring/best-practices.md` -- Do/Don't for templates, queue, provider, deliverability
- `references/scoring/scoring-workflow.md` -- 6-step audit process, category mapping, issue format
- `references/scoring/criteria/` -- 4 files covering 10 categories (transactional-delivery, templates-rendering, provider-integration, security-compliance)
- `references/resend-patterns.md` -- Resend SDK, domain verification, webhooks, batch sending
- `references/react-email-patterns.md` -- React Email components, rendering, preview server

### Fix
- `references/fix/overview.md` -- How fix works, priority order, score targets
- `references/fix/best-practices.md` -- Fix discipline, template safety, queue patterns
- `references/fix/implementation-workflow.md` -- 6-step process, priority matrix, which refs to load
- `references/fix/verification.md` -- Post-fix checklist, re-scoring protocol, comparison template
- `references/fix/fix-patterns/` -- 4 files covering 10 categories (transactional-delivery, templates-rendering, provider-integration, security-compliance)

## Output Templates

- Score: `assets/templates/scorecard.md.template` | Fix: `assets/templates/fix-report.md.template`
- Generate: `assets/templates/generated-code.md.template` | Review: `assets/templates/review-report.md.template`
- Migrate: `assets/templates/migration-report.md.template` | Test: `assets/templates/test-suite.md.template`
Fill `{{VARIABLE}}` placeholders with actual values.
