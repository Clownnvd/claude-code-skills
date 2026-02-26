# Data Flow Scoring Workflow

## Step 1: Gather Files

Read these files (minimum set):
```
src/app/**/page.tsx           # Page data fetching
src/app/api/**/route.ts       # API route patterns
src/hooks/**                  # Client data hooks
src/lib/db/index.ts           # DB client config
src/lib/api/response.ts       # Response envelope
src/lib/validations/**        # Zod schemas
src/types/index.ts            # Shared types
prisma/schema.prisma          # Indexes, models
src/app/**/error.tsx           # Error boundaries
src/app/**/loading.tsx         # Loading states
src/proxy.ts                   # Request pipeline
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

Weights: RSC(15) + Composition(10) + Prisma(12) + API(15) + State(8) + Cache(10) + Types(10) + Errors(8) + Forms(7) + DTOs(5) = 100%

## Step 4: Assign Grade

Use grade scale from overview.md.

## Step 5: List Issues

For each deduction, create issue entry:
- **Severity**: CRITICAL (0-3), HIGH (4-5), MEDIUM (6-7), LOW (8)
- **Category**: Which scoring category
- **File:Line**: Exact location
- **Issue**: What's wrong
- **Fix**: How to fix it

## Step 6: Output Scorecard

Use the template from overview.md.

## Framework-Specific Adjustments

### Next.js App Router
- Server Components fetching directly = +2 to RSC
- `"use client"` only at leaves = +1 to Composition
- `force-dynamic` everywhere = -2 to Caching

### React 19
- `useActionState` for forms = +1 to Forms
- `useOptimistic` for mutations = +1 to Forms
- Server Actions instead of API routes for forms = +1 to Forms

### Prisma + Neon
- `select` on all queries = +1 to Prisma
- Neon adapter with pooling = +1 to Prisma
- Statement timeout configured = +1 to Prisma
- `@@index` on lookup fields = +1 to Prisma

### Better Auth
- `cache()` on getServerSession = +1 to Caching
- Session type exported = +1 to Types
