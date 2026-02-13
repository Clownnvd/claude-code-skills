# Security Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| OWASP Top 10 (15%) | Integration | XSS blocked, injection prevented, broken auth caught |
| Input Sanitization (12%) | Unit + Integration | Malicious input sanitized, HTML stripped |
| Auth Security (12%) | Integration | Session secure, tokens rotated, CSRF checked |
| Data Protection (10%) | Unit | PII masked, encryption applied, no PII in logs |
| Security Headers (10%) | Integration | All headers present in response |
| CORS (8%) | Integration | Origin validated, no wildcard in prod |
| CSP (8%) | Integration | Nonce-based, no unsafe-inline, policy correct |
| Secrets (8%) | Static analysis | No hardcoded secrets, env vars used |
| Dependencies (7%) | Audit | No known CVEs, lockfile matches |
| Security Logging (10%) | Unit | Auth events logged, no PII in logs |

2. **Generate Test Files**:
   - `__tests__/security/xss.test.ts` — XSS prevention
   - `__tests__/security/headers.test.ts` — Security headers
   - `__tests__/security/auth.test.ts` — Auth security
   - `__tests__/security/secrets.test.ts` — No hardcoded secrets scan
   - `__tests__/security/deps.test.ts` — Dependency audit

3. **Output** — Test files + coverage matrix
