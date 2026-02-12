# Eval: Auth Fix Patterns

Verify specific fix patterns from `references/fix-patterns/` produce correct code changes.

## Pattern 1: Cookie Security Flags (sessions-passwords.md)

**Setup**: Better Auth config missing `useSecureCookies` and explicit `defaultCookieSameSite`.

**Steps**:
1. Apply Cookie Security Flags pattern.
2. Verify `advanced.useSecureCookies` set to `process.env.NODE_ENV === "production"`.
3. Verify `advanced.defaultCookieSameSite` set to `"lax"` (not `"strict"`, which breaks OAuth).

**Pass**: Cookies use `Secure` flag in production, `SameSite=Lax` always. Cookie prefix configured.

**Fail**: `SameSite` set to `"strict"` (breaks OAuth redirects), or `useSecureCookies` hardcoded to `true` (breaks dev).

## Pattern 2: Origin Validation in Proxy (csrf-headers.md)

**Setup**: No CSRF protection on state-changing requests. POST to `/api/auth/*` accepts any origin.

**Steps**:
1. Apply Origin Validation pattern.
2. Verify `validateOrigin()` function added to proxy.ts.
3. Verify safe methods (GET, HEAD, OPTIONS) skip validation.
4. Verify POST requests require matching Origin or Referer header.

**Pass**: State-changing requests rejected when Origin header mismatches `BETTER_AUTH_URL`. GET requests pass through. Missing Origin + missing Referer on POST returns false.

**Fail**: All requests checked (breaks GETs), or validation only checks Origin but not Referer fallback.

## Pattern 3: Strict Auth Rate Limits (ratelimit-audit.md)

**Setup**: No rate limiting on login, signup, or password reset endpoints.

**Steps**:
1. Apply Strict Auth Rate Limits pattern.
2. Verify `AUTH_RATE_LIMITS` config defined with strict (5 req/15min), standard (100 req/15min), verification (3 req/1hr) tiers.
3. Verify sign-in and sign-up routes use strict limits.

**Pass**: Login endpoint rejects after 5 attempts in 15 minutes. Returns 429 with `Retry-After` header. Verification email endpoint limited to 3/hour.

**Fail**: Rate limits too permissive (>20 for auth), or no differentiation between auth and general routes.

## Pattern 4: Two-Layer Auth Pattern (authz-2fa.md)

**Setup**: No proxy-level cookie check. All auth relies on API route `getSession()` calls.

**Steps**:
1. Apply Two-Layer Auth pattern.
2. Verify Layer 1: Proxy checks `better-auth.session_token` cookie for protected paths.
3. Verify Layer 2: API routes use `requireAuth()` for full session validation.
4. Verify redirect includes `callbackUrl` search parameter.

**Pass**: Unauthenticated requests to `/dashboard` redirect to `/sign-in?callbackUrl=/dashboard` at proxy level. API routes still validate session with DB lookup via `requireAuth()`.

**Fail**: Only one layer exists, or proxy does DB lookup (too heavy), or callbackUrl missing.
