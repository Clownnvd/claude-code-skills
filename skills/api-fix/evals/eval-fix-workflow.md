# Eval: API Fix Workflow

Verify the api-fix skill correctly parses scoring output, prioritizes, fixes, and re-scores.

## Test 1: Accept Scoring Input

**Setup**: Provide an api-scoring scorecard with 6 issues across Security, Input Validation, Rate Limiting.

**Steps**:
1. Run api-fix with the scorecard as input.
2. Verify skill parses all 6 issues with correct severity and category.
3. Verify skill identifies the weighted score and grade.

**Pass**: All issues extracted. No issue lost or duplicated.

## Test 2: Fix in Severity Order

**Setup**: Scorecard contains CRITICAL (CSP unsafe-eval), HIGH (no per-user rate limiting), MEDIUM (missing error codes).

**Steps**:
1. Run api-fix.
2. Observe fix application order.

**Pass**: CSP fix applied first (CRITICAL), then rate limiting (HIGH, 10% weight), then error codes (MEDIUM). No MEDIUM fix applied before all HIGH items resolved.

## Test 3: Fix References Correct Pattern

**Setup**: Issue in "Rate Limiting" category scored 4/10.

**Steps**:
1. Run api-fix.
2. Check which reference file the skill loads.

**Pass**: Skill loads `references/fix-patterns/ratelimit-response-perf.md` and applies the "Per-User Rate Limiting" pattern. Fix code matches the pattern structure (userId parameter, key prefix).

## Test 4: Verification Step Confirms Fix

**Setup**: Apply the "Content-Type Enforcement" fix from `input-errors.md`.

**Steps**:
1. Run api-fix to apply the fix.
2. Check that skill verifies: TypeScript compiles, existing tests pass, the specific criterion improves.

**Pass**: Skill runs `pnpm tsc --noEmit` or equivalent. Reports verification result before moving to next fix.

## Test 5: Re-Score Shows Improvement

**Setup**: Initial score 62/100 (grade C+). Apply fixes for 3 CRITICAL + 2 HIGH issues.

**Steps**:
1. Run api-fix through full cycle.
2. Compare before/after scores per category.

**Pass**: Re-score produces a higher weighted score. Each fixed category shows improvement. Final grade is at least B. Report uses `assets/templates/fix-report.md.template` format.
