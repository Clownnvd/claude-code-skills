# Security Generate Workflow

## Process

1. **Parse Request** — Extract: component type, security requirements, threat model
2. **Load Criteria** — Read all 10 security scoring categories from SKILL.md
3. **Map Criteria to Code**:

| Category | Code Pattern |
|----------|-------------|
| OWASP Top 10 Coverage (15%) | Injection prevention, broken auth checks, XSS guards |
| Input Sanitization (12%) | DOMPurify, parameterized queries, Zod validation |
| Auth Security (12%) | Session validation, token rotation, secure cookies |
| Data Protection (10%) | Encryption at rest/transit, PII handling, field masking |
| Security Headers (10%) | CSP, X-Frame-Options, HSTS, Referrer-Policy, Permissions |
| CORS Configuration (8%) | Explicit origins, no wildcard in production, preflight |
| CSP Policy (8%) | Nonce-based, no unsafe-inline, report-uri |
| Secrets Management (8%) | Env vars, no hardcoded secrets, rotation support |
| Dependency Security (7%) | npm audit, no known CVEs, lockfile integrity |
| Security Logging (10%) | Auth events, access logs, anomaly detection |

4. **Generate** — Write security-hardened code with all patterns
5. **Self-Check** — Verify all 10 categories
6. **Output** — Code + compliance checklist

## Quality Contract

- All 10 categories addressed
- Score >= 90 (A-) if audited with security scoring
- No XSS vectors, no SQL injection, no CSRF gaps
- All secrets from environment, never hardcoded
