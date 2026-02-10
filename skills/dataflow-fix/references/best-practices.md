# Data Flow Fix — Best Practices

## Fix Discipline

| Rule | Why |
|------|-----|
| One category at a time | Easier to isolate regressions |
| Read file before editing | Tool requirement + context |
| Run `tsc --noEmit` after each file | Catch type errors immediately |
| Don't change response shapes without updating clients | Breaking change |
| Prefer additive changes over rewrites | Lower risk |

## Safe Changes (apply freely)

- Adding `select: { ... }` to Prisma queries
- Adding `loading.tsx`, `error.tsx`, `not-found.tsx` files
- Adding `NO_CACHE_HEADERS` to API responses
- Adding Zod `.safeParse()` to inputs
- Adding `@@index` to schema.prisma
- Adding `.toISOString()` to date fields in responses
- Moving `"use client"` from parent to child component
- Adding `cache()` wrapper to frequently called server functions

## Dangerous Changes (verify carefully)

| Change | Risk | Mitigation |
|--------|------|------------|
| Client → Server Component | May break event handlers | Check for useState/useEffect first |
| API response shape change | Breaks client consumers | Update hooks + test |
| Remove `force-dynamic` | May serve stale data | Test with mutations |
| Schema migration | DB downtime | Backup + test migration |
| Form: API route → Server Action | Different error handling | Rewrite form completely |

## Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Adding `async` to client component | Only Server Components can be async |
| `useEffect` fetch in RSC page | Remove `"use client"`, fetch directly |
| `fetch('/api/user')` in Server Component | Call `prisma.user.findUnique()` directly |
| `"use cache"` on authenticated data | Use `NO_CACHE_HEADERS` instead |
| `select: true` (selects everything) | `select: { id: true, name: true }` |
| `findFirst` on unique field | Use `findUnique` |

## When NOT to Fix

- Score 9-10: Diminishing returns
- Requires infrastructure (Redis for cache) — flag as "requires setup"
- Would change API contract with existing clients — flag as "breaking change"
- React 19 features not yet stable — flag as "framework limitation"
