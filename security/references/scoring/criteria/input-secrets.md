# Criteria: Input Validation (15%) + Secrets Management (12%)

## Category 1: Input Validation & Sanitization (Weight: 15%)

### Enterprise (9-10)
1. Every API route uses Zod `.safeParse()` on request body
2. Validation schemas live in single source `src/lib/validations/`
3. `z.object().strict()` rejects unknown keys
4. URL params and query strings validated
5. Numbers are type-checked and range-checked
6. File uploads validated (type, size, name)
7. No raw `req.json()` without validation
8. XSS prevention: no `dangerouslySetInnerHTML` with user input
9. Prisma parameterized queries (no raw SQL with interpolation)
10. Error messages from validation don't leak schema structure

### Scoring
- 10: All 10 items met
- 9: 9 items met
- 8: 8 items met, no CRITICAL gaps
- 7: 7 items met
- 6: Missing validation on 1-2 routes
- 5: Missing validation on 3+ routes
- 4: No centralized schemas
- 3: Raw input used in some routes
- 2: Widespread missing validation
- 1: No input validation at all
- 0: SQL injection or XSS possible

### Deduction Examples
- -3: API route accepts `req.json()` without Zod validation
- -2: Duplicate validation schemas across routes
- -2: `dangerouslySetInnerHTML` with unsanitized input
- -1: Missing `.strict()` on schemas
- -1: No range check on numeric inputs

---

## Category 2: Secrets & Environment Management (Weight: 12%)

### Enterprise (9-10)
1. All secrets in environment variables (no hardcoded keys/tokens)
2. `.env.example` documents all required variables
3. Runtime env validation via Zod (`src/lib/env.ts`)
4. `env.d.ts` type declarations match `env.ts`
5. `NEXT_PUBLIC_` prefix only for truly public vars
6. No secrets in `NEXT_PUBLIC_` variables
7. `.env` in `.gitignore`
8. Server-only secrets not importable from client components
9. Env files synced: `.env.example` + `env.ts` + `env.d.ts`
10. Missing env vars fail fast at startup (not at first request)

### Scoring
- 10: All 10 items met
- 9: 9 items met
- 8: 8 items met
- 7: Minor sync issue between env files
- 6: 1 missing env validation
- 5: 2-3 gaps in env management
- 4: No runtime env validation
- 3: Some hardcoded values
- 2: Secrets in NEXT_PUBLIC_ or committed .env
- 1: Hardcoded API keys in source
- 0: Secrets committed to git

### Deduction Examples
- -4: Hardcoded API key or password in source code
- -3: Secret in `NEXT_PUBLIC_` variable
- -2: No `.env.example` file
- -2: No runtime env validation
- -1: `env.d.ts` out of sync with `env.ts`
- -1: Env var used without checking if defined
