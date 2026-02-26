# Security Review Workflow

## Process

1. **Read** — Load target file(s), identify security-relevant patterns
2. **Classify** — Which security categories apply:
   - API route → Input Validation, Error Handling, Secrets, Monitoring, Webhooks
   - Middleware/proxy → CSP, Data Protection, Open Redirect
   - Config file → Secrets, Dependencies, Supply Chain
   - Component with user input → Input Validation, Data Protection, CSP
3. **Score** — Rate each applicable category 0-10
4. **Annotate** — Cite line numbers and issues
5. **Suggest** — Concrete security fixes
6. **Summarize** — Score, priorities, quick wins

## Common Security Issues

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | Hardcoded secrets/API keys | Secrets & Environment Management | CRITICAL |
| 2 | No input sanitization on user content | Input Validation & Sanitization | CRITICAL |
| 3 | SQL injection via raw query | Input Validation & Sanitization | CRITICAL |
| 4 | Stack trace leaked to client | Error Handling & Info Disclosure | CRITICAL |
| 5 | No CSP header | Content Security Policy | HIGH |
| 6 | Known CVE in dependency | Dependency Security | HIGH |
| 7 | Open redirect vulnerability | Open Redirect & URL Validation | HIGH |
| 8 | Webhook without signature verification | Webhook & External API Security | HIGH |
| 9 | PII in logs | Data Protection & PII | HIGH |
| 10 | No security event logging | Security Monitoring & Logging | MEDIUM |
