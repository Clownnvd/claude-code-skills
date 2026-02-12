# Eval: Scalability Fix Patterns

Verify specific fix patterns from `references/fix-patterns/` produce correct code changes.

## Pattern 1: Dynamic Import Heavy Libraries (bundle-images.md)

**Setup**: `chart.js` imported at top level in a dashboard component, adding 200KB to initial bundle.

**Steps**:
1. Apply Dynamic Import pattern.
2. Verify top-level `import { Chart } from 'chart.js'` replaced with `next/dynamic`.
3. Verify `{ ssr: false }` set for browser-only libraries.
4. Verify `pnpm build` shows reduced First Load JS for the page.

**Pass**: Chart component lazy-loaded. Initial bundle does not include chart.js. Component renders after hydration with loading state.

**Fail**: Top-level import remains, or `ssr: false` missing for browser-only lib, or bundle size unchanged.

## Pattern 2: Extract Client Interactivity (rsc-dbperf.md)

**Setup**: Entire product page has `"use client"` because one button uses `useState`. Static content (headings, descriptions) shipped as client JS.

**Steps**:
1. Apply Extract Client Interactivity pattern.
2. Verify button extracted to separate `"use client"` component.
3. Verify page component is now a Server Component (no directive).
4. Verify static content rendered server-side.

**Pass**: Only interactive button is a client component. Page is server-rendered. `pnpm build` shows reduced client JS for the route.

**Fail**: Page still has `"use client"`, or extraction breaks event handling.

## Pattern 3: Promise.all for Parallel Fetches (concurrency-monitoring.md)

**Setup**: Layout fetches user, preferences, and history sequentially. Total waterfall time is sum of all three queries.

**Steps**:
1. Apply Promise.all pattern.
2. Verify sequential `await` calls replaced with `Promise.all([...])`.
3. Verify destructuring matches original variable names.
4. Verify independent queries identified correctly (no data dependency between them).

**Pass**: Three queries run in parallel. Total time equals slowest query, not sum. Error in one query propagates correctly. Dependent queries (where output of A feeds into B) kept sequential.

**Fail**: Still sequential, or dependent queries incorrectly parallelized.

## Pattern 4: Bounded In-Memory Cache (edge-memory.md)

**Setup**: Rate limiter uses unbounded `new Map()` that grows indefinitely in long-running processes.

**Steps**:
1. Apply Bounded Cache pattern.
2. Verify `BoundedCache` class with `maxSize` and `ttlMs` parameters.
3. Verify eviction of oldest entry when `maxSize` reached.
4. Verify expired entries return `undefined` on `get()`.

**Pass**: Cache has configurable max size (e.g., 10000 entries). Entries expire after TTL. Old entries evicted when full. Rate limiter uses bounded cache instead of raw Map.

**Fail**: No size limit, or no TTL expiry, or eviction breaks rate limiting logic.
