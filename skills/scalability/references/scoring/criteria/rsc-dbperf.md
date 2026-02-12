# Server Component Architecture (12%) + Database Query Performance (12%)

## Category 3: Server Component Architecture (12%)

### Criteria (10 items, each worth 1 point)

1. **Server Components by default** — Pages and layouts are Server Components unless they need interactivity (free +1 for App Router)
2. **Minimal 'use client' surface** — `'use client'` pushed to leaf nodes, not at page/layout level. Count `'use client'` directives vs total components
3. **No entire pages as client** — No page.tsx files with `'use client'` at top. Interactive parts extracted to client child components
4. **Suspense boundaries** — Async data fetching wrapped in `<Suspense>` with fallback for streaming
5. **No prop-drilling from server to client** — Data fetched close to where it's used, not fetched in parent and drilled through props
6. **Serializable props only** — No functions, Dates, Maps, or class instances passed from Server to Client components
7. **Streaming for slow data** — Slow API calls or DB queries use streaming (Suspense) instead of blocking entire page render
8. **Server Actions for mutations** — Form submissions use Server Actions or API routes, not client-side fetch in Server Components
9. **No unnecessary re-renders** — Client components don't wrap large Server Component trees (would force entire subtree to be client)
10. **Proper error boundaries** — `error.tsx` files for route segments, graceful degradation

### Deduction Examples
- `-3` Entire page marked `'use client'` when only a button needs interactivity
- `-2` No Suspense boundaries around async operations
- `-2` Functions passed as props from Server to Client components
- `-1` Missing error.tsx for key route segments

---

## Category 4: Database Query Performance (12%)

### Criteria (10 items, each worth 1 point)

1. **Connection pooling** — Using pgbouncer, Neon serverless adapter, or Prisma connection pool (free +1 for Neon adapter)
2. **Select specific fields** — Queries use `select` to limit returned columns, not fetching entire rows
3. **Indexed query fields** — `@@index` on fields used in `where`, `orderBy`, `unique` constraints on lookup fields
4. **No N+1 queries** — Related data fetched with `include` or joined query, not loop of individual queries
5. **findUnique for PK** — Primary key / unique field lookups use `findUnique`, not `findFirst`
6. **Batch independent queries** — Multiple unrelated queries use `Promise.all` instead of sequential `await`
7. **Pagination on lists** — List queries use `take`/`skip` or cursor-based pagination, not unbounded `findMany`
8. **No raw SQL without parameterization** — Any `$queryRaw` uses parameterized queries (`Prisma.sql` tagged template)
9. **Efficient relations** — `include` used judiciously (not including entire relation trees), `select` on included relations
10. **Migration indexes** — Migration files include index creation for new query patterns

### Deduction Examples
- `-3` N+1 query pattern (loop of findFirst inside map/forEach)
- `-2` No connection pooling for serverless
- `-2` Missing indexes on frequently queried fields
- `-1` findFirst used where findUnique would work

### Framework Adjustment
Prisma with Neon serverless adapter = +1 to connection pooling criterion.
