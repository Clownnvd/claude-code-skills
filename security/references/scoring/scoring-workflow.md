# Security Design Scoring Workflow

## Step 1: Gather Files

Read these files (minimum set):
```
src/lib/validations/**         # Zod schemas
.env.example                   # Env vars documentation
src/lib/env.ts                 # Runtime env validation
src/lib/api/response.ts        # Error response shapes
src/proxy.ts                    # CSP, security headers, redirects
src/app/api/webhooks/**        # Webhook verification
src/app/api/**/route.ts        # Input handling per route
src/lib/api/logger.ts          # Security logging
next.config.js                 # Build security config
package.json                   # Dependencies
prisma/schema.prisma           # Data model
src/lib/csrf.ts                # CSRF implementation
```

## Step 2: Score Each Category

For each category, use the criteria file:
1. Read the 9-10 (enterprise) checklist
2. Check how many items are met
3. Note deductions with specific file:line references
4. Assign score 0-10

## Step 3: Calculate Weighted Total

```
total = sum(score[i] * weight[i]) for i in 1..10
```

Weights: Input(15) + Secrets(12) + Deps(10) + Errors(12) + CSP(10) + Data(10) + Redirect(8) + Webhook(8) + Monitor(8) + Supply(7) = 100%

## Step 4: Assign Grade

Use grade scale from overview.md.

## Step 5: List Issues

For each deduction, create issue entry:
- **Severity**: CRITICAL (data breach risk), HIGH (exploitable), MEDIUM (defense-in-depth gap), LOW (hardening)
- **Category**: Which scoring category
- **File:Line**: Exact location
- **Issue**: What's wrong
- **Fix**: How to fix it

## Step 6: Output Scorecard

Use the template from overview.md.

## Framework-Specific Adjustments

### Next.js App Router
- Server Components can't leak client secrets = +1 to Secrets
- `poweredByHeader: false` in config = +1 to Supply Chain
- Proxy CSP header = +1 to CSP
- `force-dynamic` prevents caching private data = +1 to Data Protection

### Prisma
- `select` prevents over-fetching sensitive fields = +1 to Data Protection
- Parameterized queries prevent SQL injection = +1 to Input Validation
- `@@unique` constraints prevent data integrity issues = +1 to Data Protection

### Better Auth
- Built-in password hashing (bcrypt/argon2) = +1 to Data Protection
- Session token rotation = +1 to Data Protection
- (auth-specific items scored by auth-scoring, not here)
