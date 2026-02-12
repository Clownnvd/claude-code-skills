# Caching Scoring — Edge Cases Eval

Verify correct behavior for caching-specific edge cases.

## Test 1: No Cache Headers on Auth Responses

- Provide API routes returning auth tokens without `no-store` / `no-cache`
- Verify Cache-Control Headers penalized (score <= 3, CRITICAL)
- Verify issue flags specific routes caching sensitive data
- Verify fix recommends `NO_CACHE_HEADERS` constant pattern

## Test 2: force-dynamic on Every Page

- Provide app with `force-dynamic` on all pages including static-eligible ones
- Verify Static vs Dynamic Classification scores <= 3
- Verify issue identifies pages that should be static
- Verify ISR also penalized for missed opportunities

## Test 3: Mutations Without Revalidation

- Provide Server Actions or API routes that mutate data without `revalidatePath`/`revalidateTag`
- Verify Revalidation Strategy scores <= 2 (CRITICAL)
- Verify each mutation route is listed as an issue
- Verify fix recommends tag-based revalidation

## Test 4: Duplicate Fetch Calls in RSC Tree

- Provide server components making the same DB/fetch call multiple times per request
- Verify Request Deduplication scores <= 4
- Verify React cache() Deduplication also penalized if cache() not used
- Verify fix recommends `cache()` wrapper or `Promise.all`

## Test 5: No Cache Observability in Dev

- Provide codebase with no `x-cache` headers or cache hit/miss logging
- Verify Cache Monitoring scores <= 3
- Verify issue recommends adding debug headers in development

## Test 6: Heavy Operations in Proxy

- Provide proxy/middleware running expensive operations (DB queries, external fetches)
- Verify Proxy Caching scores <= 3
- Verify issue recommends moving logic out of proxy path

## Test 7: Static Assets Without CDN Headers

- Provide static asset responses missing `s-maxage` or `stale-while-revalidate`
- Verify CDN & Edge Caching scores <= 4
- Verify fix recommends Vercel edge config or CDN-friendly headers
