# Eval: Auth Fix Verification Loop

Verify the compile-test-rescore cycle, regression detection, and fix idempotency for auth-fix.

## Test 1: Compile + Test Verification

**Setup**: Scorecard with CRITICAL issue: sessions lack CSRF protection (CSRF & Headers 3/10). Apply the CSRF token fix from `csrf-headers.md` which adds token generation, validation middleware, and hidden form fields.

**Steps**:
1. Apply CSRF token generation to session creation in `src/lib/auth.ts`.
2. Add CSRF validation middleware to state-changing API routes.
3. Run `npx tsc --noEmit`. Verify zero type errors from new token types.
4. Run `pnpm test`. Verify login, logout, and OAuth callback tests still pass.

**Pass**: `tsc --noEmit` exits 0. All auth flow tests pass. CSRF token type is exported and consistent across middleware and session module. No broken imports.

**Fail**: Type mismatch between token shape in session vs middleware, or existing auth tests fail due to missing CSRF token in test fixtures.

## Test 2: Re-Score Improvement Verification

**Setup**: Initial auth-scoring scorecard: Sessions 5/10, CSRF & Headers 3/10, Passwords 7/10. Total 52/100 (C-). Apply fixes for session `httpOnly`/`secure` flags (Sessions) and CSRF token validation (CSRF & Headers).

**Steps**:
1. Run auth-fix for both issues.
2. Invoke `auth-scoring` to produce a new scorecard.
3. Compare per-category scores: Sessions, CSRF & Headers must increase.
4. Verify Passwords, OAuth, Rate Limiting, and all other categories remain at or above pre-fix scores.

**Pass**: Sessions >= 7/10 (was 5). CSRF & Headers >= 6/10 (was 3). No category dropped below its pre-fix score. Total weighted score increased. Comparison uses `references/verification.md` template.

**Fail**: Any unfixed category score decreased, or fixed categories show no improvement.

## Test 3: Regression Detection

**Setup**: Initial scorecard: Sessions 8/10, OAuth 7/10, CSRF & Headers 5/10. Apply a CSRF fix that adds strict `SameSite=Strict` cookies, breaking the OAuth callback flow. OAuth drops from 7/10 to 3/10.

**Steps**:
1. Apply CSRF fix with `SameSite=Strict` on all cookies including OAuth state.
2. Run `auth-scoring` re-score.
3. Verify pipeline detects OAuth dropped from 7 to 3 (delta -4).
4. Verify pipeline halts and recommends reverting the cookie change.

**Pass**: Pipeline detects the OAuth regression. Output flags: OAuth category regressed, before/after delta shown, recommendation to use `SameSite=Lax` for OAuth cookies instead. Pipeline does not continue fixing.

**Fail**: Pipeline ignores the OAuth drop and continues, or reports net improvement without flagging the per-category regression.

## Test 4: Fix Idempotency

**Setup**: Scorecard with CRITICAL issue: no CSRF protection. The `src/lib/auth.ts` already generates CSRF tokens and `src/middleware.ts` already validates them from a previous fix run.

**Steps**:
1. Run auth-fix with the same CSRF issue.
2. Check `git diff` after the fix attempt.
3. Run `auth-scoring` and compare scores to the post-first-fix scorecard.

**Pass**: No files modified (`git diff` is empty). Score remains identical. Skill reports "already applied" or "no changes needed" for the CSRF item. No duplicate token generation or validation logic inserted.

**Fail**: Second CSRF middleware added, duplicate token field in session, or score changes from the second application.
