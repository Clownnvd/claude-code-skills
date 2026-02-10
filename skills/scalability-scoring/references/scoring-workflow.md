# Scalability Scoring Workflow

## Step 1: Gather Files

Read these files (minimum set):
```
package.json                    # Dependency count, heavy packages
next.config.js                  # Build config, image optimization
src/app/**/page.tsx             # Page components, RSC boundaries
src/components/**               # 'use client' usage, component patterns
src/app/api/**/route.ts         # API response patterns
src/lib/db/**                   # Database connection, queries
src/middleware.ts                # Edge performance
prisma/schema.prisma            # Indexes, relations
src/hooks/**                    # Client state patterns
public/**                       # Asset sizes
```

## Step 2: Score Each Category

For each category:
1. Read the criteria checklist (9-10 enterprise items)
2. Check how many items are met
3. Note deductions with specific file:line references
4. Assign score 0-10

## Step 3: Calculate Weighted Total

```
total = sum(score[i] * weight[i]) for i in 1..10
```

Weights: Bundle(15) + Images(12) + RSC(12) + DB(12) + API(10) + Client(10) + Edge(8) + Memory(8) + Concurrency(7) + Monitoring(6) = 100%

## Step 4: Assign Grade

Use grade scale from SKILL.md.

## Step 5: List Issues

For each deduction:
- **Severity**: CRITICAL (user-visible perf impact), HIGH (measurable), MEDIUM (defense-in-depth), LOW (optimization)
- **Category**: Which scoring category
- **File:Line**: Exact location
- **Issue**: What's wrong
- **Fix**: How to fix it

## Step 6: Output Scorecard

Use the template from overview.md.

## Framework Adjustments

### Next.js App Router
- Automatic route-level code splitting = +1 to Bundle Size
- Server Components default = +1 to RSC Architecture
- Built-in image optimization = +1 to Images
- Edge middleware for static bypass = +1 to Edge/CDN

### Small App Adjustments
- If app has <10 pages and <5 API routes, Edge/CDN weight redistributes to Bundle and RSC
- If no public-facing images, Image weight redistributes to Bundle and Client
