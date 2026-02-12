# Eval: Security Fix Workflow

Verify the security-fix skill correctly parses scoring output, prioritizes, fixes, and re-scores.

## Test 1: Accept Scoring Input

**Setup**: Provide a security-scoring scorecard with 8 issues across Input Validation, CSP, Webhooks, Monitoring.

**Steps**:
1. Run security-fix with the scorecard as input.
2. Verify skill parses all 8 issues with correct severity and category.
3. Verify skill identifies the weighted score and grade.

**Pass**: All issues extracted. No issue lost or duplicated.

## Test 2: Fix in Severity Order

**Setup**: Scorecard contains CRITICAL (no input validation on API routes), HIGH (missing CSP headers), MEDIUM (no request IDs in logs).

**Steps**:
1. Run security-fix.
2. Observe fix application order.

**Pass**: Input validation fixed first (CRITICAL), then CSP headers (HIGH, CSP 12% weight), then request IDs (MEDIUM). No MEDIUM fix applied before all HIGH items resolved.

## Test 3: Fix References Correct Pattern

**Setup**: Issue in "Input Validation" category scored 3/10.

**Steps**:
1. Run security-fix.
2. Check which reference file the skill loads.

**Pass**: Skill loads `references/fix-patterns/input-secrets.md` and applies the "Add Zod Validation to API Route" pattern. Fix adds `schema.safeParse(body)` with `.strict()` to route handlers.

## Test 4: Verification Step Confirms Fix

**Setup**: Apply the "CSP Directives" fix from `csp-data.md`.

**Steps**:
1. Run security-fix to apply the fix.
2. Check that skill verifies: CSP header present on responses, no unsafe-eval in script-src, frame-ancestors set to 'none'.

**Pass**: Skill confirms Content-Security-Policy header added to proxy. Reports verification result before moving to next fix.

## Test 5: Re-Score Shows Improvement

**Setup**: Initial score 48/100 (grade D+). Apply fixes for 3 CRITICAL + 3 HIGH issues.

**Steps**:
1. Run security-fix through full cycle.
2. Compare before/after scores per category.

**Pass**: Re-score produces a higher weighted score. Each fixed category shows improvement. Final grade is at least B+. Report uses `assets/templates/fix-report.md.template` format.
