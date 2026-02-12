# Scalability Fix — Best Practices

## Fix Discipline

| Do | Don't |
|----|-------|
| Fix one issue at a time | Batch unrelated changes |
| Verify after each fix | Apply all fixes then test |
| Keep changes minimal | Refactor surrounding code |
| Test in dev before claiming fixed | Assume fix is correct |
| Document what changed and why | Silent fixes |

## Common Mistakes

### 1. Over-optimization
- Don't memoize everything — `React.memo` and `useMemo` have overhead
- Don't add `select` if you need all fields
- Don't force static generation if page needs per-request data

### 2. Breaking Changes
- Converting client component to server may break event handlers
- Adding ISR may cause stale data for time-sensitive content
- Changing proxy matcher may break auth redirects

### 3. False Fixes
- Adding `priority` to ALL images (only above-fold)
- Adding `@@index` on fields never queried
- Adding Suspense with no async children

## Category-Specific Tips

### Bundle Size
- Check `pnpm ls <package>` to verify package is actually in production bundle
- `devDependencies` don't affect bundle unless imported in app code
- Next.js auto-splits per route — manual splitting needed only for large in-page libs

### Database
- `select` returns typed partial objects — callers may need updating
- `@@index` requires migration — add to schema then `pnpm prisma migrate dev`
- `Promise.all` for queries only when they're truly independent (no FK dependency)

### Server Components
- A component without `'use client'` is automatically a Server Component in App Router
- Children of client components can still be Server Components if passed as `children` prop
- Don't remove `'use client'` if component uses hooks (useState, useEffect, etc.)

### Proxy
- Test proxy changes with `curl` to verify auth still works
- Proxy runs on EVERY matched request — keep it fast
- Don't add DB queries to proxy — keep it lightweight
