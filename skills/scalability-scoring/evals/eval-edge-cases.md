# Scalability Scoring — Edge Cases Eval

Verify correct behavior for scalability-specific edge cases.

## Test 1: Large Bundle With Barrel Re-Exports

- Provide codebase using `export * from` barrel files importing heavy libraries
- Verify Bundle Size scores <= 3 (CRITICAL)
- Verify issue identifies specific barrel files and their import cost
- Verify fix recommends direct imports or dynamic imports

## Test 2: Images Without next/image

- Provide pages using raw `<img>` tags instead of `next/image`
- Verify Image Optimization scores <= 3
- Verify issue lists specific image elements missing optimization
- Verify fix recommends `next/image` with width, height, and format props

## Test 3: N+1 Database Queries

- Provide code looping over records and querying DB inside the loop
- Verify DB Query Performance scores <= 2 (CRITICAL)
- Verify issue identifies the N+1 pattern with file and line reference
- Verify fix recommends `include`, `findMany` with `where IN`, or batch query

## Test 4: No Code Splitting on Heavy Components

- Provide pages importing large libraries (chart, editor, map) statically
- Verify Bundle Size penalized for missing `dynamic()` or `React.lazy`
- Verify Client-Side Performance also flagged for initial load impact
- Verify fix recommends `next/dynamic` with `ssr: false` where applicable

## Test 5: Sequential Fetches Instead of Parallel

- Provide server components with `await` chains for independent data
- Verify Concurrency scores <= 4
- Verify issue identifies specific sequential await patterns
- Verify fix recommends `Promise.all` for independent fetches

## Test 6: No Web Vitals Tracking

- Provide codebase with no performance monitoring or Lighthouse CI
- Verify Performance Monitoring scores <= 2
- Verify issue recommends Web Vitals reporting and bundle budgets
- Verify fix suggests `reportWebVitals` or Vercel Analytics

## Test 7: Memory Leaks in Client Components

- Provide components with event listeners or intervals without cleanup
- Verify Memory & Resource Management scores <= 3
- Verify issue identifies missing cleanup in useEffect return
- Verify fix recommends AbortController and cleanup functions
