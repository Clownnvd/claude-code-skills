# Criteria: CSP (10%) + Data Protection (10%)

## Category 5: Content Security Policy (Weight: 10%)

### Enterprise (9-10)
1. CSP header set in middleware on all responses
2. `default-src 'self'` baseline
3. `script-src 'self'` (no `unsafe-eval`, no `unsafe-inline` without nonce)
4. `frame-ancestors 'none'` (prevents clickjacking)
5. `style-src 'self' 'unsafe-inline'` (Tailwind needs inline)
6. `img-src 'self' data: https:` (controlled image sources)
7. `connect-src 'self'` + specific API domains
8. `X-Content-Type-Options: nosniff`
9. `X-Frame-Options: DENY` (fallback for older browsers)
10. CSP report-uri or report-to configured for monitoring

### Scoring
- 10: All 10 items met
- 9: 9 items met (report-uri optional for 9)
- 8: Good CSP but missing 1-2 directives
- 7: CSP present but too permissive
- 6: CSP only on some routes
- 5: Minimal CSP (only default-src)
- 4: CSP allows unsafe-eval
- 3: No frame-ancestors
- 2: Very permissive CSP (`* sources`)
- 1: CSP header present but ineffective
- 0: No CSP header at all

### Deduction Examples
- -3: No CSP header on any route
- -2: `script-src 'unsafe-eval'`
- -2: Missing `frame-ancestors`
- -1: Missing `X-Content-Type-Options: nosniff`
- -1: CSP only on HTML pages, not API routes
- -1: No report-uri/report-to

---

## Category 6: Data Protection & PII (Weight: 10%)

### Enterprise (9-10)
1. Prisma queries use `select` to limit returned fields
2. HTTPS enforced (HSTS header in production)
3. No PII logged (emails, IPs beyond operational need)
4. Internal database IDs not exposed in API responses
5. Stripe IDs and external service IDs not leaked to client
6. Password fields never returned in any response
7. User objects sanitized before sending to client
8. `force-dynamic` on pages showing private data
9. Sensitive data not stored in localStorage/cookies unnecessarily
10. Data deletion/export capability (GDPR readiness)

### Scoring
- 10: All 10 items met
- 9: 9 items met
- 8: Minor data exposure (non-sensitive internal IDs)
- 7: Some Prisma queries without `select`
- 6: 1 route leaking unnecessary data
- 5: Multiple routes returning full Prisma objects
- 4: Stripe/external IDs exposed to client
- 3: PII logged in production
- 2: Passwords or tokens in responses
- 1: Sensitive data in localStorage unencrypted
- 0: Passwords or secrets returned in API responses

### Deduction Examples
- -4: Password hash returned in API response
- -3: Full Prisma user object returned (includes all fields)
- -2: Stripe customer ID exposed to client-side JavaScript
- -2: PII (emails) in server logs
- -1: Missing HSTS header
- -1: Internal database PKs in API responses
