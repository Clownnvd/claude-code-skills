# Security Migrate Workflow

## Process

1. **Detect Versions** — Identify framework, auth library, security middleware versions
2. **Map Breaking Changes**:

| From → To | Category Affected | Breaking Change | Migration Action |
|-----------|------------------|-----------------|-----------------|
| Next.js 15 → 16 | Security Headers | Header config changes | Update header middleware |
| Next.js 15 → 16 | Auth Security | Proxy replaces middleware | Move auth security to proxy.ts |
| Any | CSP | Nonce generation changes | Update CSP nonce implementation |
| Any | CORS | Origin validation changes | Update CORS config |
| Any | Dependencies | New CVEs discovered | Run npm audit, update packages |
| Any | Secrets | Env var format changes | Update secret references |

3. **Apply Migrations** — NEVER weaken security during migration
4. **Verify** — Security scan, header check, CORS test
5. **Re-score** — Ensure no security regression

## Safety Rules

- NEVER remove security headers during migration
- NEVER weaken CORS or CSP during migration
- Run security audit before AND after
- Verify CSRF protection still active after auth changes
- Check for new CVEs in updated dependencies
