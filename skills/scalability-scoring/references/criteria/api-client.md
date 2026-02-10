# API Response Performance (10%) + Client-Side Performance (10%)

## Category 5: API Response Performance (10%)

### Criteria (10 items, each worth 1 point)

1. **Return only needed fields** — API responses don't return full database objects. Use `select` or map to response shape
2. **Paginated list endpoints** — Any endpoint returning lists has pagination (take/skip, cursor, or limit/offset)
3. **Appropriate HTTP status codes** — 200 for success, 201 for creation, 400 for validation, 401 for auth, 404 for not found, 500 for server errors. Not always 200 with error in body
4. **Consistent response format** — All API routes use shared response helpers (e.g., `apiSuccess()`, `apiError()`)
5. **Request body size limits** — POST/PUT routes validate request body size or use schema validation to reject oversized payloads
6. **No over-fetching in handlers** — API routes fetch only the data they need, not loading entire objects then filtering
7. **Efficient serialization** — No redundant JSON.parse/JSON.stringify cycles. Response objects are clean
8. **Error responses don't leak internals** — Error messages are user-friendly, no stack traces, no internal paths, no SQL errors
9. **Compression enabled** — Response compression via Next.js (default) or explicit gzip/brotli headers
10. **Timeout handling** — External API calls have timeout/AbortController, not unbounded fetch

### Deduction Examples
- `-3` Returning full database rows including sensitive fields
- `-2` No pagination on list endpoints
- `-2` Internal error details leaked to client
- `-1` Missing AbortController on external fetches

---

## Category 6: Client-Side Performance (10%)

### Criteria (10 items, each worth 1 point)

1. **Minimal 'use client' surface** — Interactive components are small, focused leaf nodes (shared with RSC category, counted once)
2. **No layout thrashing** — No reading DOM properties (offsetHeight) then writing (style) in the same synchronous block
3. **Debounced frequent events** — Search inputs, scroll handlers, resize listeners use debounce/throttle
4. **CSS animations preferred** — Animations use CSS transitions/transforms, not JS-driven layout changes
5. **Memoization where needed** — Expensive computations use `useMemo`, expensive components use `React.memo` — but not over-applied
6. **No unnecessary state** — Derived values computed from existing state, not stored as separate state
7. **Event handler optimization** — No inline function creation in render for stable handlers (useCallback where needed for child component deps)
8. **Efficient list rendering** — Lists use proper `key` props (not index for dynamic lists), virtualized if >100 items
9. **No blocking renders** — Heavy components wrapped in `React.lazy` + Suspense, transitions use `startTransition`
10. **React 19 automatic batching** — State updates naturally batched (free +1 for React 19)

### Deduction Examples
- `-3` Layout thrashing in animation/scroll handler
- `-2` Missing debounce on search input making API calls
- `-2` Over-memoization (useMemo on every value, React.memo on every component)
- `-1` Index used as key in dynamic list
