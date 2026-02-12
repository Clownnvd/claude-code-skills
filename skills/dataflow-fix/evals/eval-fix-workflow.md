# Eval: Data Flow Fix Workflow

Verify the dataflow-fix skill correctly parses scoring output, prioritizes, fixes, and re-scores.

## Test 1: Accept Scoring Input

**Setup**: Provide a dataflow-scoring scorecard with 6 issues across RSC Fetching, Prisma Optimization, Type Safety.

**Steps**:
1. Run dataflow-fix with the scorecard as input.
2. Verify skill parses all 6 issues with correct severity and category.
3. Verify skill identifies the weighted score and grade.

**Pass**: All issues extracted. No issue lost or duplicated.

## Test 2: Fix in Severity Order

**Setup**: Scorecard contains CRITICAL (client fetch where RSC needed), HIGH (no select on Prisma queries), MEDIUM (missing error.tsx boundaries).

**Steps**:
1. Run dataflow-fix.
2. Observe fix application order.

**Pass**: RSC conversion fixed first (CRITICAL), then Prisma select (HIGH, 12% weight), then error boundaries (MEDIUM). No MEDIUM fix applied before all HIGH items resolved.

## Test 3: Fix References Correct Pattern

**Setup**: Issue in "Prisma Optimization" category scored 4/10.

**Steps**:
1. Run dataflow-fix.
2. Check which reference file the skill loads.

**Pass**: Skill loads `references/fix-patterns/prisma-api.md` and applies the "Add select to Every Query" pattern. Fix adds explicit `select` clauses to Prisma calls.

## Test 4: Verification Step Confirms Fix

**Setup**: Apply the "Push use client to Leaves" fix from `rsc-composition.md`.

**Steps**:
1. Run dataflow-fix to apply the fix.
2. Check that skill verifies: TypeScript compiles, "use client" only on leaf components, server data still flows correctly.

**Pass**: Skill confirms the page component no longer has "use client" directive. Reports verification result before moving to next fix.

## Test 5: Re-Score Shows Improvement

**Setup**: Initial score 60/100 (grade C+). Apply fixes for 2 CRITICAL + 2 HIGH issues.

**Steps**:
1. Run dataflow-fix through full cycle.
2. Compare before/after scores per category.

**Pass**: Re-score produces a higher weighted score. Each fixed category shows improvement. Final grade is at least B+. Report uses `assets/templates/fix-report.md.template` format.
