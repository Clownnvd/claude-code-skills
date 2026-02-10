# Criteria: Monitoring (8%) + Supply Chain (7%)

## Category 9: Security Monitoring & Logging (Weight: 8%)

### Enterprise (9-10)
1. Security events logged (failed auth, rate limit hits, invalid input)
2. Request IDs for cross-service tracing
3. Structured JSON logging in production (not console.log)
4. Log levels: info for normal, warn for suspicious, error for failures
5. No PII in logs (emails, passwords, tokens)
6. Rate limit violations logged with IP and path
7. Webhook processing logged (success/failure per event)
8. Audit trail for sensitive operations (purchases, settings changes)
9. Log rotation / retention configured
10. Alerting on anomalous patterns (spike in errors, auth failures)

### Scoring
- 10: All 10 items met
- 9: 9 items met (alerting optional for 9)
- 8: Good logging, missing 1-2 items
- 7: Structured logging present, some gaps
- 6: Basic logging, no request IDs
- 5: console.log-based logging, some coverage
- 4: Minimal logging, major blind spots
- 3: Only error logging, no security events
- 2: No structured logging
- 1: Silent failures (no logging at all)
- 0: Security events completely invisible

### Deduction Examples
- -3: No security event logging at all
- -2: PII in production logs
- -2: No request IDs for tracing
- -1: console.log instead of structured logger
- -1: Missing webhook event logging
- -1: No audit trail for purchases

---

## Category 10: Supply Chain & Build Security (Weight: 7%)

### Enterprise (9-10)
1. `poweredByHeader: false` in next.config
2. Lockfile committed and reviewed on changes
3. No source maps in production (`productionBrowserSourceMaps: false`)
4. CI runs `pnpm audit` / security checks
5. No `eval()` or `new Function()` in application code
6. Build output doesn't include `.env` files
7. `X-Powered-By` header removed
8. Server-only modules not bundled to client
9. No sensitive data in build-time environment
10. Dependencies imported from official registries only

### Scoring
- 10: All 10 items met
- 9: 9 items met
- 8: Minor gap (e.g., no CI audit)
- 7: Good config, 1 missing item
- 6: `poweredByHeader` not disabled
- 5: Source maps enabled in production
- 4: No lockfile or CI security check
- 3: `eval()` or `new Function()` used
- 2: Sensitive data in build output
- 1: Multiple supply chain issues
- 0: Source code exposed in production

### Deduction Examples
- -3: Source maps enabled in production
- -2: `eval()` or `new Function()` in code
- -2: No lockfile committed
- -1: `poweredByHeader` not set to false
- -1: No CI security audit step
- -1: Server modules imported in client components
