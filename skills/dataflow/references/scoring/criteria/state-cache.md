# Criteria: State Management (8%) + Caching & Revalidation (10%)

## 5. State Management (8%)

### Score 9-10: Enterprise-grade
- Server Components handle all read-only/display data
- Client state limited to UI concerns (modals, forms, dropdowns)
- `useActionState` for form submission state
- `useOptimistic` for instant UI feedback
- No global state library (Redux/Zustand) for server data
- `revalidatePath`/`revalidateTag` after mutations instead of client refetch
- Data changes after user actions trigger server revalidation

### Score 7-8: Production-ready
- Server-first data fetching for most pages
- Client hooks used only for genuinely interactive features
- Mutations trigger proper revalidation
- Some manual `useState` + `fetch` where server action would work

### Score 5-6: Minimum
- Mix of server and client data fetching
- Custom hooks with `useState` + `useEffect` + `fetch`
- Some unnecessary state duplication
- No `useOptimistic`

### Score 3-4: Below minimum
- All data fetched client-side via `useEffect`
- Global state store holding server data
- Multiple sources of truth for same data
- `useState` + `setInterval` for polling

### Checklist
- [ ] Server Components for read-only data
- [ ] Client state only for UI concerns
- [ ] No global store for server data
- [ ] Mutations trigger server revalidation
- [ ] `useActionState` for form state (React 19)
- [ ] `useOptimistic` where applicable

## 6. Caching & Revalidation (10%)

### Score 9-10: Enterprise-grade
- `"use cache"` directive for expensive queries with `cacheTag()` and `cacheLife()`
- `revalidateTag` after mutations for targeted invalidation
- `revalidatePath` for full page revalidation after writes
- `Cache-Control: private, no-store` on authenticated API responses
- Static pages use ISR with `revalidate` for time-based updates
- `force-dynamic` only where truly needed (user-specific data)
- React `cache()` for request-level deduplication

### Score 7-8: Production-ready
- Cache-Control headers on API responses
- Some caching strategy exists
- `force-dynamic` used sparingly
- React `cache()` on frequently called functions

### Score 5-6: Minimum
- Some Cache-Control headers
- `force-dynamic` used broadly
- No tag-based invalidation
- No explicit caching strategy

### Score 3-4: Below minimum
- `force-dynamic` on every page
- No Cache-Control headers (proxy can cache user data)
- No `"use cache"` or ISR
- Stale data served after mutations

### Checklist
- [ ] `NO_CACHE_HEADERS` on authenticated responses
- [ ] `"use cache"` with `cacheTag()`/`cacheLife()` for expensive queries
- [ ] `revalidateTag`/`revalidatePath` after writes
- [ ] `force-dynamic` only where necessary
- [ ] React `cache()` for request deduplication
- [ ] Static pages with ISR where applicable
