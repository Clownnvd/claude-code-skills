# Criteria: Session Management (15%) + Password Security (12%)

## 1. Session Management (15%)

### Score 9-10: Enterprise-grade
- HttpOnly + Secure + SameSite=Lax/Strict cookies
- Server-side session storage (DB, not JWT-only)
- Session expiry configured (idle + absolute)
- Session revocation on password change
- Concurrent session limiting or detection
- Session fixation protection (new ID on auth state change)

### Score 7-8: Production-ready
- HttpOnly + Secure cookies
- Server-side sessions with DB adapter
- Reasonable expiry (7-30 days)
- Session tokens with sufficient entropy (≥128 bits)

### Score 5-6: Minimum
- Cookie-based sessions exist
- Some expiry mechanism
- Basic HTTPS enforcement

### Score 3-4: Below minimum
- Long-lived sessions with no expiry
- Session tokens in localStorage (XSS vulnerable)
- No session revocation capability

### Score 0-2: Critical
- No session management
- Tokens in URL parameters
- Predictable session IDs

### Checklist
- [ ] Session cookie: HttpOnly, Secure, SameSite
- [ ] Server-side session storage (not client-only JWT)
- [ ] Session expiry (idle timeout + absolute lifetime)
- [ ] Session invalidation on logout
- [ ] Session revocation on password change
- [ ] CSRF token tied to session
- [ ] Session rotation after privilege escalation

## 2. Password Security (12%)

### Score 9-10: Enterprise-grade
- Bcrypt/Argon2/scrypt hashing (cost factor ≥ 10)
- Minimum 8 chars + complexity requirements enforced
- Shared password schema (single source of truth)
- Breached password checking (HaveIBeenPwned API or similar)
- Password change requires current password
- Password history prevention (no reuse of last N)

### Score 7-8: Production-ready
- Strong hashing algorithm (bcrypt/Argon2)
- Minimum length enforced (≥ 8 chars)
- Single shared validation schema
- Rate limiting on login attempts

### Score 5-6: Minimum
- Bcrypt hashing
- Basic minimum length
- Rate limiting exists

### Score 3-4: Below minimum
- Weak hashing (MD5, SHA-1)
- No minimum length
- No rate limiting on password attempts

### Score 0-2: Critical
- Plaintext or reversible encryption
- No password validation
- Passwords logged or exposed in errors

### Checklist
- [ ] Bcrypt/Argon2 with appropriate cost factor
- [ ] Minimum 8 characters enforced
- [ ] Shared `strongPasswordSchema` (Zod) used everywhere
- [ ] Password not logged or included in error responses
- [ ] Rate limiting on login endpoint
- [ ] Secure password reset flow (time-limited token)
- [ ] Password change requires authentication
