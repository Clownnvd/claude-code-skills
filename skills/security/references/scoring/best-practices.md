# Security Design Best Practices

## 1. Input Validation & Sanitization

| Do | Don't |
|----|-------|
| Zod `.safeParse()` on every API input | Raw `req.json()` without validation |
| Single validation schema source in `validations/` | Duplicate schemas per route |
| Reject unknown keys (`z.object().strict()`) | Accept arbitrary input |
| Validate URL parameters and query strings | Trust URL params as safe |
| Type-check and range-check numbers | Accept any number from client |

## 2. Secrets & Environment Management

| Do | Don't |
|----|-------|
| All secrets in env vars | Hardcode API keys, passwords, tokens |
| `.env.example` documenting all vars | Undocumented env requirements |
| Runtime env validation (Zod/env.ts) | Trust env vars exist at runtime |
| `NEXT_PUBLIC_` prefix only for public vars | Put secrets in NEXT_PUBLIC_ vars |
| Sync: env.d.ts + env.ts + .env.example | Out-of-sync env files |

## 3. Dependency Security

| Do | Don't |
|----|-------|
| `npm audit` / `pnpm audit` regularly | Ignore audit warnings |
| Pin dependency versions in lockfile | No lockfile committed |
| Update dependencies monthly | Let dependencies go years without update |
| Review new dependency before adding | Install any package blindly |

## 4. Error Handling & Info Disclosure

| Do | Don't |
|----|-------|
| Generic error messages to client | Leak stack traces, DB errors, internal paths |
| Structured error codes (`VALIDATION_ERROR`) | Only human-readable error strings |
| `reportError()` for structured logging | `console.error(error)` with full object |
| Different detail levels for dev vs prod | Same verbose errors in production |

## 5. Content Security Policy

| Do | Don't |
|----|-------|
| Strict CSP in proxy | No CSP header |
| `script-src 'self'` + specific CDNs | `script-src *` or `unsafe-eval` |
| `frame-ancestors 'none'` | Allow framing from any origin |
| `default-src 'self'` baseline | No default-src |

## 6. Data Protection & PII

| Do | Don't |
|----|-------|
| `select` on Prisma queries (field filtering) | Return full Prisma objects |
| HTTPS enforced (HSTS in production) | HTTP allowed in production |
| Don't log PII (emails, IPs beyond need) | Log full user objects |
| Strip internal IDs from API responses | Leak database PKs, Stripe IDs |

## 7. Open Redirect & URL Validation

| Do | Don't |
|----|-------|
| Block `//` and `/\` in redirect URLs | Trust user-provided redirect URLs |
| Only allow relative paths for callbacks | Allow absolute URLs for redirects |
| Validate against allowlist if external | Open redirect to any domain |
| `new URL()` for safe URL parsing | String concatenation for URLs |

## 8. Webhook & External API Security

| Do | Don't |
|----|-------|
| Verify webhook signatures (Stripe, SePay) | Accept unsigned webhooks |
| Idempotency via event ID dedup | Process same event twice |
| Timeout on external API calls | Unbounded external requests |
| Don't leak external API errors to client | Forward Stripe/GitHub error details |

## 9. Security Monitoring

| Do | Don't |
|----|-------|
| Log security events (failed auth, rate limits) | Silent security failures |
| Request IDs for tracing | No correlation between logs |
| Structured JSON logging in production | Unstructured console.log |
| Monitor rate limit hits | No visibility into abuse attempts |

## 10. Supply Chain & Build Security

| Do | Don't |
|----|-------|
| `poweredByHeader: false` | Expose framework version |
| Lockfile committed and reviewed | No lockfile or `.gitignore`d |
| No source maps in production | Source maps exposing code |
| CI runs `npm audit` | No automated security checks |
