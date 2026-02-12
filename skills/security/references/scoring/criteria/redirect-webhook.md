# Criteria: Redirects (8%) + Webhooks (8%)

## Category 7: Open Redirect & URL Validation (Weight: 8%)

### Enterprise (9-10)
1. Redirect URLs validated — `//` and `/\` blocked
2. Only relative paths allowed for callback redirects
3. External redirect URLs checked against allowlist
4. `new URL()` used for safe URL parsing (not string concat)
5. Query string redirect params (`?callbackUrl=`) validated
6. No user-controlled redirect in 3xx responses without validation
7. Auth callback URLs validated before redirect
8. `Location` header values sanitized
9. JavaScript `window.location` assignments use validated URLs
10. URL validation tested with bypass attempts

### Scoring
- 10: All 10 items met
- 9: 9 items met
- 8: Minor gap in edge case handling
- 7: Most redirects validated, 1 gap
- 6: Redirect validation present but incomplete
- 5: Some redirects unvalidated
- 4: `//` or `/\` not blocked
- 3: External redirects allowed without validation
- 2: User-controlled redirects without any validation
- 1: Open redirect in auth flow
- 0: Open redirect exploitable for phishing

### Deduction Examples
- -4: Open redirect in authentication callback
- -3: No `//` or `/\` blocking on redirect URLs
- -2: External redirect without allowlist
- -1: String concatenation for URL building
- -1: Missing validation on `callbackUrl` param

---

## Category 8: Webhook & External API Security (Weight: 8%)

### Enterprise (9-10)
1. Webhook signatures verified (Stripe `constructEvent`, SePay HMAC)
2. Raw request body used for signature verification (not parsed JSON)
3. Idempotency: check-before-create by event/payment ID
4. Webhook endpoint doesn't leak internal errors
5. External API calls have timeouts configured
6. External API errors caught and not forwarded to client
7. Webhook returns 200 quickly (heavy work done async or after response)
8. Replay protection (event timestamp check)
9. Webhook secrets rotated periodically
10. Failed webhook deliveries logged for retry monitoring

### Scoring
- 10: All 10 items met
- 9: 9 items met
- 8: Minor gap (e.g., no timestamp check)
- 7: Good verification, missing idempotency
- 6: Signature verification present, some gaps
- 5: Idempotency missing on critical webhooks
- 4: No signature verification on 1 webhook
- 3: External API errors leaked to client
- 2: No signature verification
- 1: Webhook processes duplicate events
- 0: Unsigned webhooks accepted in production

### Deduction Examples
- -4: No webhook signature verification
- -3: Missing idempotency (duplicate payment processing)
- -2: External API errors forwarded to webhook response
- -2: No timeout on external API calls
- -1: No replay protection (timestamp check)
- -1: Webhook doing heavy sync work before responding
