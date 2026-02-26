# Criteria: Server Component Fetching (15%) + Server/Client Composition (10%)

## 1. Server Component Data Fetching (15%)

### Score 9-10: Enterprise-grade
- All page components are `async` Server Components
- Data fetched directly via DB/service calls (never own `/api/*` routes)
- `Promise.all` for parallel independent fetches
- `Suspense` boundaries per slow data source
- `loading.tsx` at appropriate route segments
- Components co-located with their data needs
- No `useEffect` + `fetch` for initial page data

### Score 7-8: Production-ready
- Pages fetch data server-side
- Some sequential fetches but no critical waterfalls
- At least one Suspense boundary exists
- No client-side initial data fetching for main content

### Score 5-6: Minimum
- Mix of server and client data fetching
- Some pages use RSC correctly, others rely on client hooks
- No Suspense or loading states

### Score 3-4: Below minimum
- `"use client"` at page level with useEffect for all data
- Fetching own API routes from Server Components
- No streaming, entire page blocks on slowest query

### Score 0-2: Critical
- All data fetched client-side
- No Server Components used for data
- Waterfall queries with no optimization

### Checklist
- [ ] Page components are `async` Server Components
- [ ] Direct DB/service calls (not own API routes)
- [ ] Parallel fetching with `Promise.all`
- [ ] `Suspense` boundaries for slow data
- [ ] `loading.tsx` at route segments
- [ ] No `useEffect` + `fetch` for initial page data

## 2. Server/Client Component Composition (10%)

### Score 9-10: Enterprise-grade
- `"use client"` only at leaf interactive components (buttons, forms, modals)
- Server Components pass serializable data only (string, number, boolean)
- Children pattern for nesting Server Components inside Client Components
- No unnecessary `"use client"` on render-only components
- Client Components receive minimal data (not full DB objects)

### Score 7-8: Production-ready
- `"use client"` at component level (not page level)
- Mostly serializable props
- Some over-fetching but no critical issues

### Score 5-6: Minimum
- `"use client"` on mid-level components
- Some non-serializable data crosses boundary
- Generally works but not optimized

### Score 3-4: Below minimum
- `"use client"` at layout or page level
- Non-serializable props (functions, Date objects, Prisma models)
- No distinction between server and client components

### Checklist
- [ ] `"use client"` at leaf components only
- [ ] Serializable props across boundary
- [ ] Children pattern used for server-in-client nesting
- [ ] No full DB objects passed to client components
- [ ] Interactive elements isolated in small client components
