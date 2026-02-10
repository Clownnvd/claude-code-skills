# Caching Strategy Scoring Workflow

## Step 1: Gather Files

Read these files (minimum set):
```
src/app/api/**/route.ts       # Cache-Control headers
src/app/**/page.tsx           # Static/dynamic classification
src/app/**/layout.tsx         # Layout caching
src/middleware.ts             # Middleware caching
src/lib/auth.ts               # Auth session caching
src/lib/auth/server.ts        # Server session dedup
src/lib/db/index.ts           # Prisma client config
src/lib/api/response.ts       # NO_CACHE_HEADERS utility
src/app/api/webhooks/**       # Revalidation after mutations
next.config.ts                # Static/ISR config
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

Weights: Headers(15) + Revalidation(15) + Static/Dynamic(12) + ISR(8) + ReactCache(10) + UnstableCache(10) + CDN(8) + Dedup(7) + Middleware(7) + Monitoring(8) = 100%

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
- All API routes return `NO_CACHE_HEADERS` on auth data = +2 to Headers
- `force-dynamic` only on auth-dependent pages = +1 to Static/Dynamic
- `export const dynamic = "force-dynamic"` explicit on all API routes = +1 to Static/Dynamic
- Landing page is fully static (no server session read) = +2 to Static/Dynamic

### Prisma + Neon
- `unstable_cache` wrapping expensive aggregations = +1 to UnstableCache
- Connection pooling configured = +1 to CDN (reduces origin load)

### Better Auth
- `cache()` on `getServerSession` = +2 to ReactCache
- Session check in middleware is lightweight = +1 to Middleware
- `useSession()` client-side for non-critical auth = +1 to Static/Dynamic
