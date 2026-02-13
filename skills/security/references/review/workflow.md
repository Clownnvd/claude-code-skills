# Security Review Workflow

## Process

1. **Read** — Load target file(s), identify security-relevant patterns
2. **Classify** — Which security categories apply:
   - API route → OWASP, Input Sanitization, Auth, CORS, Headers, Logging
   - Middleware/proxy → Headers, CORS, CSP, Auth Security
   - Config file → Secrets Management, Dependencies, CSP
   - Component with user input → Input Sanitization, XSS, Data Protection
3. **Score** — Rate each applicable category 0-10
4. **Annotate** — Cite line numbers and issues
5. **Suggest** — Concrete security fixes
6. **Summarize** — Score, priorities, quick wins

## Common Security Issues

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | Hardcoded secrets/API keys | Secrets Management | CRITICAL |
| 2 | No input sanitization on user content | Input Sanitization | CRITICAL |
| 3 | SQL injection via raw query | OWASP Top 10 | CRITICAL |
| 4 | Missing CSRF protection | Auth Security | CRITICAL |
| 5 | CORS wildcard (*) in production | CORS | HIGH |
| 6 | No CSP header | CSP Policy | HIGH |
| 7 | Missing security headers | Security Headers | HIGH |
| 8 | Known CVE in dependency | Dependency Security | HIGH |
| 9 | No auth event logging | Security Logging | MEDIUM |
| 10 | PII in logs | Data Protection | HIGH |
