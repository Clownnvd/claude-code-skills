# Caching Strategy Fix — Best Practices

## Fix Discipline

| Rule | Why |
|------|-----|
| One category at a time | Easier to isolate regressions |
| Read file before editing | Tool requirement + context |
| Run `tsc --noEmit` after each file | Catch type errors immediately |
| Check build output after static/dynamic changes | Verify route classification |
| Don't cache auth-dependent data with `"use cache"` | Security risk |

## Safe Changes (apply freely)

- Adding `NO_CACHE_HEADERS` to API responses
- Adding `export const dynamic = "force-dynamic"` to API routes
- Adding `revalidatePath("/affected-path")` after Prisma writes
- Wrapping `getServerSession` with `cache()`
- Adding `Vary: Cookie` to responses
- Moving header auth from server to client-side `useSession()`
- Adding proxy matcher to skip static assets

## Dangerous Changes (verify carefully)

| Change | Risk | Mitigation |
|--------|------|------------|
| Remove `force-dynamic` | May serve stale data | Test with auth + mutations |
| Add `"use cache"` | May cache user-specific data | Only on public/shared queries |
| Change proxy matcher | May break auth protection | Test protected routes |
| Add ISR to auth pages | May serve other user's data | Only on public pages |
| CDN cache public API | May leak data if auth changes | Check Vary headers |

## Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| `"use cache"` on user-specific data | Use `NO_CACHE_HEADERS` instead |
| `force-dynamic` on landing page | Move auth to client, keep page static |
| `revalidatePath("/")` after mutation | Revalidate specific path only |
| `cache()` across requests | `cache()` is per-request in RSC |
| CDN cache without Vary header | Add `Vary: Cookie` or `Vary: Authorization` |
| Missing `NO_CACHE_HEADERS` = proxy caching user data | Always add to auth responses |

## When NOT to Fix

- Score 9-10: Diminishing returns
- Requires infrastructure (Redis for advanced caching) — flag as "requires setup"
- ISR on a pure dashboard app — may not be applicable
- CDN edge functions on dev/staging — flag as "production-only"
