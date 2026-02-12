# Criteria: Dependencies (10%) + Error Handling (12%)

## Category 3: Dependency Security (Weight: 10%)

### Enterprise (9-10)
1. `pnpm audit` / `npm audit` reports 0 critical/high vulnerabilities
2. Lockfile (`pnpm-lock.yaml`) committed to git
3. No wildcard version ranges (`*`, `latest`) in package.json
4. Dependencies updated within last 90 days
5. No deprecated packages in use
6. New dependencies reviewed before adding (README, downloads, maintenance)
7. Minimal dependency footprint (no unnecessary packages)
8. Dev dependencies separated from production
9. No known CVEs in production dependencies
10. CI runs audit check on every PR

### Scoring
- 10: All 10 items met
- 9: 9 items met
- 8: 1 medium vulnerability or minor gap
- 7: 2-3 medium vulnerabilities
- 6: Some outdated dependencies (>6 months)
- 5: High vulnerability present
- 4: Multiple high vulnerabilities
- 3: Critical vulnerability present
- 2: No lockfile or wildcard versions
- 1: Multiple critical vulnerabilities
- 0: Known exploitable vulnerability in production

### Deduction Examples
- -4: Critical CVE in production dependency
- -3: No lockfile committed
- -2: High vulnerability in `pnpm audit`
- -1: Dependencies >6 months outdated
- -1: Unnecessary dependencies (could be removed)

---

## Category 4: Error Handling & Info Disclosure (Weight: 12%)

### Enterprise (9-10)
1. Generic error messages to client (no stack traces, DB errors, internal paths)
2. Structured error codes in responses (`VALIDATION_ERROR`, `UNAUTHORIZED`)
3. Consistent error response shape via `src/lib/api/response.ts`
4. `reportError()` or structured logger for server-side errors
5. No `console.error(error)` with full error objects in production
6. Different error detail levels for dev vs prod
7. 404/500 pages don't leak server info
8. API errors don't reveal database schema or query details
9. External API errors (Stripe, GitHub) not forwarded to client
10. Error boundaries in React prevent white screen of death

### Scoring
- 10: All 10 items met
- 9: 9 items met
- 8: 1 minor info disclosure
- 7: Inconsistent error response shapes
- 6: Some `console.error` with full objects
- 5: Stack trace leak possible in 1-2 routes
- 4: External API errors forwarded to client
- 3: DB error details leaked
- 2: Stack traces in production responses
- 1: Internal paths and server info leaked
- 0: Full error objects returned to client

### Deduction Examples
- -3: Stack trace or internal path in API response
- -3: Database error message forwarded to client
- -2: External API error (Stripe/GitHub) details leaked
- -2: `console.log`/`console.error` in API routes
- -1: Missing error boundary
- -1: Inconsistent error response format
