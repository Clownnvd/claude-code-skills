# Eval: API Fix Patterns

Verify specific fix patterns from `references/fix-patterns/` produce correct code changes.

## Pattern 1: CSP Hardening (security-auth.md)

**Setup**: Proxy has `Content-Security-Policy` with `'unsafe-inline' 'unsafe-eval'`.

**Steps**:
1. Apply CSP Hardening pattern.
2. Verify `'unsafe-eval'` removed from script-src.
3. Verify nonce generation or `'strict-dynamic'` added.

**Pass**: CSP no longer contains `'unsafe-eval'`. Nonce-based or `strict-dynamic` approach used. Inline scripts still work via nonce.

**Fail**: `'unsafe-eval'` still present, or CSP removed entirely, or page breaks.

## Pattern 2: Per-User Rate Limiting (ratelimit-response-perf.md)

**Setup**: Rate limiter uses only IP-based keys: `${identifier}:${ip}`.

**Steps**:
1. Apply Per-User Rate Limiting pattern.
2. Verify `userId` parameter added to `rateLimit()` function.
3. Verify authenticated routes pass `session.user.id`.

**Pass**: Rate limit key uses `user:${userId}` when authenticated, falls back to `ip:${ip}` when not. At least one authenticated route updated to pass userId.

**Fail**: Only IP-based limiting remains, or userId not passed from route handlers.

## Pattern 3: Machine-Readable Error Codes (input-errors.md)

**Setup**: API returns `{ success: false, error: "Validation failed" }` without a `code` field.

**Steps**:
1. Apply Machine-Readable Error Codes pattern.
2. Verify `errorResponse()` signature updated with `code` parameter.
3. Verify `ErrorCodes` constant object created.
4. Verify at least 3 call sites updated to include error codes.

**Pass**: Error responses include `code` field (e.g., `VALIDATION_ERROR`, `UNAUTHORIZED`). `ErrorCodes` constant defined. Call sites use codes from the constant.

**Fail**: No `code` field in responses, or codes are arbitrary strings not from a central enum.

## Pattern 4: Request-Level Structured Logging (observability-docs-testing.md)

**Setup**: No per-request logging; only Prisma slow query logs exist.

**Steps**:
1. Apply Request-Level Structured Logging pattern.
2. Verify `logRequest()` function created in `src/lib/api/logger.ts`.
3. Verify function logs method, path, status, durationMs, timestamp.
4. Verify at least 2 API route handlers call `logRequest()`.

**Pass**: `logRequest()` emits JSON in production, human-readable in dev. Route handlers log on both success and error paths. Log includes all required fields.

**Fail**: Logger missing fields, or only logs errors, or no route handlers use it.
