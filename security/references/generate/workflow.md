# Security Generate Workflow

## Process

1. **Parse Request** — Extract: component type, security requirements, threat model
2. **Load Criteria** — Read all 10 security scoring categories from SKILL.md
3. **Map Criteria to Code**:

| Category | Code Pattern |
|----------|-------------|
| Input Validation & Sanitization (15%) | Zod at boundaries, DOMPurify for HTML, parameterized queries, XSS prevention |
| Secrets & Environment Management (12%) | Env vars only, .env.example, no hardcoded secrets, rotation support |
| Dependency Security (10%) | npm audit clean, lockfile integrity, no known CVEs |
| Error Handling & Info Disclosure (12%) | No stack traces to client, safe error messages, no internal IDs leaked |
| Content Security Policy (10%) | CSP header with nonces, script-src, no unsafe-eval/unsafe-inline |
| Data Protection & PII (10%) | HTTPS enforced, PII minimization, field masking, encryption at rest |
| Open Redirect & URL Validation (8%) | Redirect allowlist, `//` and `/\` blocked, URL parsing validation |
| Webhook & External API Security (8%) | Signature verification, idempotency keys, replay protection |
| Security Monitoring & Logging (8%) | Security events logged, request IDs, anomaly detection, no PII in logs |
| Supply Chain & Build Security (7%) | Lockfile committed, poweredByHeader off, source maps disabled in prod |

4. **Generate** — Write security-hardened code with all patterns
5. **Self-Check** — Verify all 10 categories
6. **Output** — Code + compliance checklist

## Quality Contract

- All 10 categories addressed
- Score >= 90 (A-) if audited with security scoring
- No XSS vectors, no SQL injection, no info disclosure
- All secrets from environment, never hardcoded
