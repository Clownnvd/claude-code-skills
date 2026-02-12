# Eval: Caching Fix Verification Loop

Verify the compile-test-rescore cycle, regression detection, and fix idempotency for caching-fix.

## Test 1: Compile + Test Verification

**Setup**: Scorecard with HIGH issue: API routes missing `Cache-Control: no-store` on authenticated responses (Headers & Revalidation 4/10). Apply the NO_CACHE_HEADERS fix from `headers-revalidation.md`.

**Steps**:
1. Apply `Cache-Control: no-store, no-cache, must-revalidate` headers to all authenticated API route responses.
2. Add `export const dynamic = "force-dynamic"` to each API route file.
3. Run `npx tsc --noEmit`. Verify zero type errors.
4. Run `pnpm test`. Verify existing API tests and ISR page tests still pass.

**Pass**: `tsc --noEmit` exits 0. All tests pass. `pnpm build` output shows API routes as dynamic and landing page remains static. No header type mismatches.

**Fail**: Type error from `NextResponse` header methods, test regression in cached page tests, or static routes accidentally forced dynamic.

## Test 2: Re-Score Improvement Verification

**Setup**: Initial caching-scoring scorecard: Headers & Revalidation 4/10, Static/Dynamic/ISR 5/10, React Cache 3/10. Total 45/100 (D+). Apply fixes for cache-control headers and ISR `revalidatePath` after mutations.

**Steps**:
1. Run caching-fix for both issues.
2. Invoke `caching-scoring` to produce a new scorecard.
3. Compare per-category scores: Headers & Revalidation, Static/Dynamic/ISR must increase.
4. Verify CDN, React Cache, Proxy, and all other categories remain at or above pre-fix scores.

**Pass**: Headers & Revalidation >= 7/10 (was 4). Static/Dynamic/ISR >= 7/10 (was 5). No category dropped below its pre-fix score. Total weighted score increased. Comparison uses `references/verification.md` template.

**Fail**: Any unfixed category score decreased, or fixed categories show no improvement.

## Test 3: Regression Detection

**Setup**: Initial scorecard: Headers & Revalidation 7/10, Static/Dynamic/ISR 8/10, React Cache 6/10. Apply a React `cache()` fix that wraps page-level data fetches, accidentally making the landing page dynamic. Static/Dynamic/ISR drops from 8/10 to 4/10.

**Steps**:
1. Apply `cache()` wrapper that adds `cookies()` call inside cached function.
2. Run `caching-scoring` re-score.
3. Verify pipeline detects Static/Dynamic/ISR dropped from 8 to 4 (delta -4).
4. Verify pipeline halts and recommends reverting the cache wrapper.

**Pass**: Pipeline detects the Static/Dynamic/ISR regression. Output flags: category regressed, `pnpm build` shows landing page moved from static to dynamic, recommendation to avoid `cookies()` inside `cache()`. Pipeline does not continue.

**Fail**: Pipeline ignores the ISR regression and continues, or fails to identify that `cookies()` caused the static-to-dynamic shift.

## Test 4: Fix Idempotency

**Setup**: Scorecard with HIGH issue: no `Cache-Control` headers on API responses. All API routes already have `NO_CACHE_HEADERS` applied and `export const dynamic = "force-dynamic"` from a previous fix run.

**Steps**:
1. Run caching-fix with the same cache-control issue.
2. Check `git diff` after the fix attempt.
3. Run `caching-scoring` and compare scores to the post-first-fix scorecard.

**Pass**: No files modified (`git diff` is empty). Score remains identical. Skill reports "already applied" or "no changes needed." No duplicate `Cache-Control` headers or duplicate `dynamic` exports inserted.

**Fail**: Double `Cache-Control` header set, second `export const dynamic` line added, or score changes from the second application.
