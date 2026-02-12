# Data Flow Scoring — Edge Cases Eval

Verify correct behavior for data-flow-specific edge cases.

## Test 1: Client-Side useEffect for Initial Data

- Provide components using `useEffect` + `fetch` for initial page data
- Verify RSC Data Fetching scores <= 3 (CRITICAL)
- Verify issue recommends converting to async server component
- Verify Server/Client Composition also penalized

## Test 2: "use client" at Page Level

- Provide pages with `"use client"` at the top, wrapping entire page trees
- Verify Server/Client Composition scores <= 3
- Verify issue identifies specific pages that should be server components
- Verify fix recommends pushing `"use client"` to leaf components

## Test 3: Prisma Queries Without select

- Provide services using `findMany` without `select` (fetching all fields)
- Verify Prisma Query Optimization scores <= 4
- Verify issue references specific queries returning excess data
- Verify DTO category also penalized for Prisma model leaks

## Test 4: No Zod Validation at API Boundaries

- Provide API routes accepting request bodies without schema validation
- Verify Type Safety scores <= 3 (CRITICAL)
- Verify API Route Design also penalized
- Verify fix recommends Zod schema at route boundary

## Test 5: Missing error.tsx Boundaries

- Provide app routes without `error.tsx` files
- Verify Error Propagation scores <= 4
- Verify issue lists route segments lacking error boundaries
- Verify fix recommends adding `error.tsx` at key layout levels

## Test 6: Forms Without Loading States

- Provide form components with no `useFormStatus` or loading indicators
- Verify Form Handling scores <= 5
- Verify issue recommends pending state, optimistic updates, or loading UI

## Test 7: Non-Serializable Props Crossing Server/Client

- Provide server components passing Date objects or functions to client components
- Verify Server/Client Composition penalized
- Verify Type Safety also penalized for boundary violation
- Verify fix recommends serializing to ISO strings or primitives
