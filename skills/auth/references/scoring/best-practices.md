# Auth Best Practices — Do / Don't

## Sessions

| Do | Don't |
|----|-------|
| HttpOnly + Secure + SameSite cookies | Store tokens in localStorage |
| Server-side sessions with DB adapter | Client-only JWT with no revocation |
| Set idle + absolute expiry | Never-expiring sessions |
| Rotate session on privilege change | Reuse same session ID after login |

## Passwords

| Do | Don't |
|----|-------|
| Bcrypt/Argon2 with cost ≥ 10 | MD5, SHA-1, SHA-256 (unsalted) |
| Single shared `strongPasswordSchema` | Different validation per form |
| Require current password for changes | Allow password change without auth |
| Rate limit login attempts | Allow unlimited login attempts |

## OAuth

| Do | Don't |
|----|-------|
| Env-based enable: `Boolean(process.env.CLIENT_ID)` | Hardcode credentials |
| Account linking with trusted providers | Auto-link all providers blindly |
| Minimal OAuth scopes | Request all available scopes |
| Validate state parameter | Skip CSRF on OAuth callback |

## CSRF

| Do | Don't |
|----|-------|
| Validate Origin against allowlist | Accept any Origin |
| Use Referer as fallback | Rely only on X-Requested-With |
| Reject if BOTH Origin + Referer missing | Silent pass-through |
| Block `//` and `/\` in redirects | Trust user-supplied redirect URLs |

## Security Headers

| Do | Don't |
|----|-------|
| Apply headers on ALL routes via middleware | Only on protected pages |
| Strict CSP (no `unsafe-eval`) | `default-src *` |
| HSTS with includeSubDomains | Short max-age or no HSTS |
| Disable dangerous APIs via Permissions-Policy | Skip Permissions-Policy |

## Rate Limiting

| Do | Don't |
|----|-------|
| Strict limits on auth mutations (≤ 5/min) | Same limit for all endpoints |
| Distributed store (Upstash Redis) | In-memory store (resets on deploy) |
| Per-user limiting on authenticated routes | IP-only (bypassable via proxies) |
| Return 429 with Retry-After | Silent throttling or generic 500 |

## Audit Logging

| Do | Don't |
|----|-------|
| Log all auth events (sign_in, sign_up, etc.) | Log only errors |
| Structured JSON in production | Free-text console.log |
| Include userId, never PII | Include email, name, password |
| Use `warn` level for failed attempts | Same level for all events |

## Authorization

| Do | Don't |
|----|-------|
| Two-layer: proxy (Node) + API route (Node) | Client-only auth gates |
| `requireAuth()` in every protected API route | Trust middleware alone |
| Object-level auth (own resources only) | Trust user-supplied IDs |
| Preserve callbackUrl on login redirect | Redirect to static path |
