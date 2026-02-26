# Security Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| Input Validation & Sanitization (15%) | Unit + Integration | Zod rejects invalid input, XSS stripped, SQL injection blocked |
| Secrets & Environment Management (12%) | Static analysis | No hardcoded secrets, env vars used, .env.example present |
| Dependency Security (10%) | Audit | No known CVEs, lockfile integrity, npm audit clean |
| Error Handling & Info Disclosure (12%) | Integration | No stack traces in response, safe error messages, no internal IDs |
| Content Security Policy (10%) | Integration | CSP header present, nonce-based, no unsafe-eval |
| Data Protection & PII (10%) | Unit + Integration | HTTPS enforced, PII masked, no PII in logs |
| Open Redirect & URL Validation (8%) | Integration | Redirect allowlist enforced, malicious URLs blocked |
| Webhook & External API Security (8%) | Integration | Signature verified, replay attack blocked, idempotency |
| Security Monitoring & Logging (8%) | Unit | Security events logged, request IDs present, no PII in logs |
| Supply Chain & Build Security (7%) | Build test | Lockfile committed, poweredByHeader off, source maps disabled |

2. **Generate Test Files**:
   - `__tests__/security/input-validation.test.ts` — XSS, injection prevention
   - `__tests__/security/error-handling.test.ts` — Info disclosure prevention
   - `__tests__/security/headers.test.ts` — CSP, security headers
   - `__tests__/security/secrets.test.ts` — No hardcoded secrets scan
   - `__tests__/security/deps.test.ts` — Dependency audit

3. **Output** — Test files + coverage matrix
