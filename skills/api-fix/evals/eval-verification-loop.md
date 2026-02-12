# Eval: API Fix Verification Loop

Verify the compile-test-rescore cycle, regression detection, and fix idempotency for api-fix.

## Test 1: Compile + Test Verification

**Setup**: Scorecard with HIGH issue: API routes missing CSP headers (Security 5/10). Apply the CSP Hardening fix from `security-auth.md` which adds `Content-Security-Policy` to the proxy middleware.

**Steps**:
1. Apply the CSP header fix to `middleware.ts` or proxy config.
2. Run `npx tsc --noEmit`. Verify zero type errors.
3. Run `pnpm test`. Verify all existing API route tests still pass.
4. Verify new CSP header string is valid (no syntax errors in directives).

**Pass**: `tsc --noEmit` exits 0. Test suite passes with same count (no tests deleted). CSP directive parses without error. No broken imports from middleware changes.

**Fail**: Type error in header types, test regression in route handlers, or malformed CSP string.

## Test 2: Re-Score Improvement Verification

**Setup**: Initial api-scoring scorecard: Security 5/10, Rate Limiting 4/10, Input Validation 6/10. Total 58/100 (C). Apply fixes for CSP headers (Security) and per-user rate limiting (Rate Limiting).

**Steps**:
1. Run api-fix for both issues.
2. Invoke `api-scoring` to produce a new scorecard.
3. Compare per-category scores: Security, Rate Limiting must increase.
4. Verify Input Validation, Error Handling, and all other categories remain at or above pre-fix scores.

**Pass**: Security >= 7/10 (was 5). Rate Limiting >= 6/10 (was 4). No category dropped below its pre-fix score. Total weighted score increased. Comparison table matches `references/verification.md` template.

**Fail**: Any unfixed category score decreased, or fixed categories show no improvement.

## Test 3: Regression Detection

**Setup**: Initial scorecard: Security 7/10, Rate Limiting 6/10, Performance 8/10. Apply a rate limiting fix that adds synchronous Redis lookups to every request, regressing Performance from 8/10 to 5/10.

**Steps**:
1. Apply the rate limiting fix with blocking Redis calls.
2. Run `api-scoring` re-score.
3. Verify pipeline detects Performance dropped from 8 to 5 (delta -3).
4. Verify pipeline halts further fixes and flags the regression.

**Pass**: Pipeline detects the Performance regression. Output includes: which category regressed, the before/after delta, and a recommendation to revert the rate limiting change. Pipeline does not continue to the next fix.

**Fail**: Pipeline ignores the Performance drop and continues fixing, or reports overall improvement without flagging the per-category regression.

## Test 4: Fix Idempotency

**Setup**: Scorecard with HIGH issue: no per-user rate limiting. The `rateLimit()` function in `src/lib/api/rate-limit.ts` already has `userId` parameter and key prefix `user:${userId}` from a previous fix run.

**Steps**:
1. Run api-fix with the same rate limiting issue.
2. Check `git diff` after the fix attempt.
3. Run `api-scoring` and compare scores to the post-first-fix scorecard.

**Pass**: No files modified (`git diff` is empty or unchanged). Score remains identical to post-first-fix score. Skill reports "already applied" or "no changes needed" for the rate limiting item. No duplicate code blocks inserted.

**Fail**: Duplicate `userId` parameter added, wrapper function re-created, or score changes from the second application.
