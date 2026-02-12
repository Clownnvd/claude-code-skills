# Eval: Security Fix Patterns

Verify specific fix patterns from `references/fix-patterns/` produce correct code changes.

## Pattern 1: Zod Validation on API Routes (input-secrets.md)

**Setup**: API route reads `await req.json()` and uses `body.email` without validation. Accepts any shape.

**Steps**:
1. Apply Zod Validation pattern.
2. Verify schema created in `src/lib/validations/` with `.strict()`.
3. Verify `safeParse()` used (not `parse()` which throws).
4. Verify validation error returns 400 with field-level errors.

**Pass**: Invalid input returns `{ success: false, errors: { email: ["Invalid email"] } }`. Extra fields rejected by `.strict()`. Valid input proceeds to handler.

**Fail**: No validation added, or `.strict()` missing (extra fields accepted), or `parse()` used (uncaught throw).

## Pattern 2: CSP Headers in Proxy (csp-data.md)

**Setup**: No Content-Security-Policy header on any response. Scripts can load from any origin.

**Steps**:
1. Apply CSP pattern.
2. Verify CSP directives include: `default-src 'self'`, `script-src 'self'`, `frame-ancestors 'none'`, `base-uri 'self'`.
3. Verify `style-src 'self' 'unsafe-inline'` for Tailwind compatibility.
4. Verify `connect-src` allows Stripe API.

**Pass**: CSP header present on all responses. Scripts restricted to same origin. iframes blocked via `frame-ancestors 'none'`. Stripe checkout still works via `connect-src` and `frame-src`.

**Fail**: CSP missing, or too permissive (`*` in any directive), or breaks Stripe integration.

## Pattern 3: Open Redirect Blocking (redirect-webhook.md)

**Setup**: `callbackUrl` query parameter used after login redirect. No validation on the URL value. Attacker can set `callbackUrl=https://evil.com`.

**Steps**:
1. Apply Open Redirect Blocking pattern.
2. Verify `isValidRedirectUrl()` function rejects protocol-relative URLs (`//evil.com`).
3. Verify only relative paths starting with `/` accepted.
4. Verify decoded variants also checked (`%2F%2F` blocked).

**Pass**: `callbackUrl=//evil.com` blocked. `callbackUrl=/dashboard` allowed. `callbackUrl=https://evil.com` blocked. Fallback redirects to `/dashboard`.

**Fail**: External URLs accepted, or encoded bypass works, or all callbackUrls rejected.

## Pattern 4: Webhook Signature Verification (redirect-webhook.md)

**Setup**: Stripe webhook handler processes events without verifying the `stripe-signature` header. Any POST to the endpoint is accepted.

**Steps**:
1. Apply Signature Verification pattern.
2. Verify `stripe.webhooks.constructEvent()` called with raw body and signature.
3. Verify missing signature returns 401.
4. Verify invalid signature returns 401 with `"Invalid signature"` message.

**Pass**: Valid Stripe signature accepted. Missing signature rejected with 401. Tampered body rejected. Raw body used (not parsed JSON). Webhook secret from env, not hardcoded.

**Fail**: No signature check, or parsed JSON used instead of raw body, or secret hardcoded.
