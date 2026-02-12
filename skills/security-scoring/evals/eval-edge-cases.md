# Security Scoring — Edge Cases Eval

Verify correct behavior for security-specific edge cases.

## Test 1: No Input Validation on User Input

- Provide API routes accepting user input without Zod or any validation
- Verify Input Validation scores <= 2 (CRITICAL)
- Verify OWASP A03 (Injection) flagged
- Verify issue recommends Zod schemas at every boundary

## Test 2: Hardcoded Secrets in Source Code

- Provide code with API keys, DB URLs, or tokens in source files
- Verify Secrets & Environment Mgmt scores 0 (CRITICAL)
- Verify issue identifies specific files and variable names
- Verify fix recommends env variables with `.env.example` template

## Test 3: Known CVEs in Dependencies

- Provide `package.json` with dependencies that have known vulnerabilities
- Verify Dependency Security scores <= 3
- Verify issue lists specific packages and CVE identifiers
- Verify fix recommends `npm audit fix` or version upgrade

## Test 4: Stack Traces Leaked to Client

- Provide error handling that sends full stack traces in production responses
- Verify Error Handling & Info Disclosure scores <= 2 (CRITICAL)
- Verify OWASP A09 flagged
- Verify fix recommends safe error envelope with generic client message

## Test 5: Missing CSP Header

- Provide app with no Content-Security-Policy header configured
- Verify CSP scores <= 2
- Verify issue flags XSS risk from missing script-src directive
- Verify fix recommends CSP header with nonce or strict policy

## Test 6: Webhook Endpoints Without Signature Verification

- Provide webhook handler routes that process payloads without verifying signatures
- Verify Webhook Security scores <= 2 (CRITICAL)
- Verify issue flags replay attack and spoofing risk
- Verify fix recommends HMAC signature verification and idempotency keys

## Test 7: Open Redirect Vulnerability

- Provide redirect logic using unvalidated user-supplied URLs
- Verify Open Redirect scores <= 2 (CRITICAL)
- Verify issue identifies the redirect code and attack vector
- Verify fix recommends allowlist validation and `//` blocking
