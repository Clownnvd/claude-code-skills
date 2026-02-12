# Security + Authentication & Authorization

Covers categories 1 (Security, 20%) and 2 (Auth & AuthZ, 15%).

## Category 1: Security (20%)

### Checklist (subtract 1 per missing item from baseline 5)

- [ ] TLS enforced; HSTS header with `max-age >= 31536000; includeSubDomains`
- [ ] Security headers on ALL responses: `X-Content-Type-Options`, `X-Frame-Options`, `CSP`, `Referrer-Policy`, `Permissions-Policy`
- [ ] CORS explicit allowlist (never wildcard `*` on authenticated endpoints)
- [ ] CSRF protection on state-changing endpoints (Origin/Referer validation)
- [ ] No secrets in responses, errors, or headers (API keys, tokens, passwords, internal URLs)
- [ ] Request size limits enforced per-endpoint (body, headers, URL)
- [ ] No known CVEs in production dependencies
- [ ] Webhook signature verification for all inbound webhooks

### Bonus (add 1 per item, max 10)

- [ ] CSP with nonces or strict dynamic
- [ ] Subresource Integrity (SRI) on external scripts
- [ ] Automated dependency scanning in CI (Snyk, npm audit, etc.)

### OWASP API Top 10 Coverage

| Risk | What to check |
|------|---------------|
| API2: Broken Auth | Token validation, credential stuffing protection |
| API6: Sensitive Flows | Business-critical actions protected (purchase, invite) |
| API7: SSRF | URL inputs validated, internal IPs blocked |
| API8: Misconfiguration | Default configs changed, debug disabled in prod |

### Scoring Guide

| Score | Criteria |
|-------|----------|
| 0-3 | Missing TLS, no CSRF, secrets leaked, no security headers |
| 4-5 | Basic headers present but gaps (missing CSP, weak CORS) |
| 6-7 | All headers, CSRF, CORS configured; minor gaps |
| 8-9 | Full OWASP coverage, dependency scanning, request limits |
| 10 | All above + automated security tests in CI + CSP with nonces |

---

## Category 2: Authentication & Authorization (15%)

### Checklist

- [ ] Auth on every endpoint that accesses user data (no unprotected routes)
- [ ] Token validation: signature, expiry, issuer checked per-request
- [ ] Object-level auth (BOLA): every resource ID verified against current user
- [ ] Function-level auth (BFLA): admin endpoints separated, role checks at handler level
- [ ] Property-level auth (BOPLA): write operations only accept permitted fields
- [ ] Session: HttpOnly + Secure + SameSite cookies; token rotation on privilege change
- [ ] Logout invalidates session immediately
- [ ] Default-deny access model (explicit grants only)

### Bonus

- [ ] Multi-tenancy isolation at data layer
- [ ] Refresh token rotation with one-time use
- [ ] Audit log of auth events (login, logout, failed attempts)

### Scoring Guide

| Score | Criteria |
|-------|----------|
| 0-3 | Unprotected endpoints, no BOLA checks, tokens not validated |
| 4-5 | Auth present but inconsistent; some endpoints unprotected |
| 6-7 | All endpoints protected; BOLA checks present; basic session mgmt |
| 8-9 | Full BOLA + BFLA + BOPLA; secure sessions; audit logging |
| 10 | All above + multi-tenancy isolation + automated BOLA tests in CI |
