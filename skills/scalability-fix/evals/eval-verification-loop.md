# Eval: Scalability Fix Verification Loop

Verify the compile-test-rescore cycle, regression detection, and fix idempotency for scalability-fix.

## Test 1: Compile + Test Verification

**Setup**: Scorecard with CRITICAL issue: heavy library (`chart.js`, 200KB) imported at top level in a client component (Bundle Size 3/10). Apply the Dynamic Import fix from `bundle-images.md` which converts to `next/dynamic` with `{ ssr: false }`.

**Steps**:
1. Replace `import Chart from 'chart.js'` with `const Chart = dynamic(() => import('chart.js'), { ssr: false })`.
2. Run `npx tsc --noEmit`. Verify zero type errors from dynamic import wrapper.
3. Run `pnpm test`. Verify chart component tests still pass (mock may need update).
4. Run `pnpm build`. Verify bundle analyzer (if available) shows chart.js in a separate chunk.

**Pass**: `tsc --noEmit` exits 0. All tests pass. Build succeeds with chart.js code-split into its own chunk. No `'use client'` directive added to a previously server-rendered parent.

**Fail**: Type error from dynamic component props, test failure from SSR mismatch, or chart.js still in main bundle.

## Test 2: Re-Score Improvement Verification

**Setup**: Initial scalability-scoring scorecard: Bundle Size 3/10, RSC Architecture 5/10, DB Performance 4/10. Total 44/100 (D+). Apply fixes for dynamic imports (Bundle Size) and N+1 query batching with `Promise.all` (DB Performance).

**Steps**:
1. Run scalability-fix for both issues.
2. Invoke `scalability-scoring` to produce a new scorecard.
3. Compare per-category scores: Bundle Size, DB Performance must increase.
4. Verify RSC Architecture, Concurrency, Rendering, and all other categories remain at or above pre-fix scores.

**Pass**: Bundle Size >= 6/10 (was 3). DB Performance >= 7/10 (was 4). No category dropped below its pre-fix score. Total weighted score increased. N+1 queries replaced with batched `Promise.all` or `findMany({ where: { id: { in: ids } } })`.

**Fail**: Any unfixed category score decreased, or N+1 pattern still present in fixed queries.

## Test 3: Regression Detection

**Setup**: Initial scorecard: RSC Architecture 8/10, Bundle Size 7/10, Rendering 7/10. Apply a bundle size fix that adds `"use client"` to a shared layout component to enable dynamic imports, moving server-rendered content to client. RSC Architecture drops from 8/10 to 4/10.

**Steps**:
1. Apply `"use client"` to `src/app/layout.tsx` to support dynamic chart import.
2. Run `scalability-scoring` re-score.
3. Verify pipeline detects RSC Architecture dropped from 8 to 4 (delta -4).
4. Verify pipeline halts and recommends extracting the chart into a leaf Client Component instead.

**Pass**: Pipeline detects the RSC Architecture regression. Output flags: layout converted to Client Component unnecessarily, before/after delta shown, recommendation to isolate `"use client"` to leaf components. Pipeline does not continue.

**Fail**: Pipeline ignores the RSC regression and continues, or fails to identify that `"use client"` on layout caused the architecture score drop.

## Test 4: Fix Idempotency

**Setup**: Scorecard with CRITICAL issue: heavy library at top level. The chart component already uses `next/dynamic` with `{ ssr: false }` from a previous fix run.

**Steps**:
1. Run scalability-fix with the same bundle size issue.
2. Check `git diff` after the fix attempt.
3. Run `scalability-scoring` and compare scores to the post-first-fix scorecard.

**Pass**: No files modified (`git diff` is empty). Score remains identical. Skill reports "already applied" or "no changes needed." No nested dynamic wrappers or duplicate `ssr: false` configurations.

**Fail**: Double-wrapped dynamic import, duplicate loading component, or score changes from the second application.
