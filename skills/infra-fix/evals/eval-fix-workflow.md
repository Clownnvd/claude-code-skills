# Eval: Infrastructure Fix Workflow

Verify the infra-fix skill correctly parses scoring output, prioritizes, fixes, and re-scores.

## Test 1: Accept Scoring Input

**Setup**: Provide an infra-scoring scorecard with 7 issues across CI Pipeline, Environment Management, Monitoring.

**Steps**:
1. Run infra-fix with the scorecard as input.
2. Verify skill parses all 7 issues with correct severity and category.
3. Verify skill identifies the weighted score and grade.

**Pass**: All issues extracted. No issue lost or duplicated.

## Test 2: Fix in Severity Order

**Setup**: Scorecard contains CRITICAL (no CI pipeline), HIGH (no env validation), MEDIUM (no health endpoint).

**Steps**:
1. Run infra-fix.
2. Observe fix application order.

**Pass**: CI pipeline fixed first (CRITICAL), then env validation (HIGH, Environment Mgmt 12% weight), then health endpoint (MEDIUM). No MEDIUM fix applied before all HIGH items resolved.

## Test 3: Fix References Correct Pattern

**Setup**: Issue in "CI Pipeline" category scored 2/10.

**Steps**:
1. Run infra-fix.
2. Check which reference file the skill loads.

**Pass**: Skill loads `references/fix-patterns/ci-cd.md` and applies the "GitHub Actions CI Workflow" pattern. Fix creates `.github/workflows/ci.yml` with parallel lint/typecheck/test jobs.

## Test 4: Verification Step Confirms Fix

**Setup**: Apply the "Env Validation with Zod" fix from `env-monitoring.md`.

**Steps**:
1. Run infra-fix to apply the fix.
2. Check that skill verifies: env.ts schema matches .env.example keys, app starts without env errors.

**Pass**: Skill confirms Zod schema covers all required env vars. Reports verification result before moving to next fix.

## Test 5: Re-Score Shows Improvement

**Setup**: Initial score 40/100 (grade D). Apply fixes for 3 CRITICAL + 2 HIGH issues.

**Steps**:
1. Run infra-fix through full cycle.
2. Compare before/after scores per category.

**Pass**: Re-score produces a higher weighted score. Each fixed category shows improvement. Final grade is at least B. Report uses `assets/templates/fix-report.md.template` format.
