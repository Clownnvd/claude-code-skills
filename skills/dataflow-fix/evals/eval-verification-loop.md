# Eval: Data Flow Fix Verification Loop

Verify the compile-test-rescore cycle, regression detection, and fix idempotency for dataflow-fix.

## Test 1: Compile + Test Verification

**Setup**: Scorecard with HIGH issue: Prisma queries use `findMany()` without `select`, returning full models to client (Prisma & API 4/10). Apply the Prisma Select fix from `prisma-api.md`.

**Steps**:
1. Add explicit `select` clauses to all `findMany`/`findFirst` calls, returning only fields needed by the UI.
2. Update corresponding TypeScript return types to match narrowed select shape.
3. Run `npx tsc --noEmit`. Verify zero type errors from narrowed Prisma types.
4. Run `pnpm test`. Verify data-fetching tests and component render tests still pass.

**Pass**: `tsc --noEmit` exits 0. All tests pass. Prisma return types match `select` shape (no `Property does not exist` errors). Components receive only declared fields.

**Fail**: Type error from accessing fields excluded by `select`, or component tests fail due to missing properties in narrowed data.

## Test 2: Re-Score Improvement Verification

**Setup**: Initial dataflow-scoring scorecard: RSC Composition 5/10, Prisma & API 4/10, Types & Errors 6/10. Total 50/100 (C-). Apply fixes for RSC boundary extraction (RSC Composition) and Prisma `select` clauses (Prisma & API).

**Steps**:
1. Run dataflow-fix for both issues.
2. Invoke `dataflow-scoring` to produce a new scorecard.
3. Compare per-category scores: RSC Composition, Prisma & API must increase.
4. Verify Types & Errors, State & Cache, Forms & DTOs, and all other categories remain at or above pre-fix scores.

**Pass**: RSC Composition >= 7/10 (was 5). Prisma & API >= 7/10 (was 4). No category dropped below its pre-fix score. Total weighted score increased. Comparison uses `references/verification.md` template.

**Fail**: Any unfixed category score decreased, or fixed categories show no improvement.

## Test 3: Regression Detection

**Setup**: Initial scorecard: RSC Composition 8/10, Prisma & API 7/10, Types & Errors 7/10. Apply an RSC boundary fix that moves a form handler into a Server Component without `"use server"`, breaking client-side form submission. Forms & DTOs drops from 6/10 to 2/10.

**Steps**:
1. Apply RSC extraction that moves `onSubmit` handler into a Server Component file without adding `"use server"` directive.
2. Run `dataflow-scoring` re-score.
3. Verify pipeline detects Forms & DTOs dropped from 6 to 2 (delta -4).
4. Verify pipeline halts and recommends adding `"use server"` or moving handler back to Client Component.

**Pass**: Pipeline detects the Forms & DTOs regression. Output flags: category regressed, identifies missing `"use server"` directive as root cause, recommends corrective action. Pipeline does not continue.

**Fail**: Pipeline ignores the forms regression and continues, or fails to identify the RSC boundary violation.

## Test 4: Fix Idempotency

**Setup**: Scorecard with HIGH issue: Prisma queries lack `select`. All `findMany` calls in `src/lib/db/` already have explicit `select` clauses from a previous fix run.

**Steps**:
1. Run dataflow-fix with the same Prisma select issue.
2. Check `git diff` after the fix attempt.
3. Run `dataflow-scoring` and compare scores to the post-first-fix scorecard.

**Pass**: No files modified (`git diff` is empty). Score remains identical. Skill reports "already applied" or "no changes needed." No duplicate `select` clauses or wrapper functions inserted.

**Fail**: Redundant `select` nesting added, existing select overwritten, or score changes from the second application.
