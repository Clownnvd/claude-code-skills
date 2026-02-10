# Criteria: CSRF & Origin Validation (12%) + Security Headers (10%)

## 5. CSRF & Origin Validation (12%)

### Score 9-10: Enterprise-grade
- Origin header validated against allowlist
- Referer header used as fallback
- Reject if BOTH Origin AND Referer missing (no silent pass)
- Error response includes `code: "FORBIDDEN"` (not generic 403)
- CSRF validation on ALL state-changing routes (POST/PATCH/DELETE)
- Double-submit cookie pattern or synchronizer token
- Open redirect prevention: block `//` and `/\` in redirect URLs

### Score 7-8: Production-ready
- Origin validation against `NEXT_PUBLIC_APP_URL`
- Referer fallback
- Applied to all mutation endpoints
- Clear error responses

### Score 5-6: Minimum
- Some CSRF protection exists
- Origin or Referer checked
- Applied to most mutation endpoints

### Score 3-4: Below minimum
- CSRF only on some routes
- X-Requested-With fallback (spoofable)
- No open redirect prevention

### Score 0-2: Critical
- No CSRF protection
- State-changing GET requests
- Open redirect vulnerabilities

### Checklist
- [ ] Origin validated against known domain(s)
- [ ] Referer used as fallback when Origin missing
- [ ] Reject when BOTH Origin AND Referer absent
- [ ] Applied to ALL POST/PATCH/DELETE routes
- [ ] Error responses include error code
- [ ] Redirect URLs validated (no `//` or `/\`)
- [ ] CSRF token in forms (if applicable)

## 6. Security Headers (10%)

### Score 9-10: Enterprise-grade
- All headers below set on ALL routes (not just protected pages)
- CSP with strict policy (no `unsafe-eval`, minimal `unsafe-inline`)
- HSTS with `includeSubDomains` + `preload`
- `Permissions-Policy` with all dangerous APIs disabled

### Score 7-8: Production-ready
Headers present on all responses:

| Header | Value |
|--------|-------|
| `X-Frame-Options` | `DENY` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `X-XSS-Protection` | `1; mode=block` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `Content-Security-Policy` | Restrictive policy |
| `Permissions-Policy` | Dangerous APIs disabled |

### Score 5-6: Minimum
- Most headers present
- CSP exists but permissive
- Missing on some routes

### Score 3-4: Below minimum
- Only X-Frame-Options
- No CSP
- Headers only on HTML pages

### Score 0-2: Critical
- No security headers
- `X-Frame-Options: ALLOW`
- CSP with `unsafe-eval`

### Checklist
- [ ] All 7 security headers present
- [ ] Applied via middleware to ALL routes
- [ ] CSP restricts script-src, style-src, connect-src
- [ ] HSTS with includeSubDomains
- [ ] Permissions-Policy disables camera, microphone, geolocation, interest-cohort
- [ ] CORS explicit allowlist (not wildcard `*`)
