---
name: payment
description: Payment quality system. 7 modes: score (10-category audit), fix (auto-fix from scorecard), loop (score->fix until target). Stripe + Next.js patterns.
license: Complete terms in LICENSE.txt
---

# Payment Quality System

One skill, 7 modes. Score payment integration, fix issues, or run the full loop.

## Modes

| Mode | Trigger | What It Does |
|------|---------|--------------|
| **score** | "score my payments", "audit Stripe" | 10-category audit -> scorecard with grade (A+ to F) |
| **fix** | "fix payment issues", provide a scorecard | Parse scorecard -> prioritize -> apply fixes -> verify |
| **loop** | "score and fix until B+", "payment loop" | Run score, then fix, then re-score until target grade reached |
| **generate** | Create new code | Load criteria -> Generate meeting all 10 -> Self-check |
| **review** | Quick 1-2 file check | Read files -> Score applicable categories -> Annotate + fix |
| **migrate** | Framework upgrade | Detect versions -> Map breaking changes -> Migrate -> Verify |
| **test** | Generate test cases | Map categories to assertions -> Generate test files |

## Mode: Score

Audit any payment integration against 10 weighted categories. Score 0-100 with letter grade and prioritized issues list.

Load `references/scoring/scoring-workflow.md` for the full 6-step process.

| # | Category | Weight | Criteria Reference |
|---|----------|--------|--------------------|
| 1 | Checkout & Billing Flow | 15% | `scoring/criteria/checkout-billing.md` |
| 2 | Subscription Lifecycle | 15% | `scoring/criteria/subscription-lifecycle.md` |
| 3 | Webhook Integration | 12% | `scoring/criteria/webhook-integration.md` |
| 4 | Payment Security & PCI | 12% | `scoring/criteria/security-compliance.md` |
| 5 | Pricing & Plan Management | 10% | `scoring/criteria/checkout-billing.md` |
| 6 | Customer Portal | 8% | `scoring/criteria/checkout-billing.md` |
| 7 | Error Handling & Recovery | 8% | `scoring/criteria/webhook-integration.md` |
| 8 | Metered/Usage Billing | 8% | `scoring/criteria/subscription-lifecycle.md` |
| 9 | Testing & Simulation | 6% | `scoring/criteria/security-compliance.md` |
| 10 | Monitoring & Analytics | 6% | `scoring/criteria/security-compliance.md` |

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
| Checkout & Billing, Customer Portal, Pricing | `fix/fix-patterns/checkout-billing.md` |
| Subscription Lifecycle, Metered/Usage Billing | `fix/fix-patterns/subscription-lifecycle.md` |
| Webhook Integration, Error Handling & Recovery | `fix/fix-patterns/webhook-integration.md` |
| Payment Security, Testing, Monitoring | `fix/fix-patterns/security-compliance.md` |

### Verification

Load `references/fix/verification.md` for post-fix checklist, re-scoring protocol, and comparison template.

## Mode: Loop

Automated score-fix cycle. Runs score -> fix -> re-score until target grade is met.

1. **Score** the payment integration (Mode: Score)
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
| Stripe | `references/stripe-patterns.md` -- SDK init, Products/Prices, Checkout Sessions, webhooks |
| Next.js App Router | `references/webhook-patterns.md` -- route handlers, raw body parsing, signature verification |
| Polar + Next.js 16 | `references/polar-nextjs16-reference.md` -- 25 errors (POL-001–025), checkout flows, subscriptions, webhooks, Free/Pro gating, Better Auth plugin, customer portal, CViet patterns |

## Quick Reference -- All Files

### Scoring
- `references/scoring/overview.md` -- Scoring system, grade scale, scorecard format
- `references/scoring/best-practices.md` -- Do/Don't for checkout, subscriptions, webhooks, security
- `references/scoring/scoring-workflow.md` -- 6-step audit process, category mapping, issue format
- `references/scoring/criteria/` -- 4 files covering 10 categories (checkout-billing, subscription-lifecycle, webhook-integration, security-compliance)
- `references/stripe-patterns.md` -- Stripe SDK init, Products/Prices, Checkout, Portal, test clocks
- `references/webhook-patterns.md` -- Webhook verification, event routing, idempotency, retry handling

### Fix
- `references/fix/overview.md` -- How fix works, priority order, score targets
- `references/fix/best-practices.md` -- Fix discipline, safe changes, webhook testing
- `references/fix/implementation-workflow.md` -- 6-step process, priority matrix, which refs to load
- `references/fix/verification.md` -- Post-fix checklist, re-scoring protocol, comparison template
- `references/fix/fix-patterns/` -- 4 files covering 10 categories (checkout-billing, subscription-lifecycle, webhook-integration, security-compliance)

## Output Templates

- Score: `assets/templates/scorecard.md.template` | Fix: `assets/templates/fix-report.md.template`
- Generate: `assets/templates/generated-code.md.template` | Review: `assets/templates/review-report.md.template`
- Migrate: `assets/templates/migration-report.md.template` | Test: `assets/templates/test-suite.md.template`
Fill `{{VARIABLE}}` placeholders with actual values.
