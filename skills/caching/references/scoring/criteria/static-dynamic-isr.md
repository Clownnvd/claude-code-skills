# Criteria: Static vs Dynamic Classification (12%) + ISR Configuration (8%)

## 3. Static vs Dynamic Classification (12%)

### Score 9-10: Enterprise-grade
- Landing/marketing pages are fully static (no server session reads)
- Auth check moved to client-side `useSession()` for non-critical UI
- Only auth-dependent pages/routes use `force-dynamic`
- `export const dynamic = "force-dynamic"` explicit (not implicit via cookies())
- No page accidentally made dynamic by layout/header session read
- Public pages (landing, pricing, docs) generate at build time
- Blog/content pages use static generation

### Score 7-8: Production-ready
- Most public pages are static
- Auth pages correctly dynamic
- Some pages unnecessarily dynamic
- Landing page mostly static

### Score 5-6: Minimum
- Mix of static and dynamic with no clear strategy
- Landing page dynamic due to auth header
- Some pages using `force-dynamic` unnecessarily

### Score 3-4: Below minimum
- All pages `force-dynamic`
- No static generation
- Server session read in root layout makes everything dynamic

### Checklist
- [ ] Landing page is fully static
- [ ] Auth check in header is client-side
- [ ] Public pages generate at build time
- [ ] `force-dynamic` only on auth-dependent pages/routes
- [ ] No accidental dynamic rendering from layout
- [ ] `export const dynamic` explicit where needed

## 4. ISR Configuration (8%)

### Score 9-10: Enterprise-grade
- Public content pages have `revalidate` configured
- `revalidate = 3600` (or appropriate TTL) on semi-static pages
- On-demand revalidation via webhook for content updates
- `stale-while-revalidate` pattern for good UX
- ISR used for pages that change infrequently

### Score 7-8: Production-ready
- Some ISR configuration exists
- Time-based revalidation on public pages
- No on-demand revalidation

### Score 5-6: Minimum
- ISR not configured but pages could benefit
- All public pages either fully static or fully dynamic
- No revalidation strategy for content

### Score 3-4: Below minimum
- No ISR at all
- Public pages always rebuilt or never updated
- No concept of time-based freshness

### N/A Adjustment
If the app has no semi-static content pages (pure SPA dashboard + static landing), score ISR based on:
- Landing page: could benefit from ISR if content changes
- If truly N/A: redistribute 8% weight to Headers (20%) + Revalidation (18%)

### Checklist
- [ ] `revalidate` on public content pages
- [ ] Appropriate TTL values
- [ ] On-demand revalidation for content updates
- [ ] ISR where pages change infrequently
