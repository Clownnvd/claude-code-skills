# Data Flow Best Practices

## 1. Server Component Data Fetching

| Do | Don't |
|----|-------|
| Fetch data in `async` Server Components | `useEffect` + `fetch` for initial page data |
| `Promise.all` for parallel fetches | Sequential awaits creating waterfalls |
| `Suspense` per slow data source | Blocking entire page on one query |
| Direct DB/service calls in RSC | Fetch own `/api/*` routes from RSC |

## 2. Server/Client Composition

| Do | Don't |
|----|-------|
| `"use client"` at leaf components | `"use client"` at page level |
| Pass serializable props (string, number) | Pass functions or class instances across boundary |
| Children pattern for server-in-client | Convert entire subtrees to client components |

## 3. Prisma Queries

| Do | Don't |
|----|-------|
| `select` on every query | Bare `findMany()` returning all columns |
| `findUnique` for unique fields | `findFirst` on unique columns |
| `@@index` on lookup fields | Only auto-generated PK indexes |
| `$transaction` for atomic writes | Sequential creates without transaction |
| Singleton PrismaClient | Multiple instances |

## 4. API Route Design

| Do | Don't |
|----|-------|
| Consistent `{ success, data, error, code }` | Different shapes per endpoint |
| Zod `.safeParse()` on every input | Raw `req.json()` without validation |
| Auth check as first step (fail fast) | Auth check after business logic |
| Service layer separation | Prisma queries directly in route handler |
| Machine-readable error codes | Only human-readable strings |

## 5. State Management

| Do | Don't |
|----|-------|
| Server Components for read-only data | Client `useEffect` for initial data |
| `useState` for UI-only state (modals, forms) | Global store for server data |
| `revalidatePath` after mutations | Manual refetch from client |

## 6. Caching

| Do | Don't |
|----|-------|
| `NO_CACHE_HEADERS` on authenticated responses | Allow proxy caching of user data |
| `unstable_cache` with tags for expensive queries | `force-dynamic` on everything |
| `revalidateTag` after writes | No cache invalidation strategy |

## 7. Type Safety

| Do | Don't |
|----|-------|
| `z.infer<typeof schema>` for types | Duplicate type definitions |
| Shared schemas in `validations/` | Inline schemas per route |
| `ApiResponse<T>` generic | `any` in API response handling |
| Same schema on client and server | Different validation rules |

## 8. Error Propagation

| Do | Don't |
|----|-------|
| `error.tsx` per route segment | Only root-level error boundary |
| Wrap external API errors | Leak Stripe/GitHub error details |
| Non-fatal side effects don't crash main flow | GitHub invite failure crashes checkout |
| `not-found.tsx` + `notFound()` | Generic 404 page |

## 9. Form Handling

| Do | Don't |
|----|-------|
| `useActionState` + Server Actions | `onSubmit` + `preventDefault` + `fetch` |
| Zod validation in server action | Client-only validation |
| Loading states during submission | No feedback while submitting |
| Field-level error display | Generic "something went wrong" |

## 10. Data Transformation

| Do | Don't |
|----|-------|
| `select` as implicit DTO | Return full Prisma objects |
| `.toISOString()` for dates | Raw Date objects in JSON |
| Strip internal fields (userId, stripe IDs) | Leak database internals |
| Consistent naming (`avatarUrl` not `image`) | Mixed naming conventions |
