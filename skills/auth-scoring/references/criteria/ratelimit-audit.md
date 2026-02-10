# Criteria: Rate Limiting — Auth Routes (12%) + Audit Logging (8%)

## 7. Rate Limiting on Auth Routes (12%)

### Score 9-10: Enterprise-grade
- Strict rate limiting on all auth mutation endpoints:
  - Login: 5/min per IP
  - Sign-up: 3/min per IP
  - Password reset: 3/min per IP
  - Email verification resend: 3/min per user
- Standard rate limiting on auth read endpoints (10-20/min)
- Per-user rate limiting on authenticated routes
- Rate limit response includes `Retry-After` header
- Account lockout after N failed attempts (with unlock mechanism)
- Distributed rate limiting (Redis/Upstash, not in-memory)

### Score 7-8: Production-ready
- Rate limiting on login, sign-up, password reset
- Strict limits (≤ 5/min) on mutation endpoints
- Distributed store (Upstash Redis)
- 429 response with clear error message

### Score 5-6: Minimum
- Rate limiting on login endpoint
- Some form of request throttling
- 429 status returned

### Score 3-4: Below minimum
- Rate limiting only on some auth routes
- In-memory store (resets on deploy)
- No distinction between strict/standard rates

### Score 0-2: Critical
- No rate limiting on auth routes
- Brute-force login possible
- No account lockout

### Checklist
- [ ] Login endpoint: strict rate limit (≤ 5/min)
- [ ] Sign-up endpoint: strict rate limit
- [ ] Password reset: strict rate limit
- [ ] Email verification resend: rate limited
- [ ] Distributed store (Redis/Upstash, not memory)
- [ ] 429 response with `Retry-After` or clear message
- [ ] Per-user rate limiting on authenticated auth routes

## 8. Audit Logging (8%)

### Score 9-10: Enterprise-grade
- All auth events logged: sign_in, sign_up, sign_out, password_reset, email_verified, oauth_link
- Structured JSON format in production
- userId included (never PII like email/name)
- IP address logged (from trusted header)
- Failed auth attempts logged with `warn` level
- Log aggregation ready (parseable by ELK/Datadog/etc.)
- Separate audit log (not mixed with app logs)

### Score 7-8: Production-ready
- sign_in, sign_up, password_reset logged
- Structured format with userId
- Severity levels (info vs warn)
- No PII in logs

### Score 5-6: Minimum
- Some auth events logged
- Basic format
- Console output

### Score 3-4: Below minimum
- Only errors logged
- PII in logs (email, name)
- No structure (free text)

### Score 0-2: Critical
- No auth event logging
- Passwords or tokens in logs
- No ability to trace auth activity

### Checklist
- [ ] All auth events logged (sign_in, sign_up, sign_out, password_reset, etc.)
- [ ] Structured JSON in production
- [ ] userId included, no PII (email, name, password)
- [ ] IP address from trusted header (last in X-Forwarded-For)
- [ ] Failed attempts at `warn` level
- [ ] Better Auth `databaseHooks` configured for events
