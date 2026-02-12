# Eval: Caching Fix Patterns

Verify specific fix patterns from `references/fix-patterns/` produce correct code changes.

## Pattern 1: NO_CACHE_HEADERS on Authenticated Responses (headers-revalidation.md)

**Setup**: Authenticated API routes return `successResponse(data)` without cache headers. User-specific data could be cached by intermediaries.

**Steps**:
1. Apply NO_CACHE_HEADERS pattern.
2. Verify `NO_CACHE_HEADERS` constant defined as `{ "Cache-Control": "private, no-store" }`.
3. Verify all authenticated API routes pass `NO_CACHE_HEADERS` to `successResponse()`.

**Pass**: Every authenticated route returns `Cache-Control: private, no-store`. Public endpoints (health) use `public, s-maxage` instead.

**Fail**: Authenticated routes still missing cache headers, or public endpoints get `no-store`.

## Pattern 2: cache() Session Dedup (react-cache-use-cache.md)

**Setup**: Multiple Server Components in the same request tree each call `auth.api.getSession()`, causing duplicate DB queries.

**Steps**:
1. Apply `cache()` wrapper pattern.
2. Verify `getServerSession` exported from `src/lib/auth/server.ts` wrapped with `cache()`.
3. Verify layout.tsx and page.tsx both import from the shared cached function.

**Pass**: Single DB query per request even when multiple components call `getServerSession()`. `cache()` import from `"react"`. Both layout and page use the shared function.

**Fail**: Components still call `auth.api.getSession()` directly, or `cache()` imported from wrong package.

## Pattern 3: Static Page Conversion (static-dynamic-isr.md)

**Setup**: Landing page renders dynamically because header reads server session via `headers()`.

**Steps**:
1. Apply Static Page Conversion pattern.
2. Verify server-side session check moved to client component using `useSession()`.
3. Verify `export const dynamic = "force-dynamic"` removed from landing page.
4. Verify `pnpm build` output shows landing page as static (circle icon).

**Pass**: Landing page builds as static. Auth state checked client-side. No `headers()` or `cookies()` call in the page tree.

**Fail**: Page still dynamic in build output, or auth check removed entirely.

## Pattern 4: revalidatePath After Mutations (headers-revalidation.md)

**Setup**: Prisma `create`/`update` calls in API routes and webhooks do not trigger cache revalidation. Dashboard shows stale data after purchase.

**Steps**:
1. Apply revalidatePath pattern.
2. Verify `revalidatePath("/dashboard")` called after purchase creation.
3. Verify webhook handlers also call revalidation.

**Pass**: After `prisma.purchase.create()`, `revalidatePath("/dashboard")` called. Stripe webhook handler includes revalidation. Dashboard reflects new purchase without manual refresh.

**Fail**: No revalidation added, or revalidation on wrong path, or only added in API route but not webhook.
