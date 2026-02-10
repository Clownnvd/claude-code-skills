# Scalability & Performance Scoring — Overview

## Purpose
Objectively score application scalability and performance in Next.js App Router applications. Covers bundle optimization, rendering performance, database efficiency, and resource management.

## Scope Boundaries
- **This skill**: Bundle size, images, RSC architecture, DB queries, API perf, client rendering, edge/CDN, memory, concurrency, monitoring
- **caching-scoring**: Cache headers, revalidation, ISR, React cache(), unstable_cache
- **dataflow-scoring**: RSC data flow, Prisma patterns, API route design, form handling

## Scoring System
- 10 categories, each scored 0-10
- Weighted sum produces 0-100 total
- Each deduction must cite specific file + line + reason

## Output Format

```markdown
## Scalability & Performance Scorecard — [Project Name]

| # | Category | Weight | Score | Weighted | Issues |
|---|----------|--------|-------|----------|--------|
| 1 | Bundle Size & Code Splitting | 15% | X/10 | Y | ... |
| ... | | | | | |
| **Total** | | **100%** | | **XX/100** | |
| **Grade** | | | | **B+** | |

### Issues List
| # | Severity | Category | File:Line | Issue | Fix |
|---|----------|----------|-----------|-------|-----|
| 1 | CRITICAL | ... | ... | ... | ... |
```

## Files to Audit (ordered by priority)
1. `package.json` — dependency count, bundle-heavy packages
2. `next.config.js` — webpack config, image config, experimental features
3. `src/app/**/page.tsx` — RSC vs client, streaming, Suspense
4. `src/components/**` — 'use client' directives, component size
5. `src/app/api/**/route.ts` — response size, query patterns
6. `src/lib/db/**` — connection pooling, query patterns
7. `src/middleware.ts` — edge performance, static bypass
8. `prisma/schema.prisma` — indexes, relations
9. `src/hooks/**` — client-side state, re-render patterns
10. `public/**` — unoptimized assets, large files

## Framework-Specific Adjustments

### Next.js App Router
- Server Components by default = +1 to RSC Architecture
- Automatic code splitting per route = +1 to Bundle Size
- `next/image` auto-optimization = +1 to Images
- Edge middleware = +1 to Edge/CDN

### Prisma
- Connection pooling via Neon adapter = +1 to DB Performance
- `select` limits returned fields = +1 to API Performance
- `@@index` on query fields = +1 to DB Performance

### React 19
- Automatic batching = +1 to Client Performance
- Server Actions reduce client JS = +1 to Bundle Size
