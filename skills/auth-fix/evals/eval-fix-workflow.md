# Eval: Auth Fix Workflow

Verify the auth-fix skill correctly parses scoring output, prioritizes, fixes, and re-scores.

## Test 1: Accept Scoring Input

**Setup**: Provide an auth-scoring scorecard with 7 issues across Session Management, CSRF, Rate Limiting.

**Steps**:
1. Run auth-fix with the scorecard as input.
2. Verify skill parses all 7 issues with correct severity and category.
3. Verify skill identifies the weighted score and grade.

**Pass**: All issues extracted. No issue lost or duplicated.

## Test 2: Fix in Severity Order

**Setup**: Scorecard contains CRITICAL (no CSRF validation on POST), HIGH (missing cookie security flags), MEDIUM (no audit logging).

**Steps**:
1. Run auth-fix.
2. Observe fix application order.

**Pass**: CSRF fix applied first (CRITICAL), then cookie flags (HIGH, Session Management 15% weight), then audit logging (MEDIUM). No MEDIUM fix applied before all HIGH items resolved.

## Test 3: Fix References Correct Pattern

**Setup**: Issue in "Session Management" category scored 4/10.

**Steps**:
1. Run auth-fix.
2. Check which reference file the skill loads.

**Pass**: Skill loads `references/fix-patterns/sessions-passwords.md` and applies the "Cookie Security Flags" pattern. Fix modifies Better Auth config with `useSecureCookies` and `defaultCookieSameSite`.

## Test 4: Verification Step Confirms Fix

**Setup**: Apply the "Origin Validation in Proxy" fix from `csrf-headers.md`.

**Steps**:
1. Run auth-fix to apply the fix.
2. Check that skill verifies: code compiles, Better Auth config valid, auth flow not broken.

**Pass**: Skill confirms `validateOrigin()` function added to proxy.ts. Reports verification result before moving to next fix.

## Test 5: Re-Score Shows Improvement

**Setup**: Initial score 58/100 (grade C). Apply fixes for 2 CRITICAL + 3 HIGH issues.

**Steps**:
1. Run auth-fix through full cycle.
2. Compare before/after scores per category.

**Pass**: Re-score produces a higher weighted score. Each fixed category shows improvement. Final grade is at least B+. Report uses `assets/templates/fix-report.md.template` format.
