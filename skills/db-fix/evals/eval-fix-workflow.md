# Eval: Database Fix Workflow

Verify the db-fix skill correctly parses scoring output, prioritizes, fixes, and re-scores.

## Test 1: Accept Scoring Input

**Setup**: Provide a db-scoring scorecard with 8 issues across Schema Design, Security, Indexing, Operations.

**Steps**:
1. Run db-fix with the scorecard as input.
2. Verify skill parses all 8 issues with correct severity and category.
3. Verify skill identifies the weighted score and grade.

**Pass**: All issues extracted. No issue lost or duplicated.

## Test 2: Fix in Severity Order

**Setup**: Scorecard contains CRITICAL (no SSL on connection string), HIGH (missing FK indexes), MEDIUM (no schema comments).

**Steps**:
1. Run db-fix.
2. Observe fix application order.

**Pass**: SSL enforcement fixed first (CRITICAL), then FK indexes (HIGH, Indexing 12% weight), then schema comments (MEDIUM). No MEDIUM fix applied before all HIGH items resolved.

## Test 3: Fix References Correct Pattern

**Setup**: Issue in "Indexing" category scored 3/10.

**Steps**:
1. Run db-fix.
2. Check which reference file the skill loads.

**Pass**: Skill loads `references/fix-patterns/performance-scaling.md` and applies the "Foreign Key Indexes" pattern. Fix adds `@@index([userId])` to Prisma schema models.

## Test 4: Verification Step Confirms Fix

**Setup**: Apply the "String-to-Enum Conversion" fix from `schema-integrity.md`.

**Steps**:
1. Run db-fix to apply the fix.
2. Check that skill verifies: `prisma validate` passes, migration SQL reviewed, application code updated to use enum.

**Pass**: Skill confirms enum created in schema and application code uses `PaymentMethod.STRIPE` or equivalent. Reports verification result before moving to next fix.

## Test 5: Re-Score Shows Improvement

**Setup**: Initial score 52/100 (grade C-). Apply fixes for 2 CRITICAL + 4 HIGH issues.

**Steps**:
1. Run db-fix through full cycle.
2. Compare before/after scores per category.

**Pass**: Re-score produces a higher weighted score. Each fixed category shows improvement. Final grade is at least B. Report uses `assets/templates/fix-report.md.template` format.
