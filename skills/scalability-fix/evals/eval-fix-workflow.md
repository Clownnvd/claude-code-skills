# Eval: Scalability Fix Workflow

Verify the scalability-fix skill correctly parses scoring output, prioritizes, fixes, and re-scores.

## Test 1: Accept Scoring Input

**Setup**: Provide a scalability-scoring scorecard with 6 issues across Bundle Size, RSC Architecture, Concurrency.

**Steps**:
1. Run scalability-fix with the scorecard as input.
2. Verify skill parses all 6 issues with correct severity and category.
3. Verify skill identifies the weighted score and grade.

**Pass**: All issues extracted. No issue lost or duplicated.

## Test 2: Fix in Severity Order

**Setup**: Scorecard contains CRITICAL (entire page is "use client"), HIGH (sequential DB queries in layout), MEDIUM (no event listener cleanup).

**Steps**:
1. Run scalability-fix.
2. Observe fix application order.

**Pass**: RSC extraction fixed first (CRITICAL), then parallel queries (HIGH, RSC 15% weight), then event cleanup (MEDIUM). No MEDIUM fix applied before all HIGH items resolved.

## Test 3: Fix References Correct Pattern

**Setup**: Issue in "Bundle Size" category scored 5/10.

**Steps**:
1. Run scalability-fix.
2. Check which reference file the skill loads.

**Pass**: Skill loads `references/fix-patterns/bundle-images.md` and applies the "Dynamic Import Heavy Libraries" pattern. Fix converts top-level imports to `next/dynamic` with `{ ssr: false }`.

## Test 4: Verification Step Confirms Fix

**Setup**: Apply the "Suspense Boundaries" fix from `rsc-dbperf.md`.

**Steps**:
1. Run scalability-fix to apply the fix.
2. Check that skill verifies: `pnpm build` succeeds, page renders with streaming, no layout shift.

**Pass**: Skill confirms Suspense wrapper added with appropriate fallback. Reports verification result before moving to next fix.

## Test 5: Re-Score Shows Improvement

**Setup**: Initial score 56/100 (grade C). Apply fixes for 1 CRITICAL + 3 HIGH issues.

**Steps**:
1. Run scalability-fix through full cycle.
2. Compare before/after scores per category.

**Pass**: Re-score produces a higher weighted score. Each fixed category shows improvement. Final grade is at least B+. Report uses `assets/templates/fix-report.md.template` format.
