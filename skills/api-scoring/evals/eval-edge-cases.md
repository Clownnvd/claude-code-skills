# API Scoring — Edge Cases Eval

Verify correct behavior for API-specific edge cases.

## Test 1: No API Routes Found

- Run against a codebase with zero API route files
- Verify scoring does not crash
- Verify output notes the absence and scores relevant categories at 0
- Verify non-API categories (Documentation, Testing) can still score above 0

## Test 2: API Routes Without Auth Middleware

- Provide routes with no auth checks
- Verify Security scores <= 3 (CRITICAL)
- Verify Auth & AuthZ scores <= 3 (CRITICAL)
- Verify OWASP API1 (BOLA) and API2 (Broken Auth) flagged

## Test 3: Missing Rate Limiting on Public Endpoints

- Provide public API routes with no rate limiting
- Verify Rate Limiting scores 0-2
- Verify OWASP API4 (Resource Consumption) flagged as CRITICAL
- Verify issue references specific unprotected route files

## Test 4: Sensitive Data in Error Responses

- Provide API routes that leak stack traces or internal details in error responses
- Verify Error Handling penalized (score <= 4)
- Verify OWASP API8 (Misconfiguration) flagged
- Verify issue recommends safe error envelope pattern

## Test 5: Next.js App Router API Routes

- Provide Next.js `route.ts` files using App Router conventions
- Verify framework-specific adjustments from `nextjs-patterns.md` are applied
- Verify two-layer auth pattern is checked (middleware + route handler)
- Verify webhook route patterns are evaluated separately

## Test 6: All Categories Score 10

- Provide exemplary codebase hitting all criteria
- Verify total score is 100 and grade is A+
- Verify issues list is empty or contains only LOW suggestions
- Verify no false CRITICAL/HIGH issues on a perfect codebase

## Test 7: Mixed HTTP Methods Without Validation

- Provide routes accepting POST/PUT/PATCH without input validation
- Verify Input Validation scores <= 3
- Verify OWASP API3 (BOPLA) and API7 (SSRF) flagged
