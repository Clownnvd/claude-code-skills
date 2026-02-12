# Auth Scoring — Edge Cases Eval

Verify correct behavior for authentication-specific edge cases.

## Test 1: No Auth Implementation Found

- Run against a codebase with no auth library or session handling
- Verify scoring does not crash
- Verify all auth categories score 0
- Verify output recommends implementing auth before production

## Test 2: Sessions Without Expiry or Rotation

- Provide session config with no `expiresIn` or token rotation
- Verify Session Management scores <= 3 (CRITICAL)
- Verify issue recommends session expiry and rotation settings
- Verify OWASP A07 flagged

## Test 3: Plaintext or Weak Password Hashing

- Provide auth config using MD5/SHA1 or no hashing
- Verify Password Security scores 0-1 (CRITICAL)
- Verify issue specifically names the weak algorithm
- Verify OWASP A02 (Cryptographic Failures) flagged

## Test 4: OAuth Without State Parameter

- Provide OAuth setup missing CSRF state verification
- Verify OAuth scores <= 4
- Verify CSRF & Origin Validation also penalized
- Verify issue explains state parameter requirement

## Test 5: Missing CSRF Protection on Mutations

- Provide forms/routes with POST/PUT/DELETE and no CSRF token
- Verify CSRF & Origin Validation scores <= 3 (CRITICAL)
- Verify OWASP A01 (Broken Access Control) flagged

## Test 6: Better Auth Plugin Configuration

- Provide Better Auth config with missing plugins (e.g., no twoFactor)
- Verify framework-specific adjustments from `better-auth-patterns.md` apply
- Verify 2FA/MFA scores 0 when plugin is absent
- Verify databaseHooks and session cookie config checked

## Test 7: No Rate Limiting on Login/Register

- Provide login and register routes with no rate limiting
- Verify Rate Limiting scores <= 2 (CRITICAL)
- Verify brute force attack vector noted in issues
- Verify fix recommends per-IP and per-account limiting
