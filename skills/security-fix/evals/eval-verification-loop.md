# Eval: Security Fix Verification Loop

Verify the compile-test-rescore cycle, regression detection, and fix idempotency for security-fix.

## Test 1: Compile + Test Verification

**Setup**: Scorecard with CRITICAL issue: no input validation on API routes (Input Validation 2/10). Apply the Zod Validation fix from `input-secrets.md` which adds `schema.safeParse(body)` with `.strict()` to route handlers.

**Steps**:
1. Create Zod schemas for each API route's expected body shape.
2. Add `safeParse` with `.strict()` at the top of each POST/PUT/PATCH handler.
3. Run `npx tsc --noEmit`. Verify zero type errors from new Zod schema types.
4. Run `pnpm test`. Verify existing API tests still pass (request bodies must match new schemas).

**Pass**: `tsc --noEmit` exits 0. All tests pass. Zod schema types exported as `z.infer<typeof schema>`. Error responses return 400 with `VALIDATION_ERROR` code for invalid input. No broken webhook handlers.

**Fail**: Type mismatch between Zod schema and existing handler types, test failure from stricter validation rejecting valid test payloads, or webhook endpoint broken by `.strict()`.

## Test 2: Re-Score Improvement Verification

**Setup**: Initial security-scoring scorecard: Input Validation 2/10, CSP 3/10, Secrets Management 6/10. Total 42/100 (D). Apply fixes for Zod validation (Input Validation) and Content-Security-Policy headers (CSP).

**Steps**:
1. Run security-fix for both issues.
2. Invoke `security-scoring` to produce a new scorecard.
3. Compare per-category scores: Input Validation, CSP must increase.
4. Verify Secrets Management, Webhooks, Monitoring, and all other categories remain at or above pre-fix scores.

**Pass**: Input Validation >= 7/10 (was 2). CSP >= 6/10 (was 3). No category dropped below its pre-fix score. Total weighted score increased. CSP header contains no `'unsafe-eval'` in `script-src`. Comparison uses `references/verification.md` format.

**Fail**: Any unfixed category score decreased, or CSP still contains unsafe directives.

## Test 3: Regression Detection

**Setup**: Initial scorecard: Input Validation 8/10, CSP 7/10, Auth Integration 7/10. Apply a CSP fix that sets `frame-ancestors 'none'` and `form-action 'self'`, breaking the OAuth popup flow. Auth Integration drops from 7/10 to 3/10.

**Steps**:
1. Apply strict CSP that blocks OAuth provider redirect with `form-action 'self'`.
2. Run `security-scoring` re-score.
3. Verify pipeline detects Auth Integration dropped from 7 to 3 (delta -4).
4. Verify pipeline halts and recommends adding OAuth provider domains to `form-action` allowlist.

**Pass**: Pipeline detects the Auth Integration regression. Output flags: OAuth flow broken by CSP, before/after delta shown, recommendation to allowlist OAuth callback domains in `form-action`. Pipeline does not continue.

**Fail**: Pipeline ignores the auth regression and continues, or fails to link CSP changes to the OAuth breakage.

## Test 4: Fix Idempotency

**Setup**: Scorecard with CRITICAL issue: no input validation. All API routes already have Zod `safeParse` with `.strict()` from a previous fix run.

**Steps**:
1. Run security-fix with the same input validation issue.
2. Check `git diff` after the fix attempt.
3. Run `security-scoring` and compare scores to the post-first-fix scorecard.

**Pass**: No files modified (`git diff` is empty). Score remains identical. Skill reports "already applied" or "no changes needed." No duplicate Zod schemas, no duplicate `safeParse` calls, no redundant validation middleware.

**Fail**: Duplicate schema definitions created, double validation on same route, or score changes from the second application.
