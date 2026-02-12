# API Best Practices — Do / Don't

Quick reference for common patterns. Use during scoring to identify issues.

## Security

| Do | Don't |
|----|-------|
| Verify webhook signatures (Stripe, SePay) | Trust raw webhook payloads |
| Validate Origin/Referer for CSRF | Only check X-Requested-With (spoofable) |
| Use rightmost X-Forwarded-For IP | Use leftmost IP (client-spoofable) |
| Set security headers on ALL routes | Only set headers on protected pages |
| Validate payment amounts server-side | Trust client-submitted amounts |
| Return generic error messages | Leak DB errors, stack traces, paths |

## Input Validation

| Do | Don't |
|----|-------|
| Validate at route entry with schema | Validate deep in business logic |
| Single source of truth for schemas | Duplicate validation in multiple files |
| Allowlist query params / sort fields | Pass raw query params to DB |
| Reject unknown fields in body | Spread `req.body` into DB create |
| Validate path params (UUID format) | Trust path params as valid IDs |

## Error Handling

| Do | Don't |
|----|-------|
| Consistent envelope: `{ success, data, error }` | Mix formats across routes |
| Return field-level errors for validation | Return single string for all validation |
| Use `serverError()` helper (hides details) | Return `{ error: err.message }` from catch |
| Use correct status codes (401 vs 403) | Return 200 with error in body |
| Throw in webhook for missing data | Silently `return` on missing data |

## Rate Limiting

| Do | Don't |
|----|-------|
| Different limits per endpoint sensitivity | One global limit for everything |
| Include rate limit headers in responses | Return 429 without Retry-After |
| Use distributed store (Redis) in production | In-memory only in production |
| Rate limit webhook endpoints | Leave webhooks unprotected |

## Performance

| Do | Don't |
|----|-------|
| Use `select` clause on DB queries | Return all columns (SELECT *) |
| Eager load relations (avoid N+1) | Loop with individual queries |
| Connection pooling with singleton | New connection per request |
| Set DB query timeouts | Allow unbounded query execution |
| Log slow queries (> 1000ms threshold) | Ignore query performance |

## Auth

| Do | Don't |
|----|-------|
| Verify user owns resource (BOLA check) | Trust user-supplied resource IDs |
| Check auth at handler level, not just proxy | Rely only on proxy cookie check |
| Validate session + DB lookup for mutations | Trust cookie existence for writes |
| Separate admin from user endpoints | Same auth level for all roles |

## Observability

| Do | Don't |
|----|-------|
| Structured JSON logs in production | `console.log("error:", err)` |
| Health check that pings DB | Health check that returns 200 always |
| Sanitize query params in logs | Log full SQL with user data |
| Use log levels correctly (ERROR, WARN, INFO) | Everything at INFO level |

## Testing

| Do | Don't |
|----|-------|
| Test auth: 401, 403, BOLA scenarios | Only test happy path |
| Test validation: boundary values, wrong types | Only test valid inputs |
| Mock external APIs (Stripe, GitHub) | Call real APIs in unit tests |
| Run tests in CI on every PR | Manual testing only |
