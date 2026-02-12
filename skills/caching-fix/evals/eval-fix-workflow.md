# Eval: Caching Fix Workflow

Verify the caching-fix skill correctly parses scoring output, prioritizes, fixes, and re-scores.

## Test 1: Accept Scoring Input

**Setup**: Provide a caching-scoring scorecard with 5 issues across Cache-Control Headers, Static/Dynamic, Request Dedup.

**Steps**:
1. Run caching-fix with the scorecard as input.
2. Verify skill parses all 5 issues with correct severity and category.
3. Verify skill identifies the weighted score and grade.

**Pass**: All issues extracted. No issue lost or duplicated.

## Test 2: Fix in Severity Order

**Setup**: Scorecard contains CRITICAL (authenticated data cached publicly), HIGH (no revalidation after mutations), MEDIUM (no cache() dedup).

**Steps**:
1. Run caching-fix.
2. Observe fix application order.

**Pass**: Public cache leak fixed first (CRITICAL), then revalidation (HIGH, 15% weight), then cache() dedup (MEDIUM). No MEDIUM fix applied before all HIGH items resolved.

## Test 3: Fix References Correct Pattern

**Setup**: Issue in "Cache-Control Headers" category scored 3/10.

**Steps**:
1. Run caching-fix.
2. Check which reference file the skill loads.

**Pass**: Skill loads `references/fix-patterns/headers-revalidation.md` and applies the "NO_CACHE_HEADERS" pattern. Fix adds `Cache-Control: private, no-store` to authenticated API responses.

## Test 4: Verification Step Confirms Fix

**Setup**: Apply the "Static Page Conversion" fix from `static-dynamic-isr.md`.

**Steps**:
1. Run caching-fix to apply the fix.
2. Check that skill verifies: `pnpm build` output shows correct static/dynamic classification.

**Pass**: Skill checks build output for static indicator on the converted page. Reports verification result before moving to next fix.

## Test 5: Re-Score Shows Improvement

**Setup**: Initial score 55/100 (grade C). Apply fixes for 1 CRITICAL + 3 HIGH issues.

**Steps**:
1. Run caching-fix through full cycle.
2. Compare before/after scores per category.

**Pass**: Re-score produces a higher weighted score. Each fixed category shows improvement. Final grade is at least B. Report uses `assets/templates/fix-report.md.template` format.
