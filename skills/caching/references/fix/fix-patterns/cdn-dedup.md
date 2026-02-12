# Fix Patterns: CDN & Edge + Request Deduplication

## CDN & Edge Fixes

### Fix: Add Vary Header on Auth-Dependent Responses
```typescript
// For responses that vary by authentication:
return successResponse(data, 200, {
  ...NO_CACHE_HEADERS,
  "Vary": "Cookie",
});
```

### Fix: CDN-Cacheable Public Response
```typescript
// Health/status endpoint:
return successResponse({ status: "ok" }, 200, {
  "Cache-Control": "public, s-maxage=10, stale-while-revalidate=30",
});
```

### Fix: Static Asset Headers in next.config.ts
```typescript
// next.config.ts
const nextConfig = {
  async headers() {
    return [
      {
        source: "/_next/static/(.*)",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=31536000, immutable",
          },
        ],
      },
    ];
  },
};
```

## Request Deduplication Fixes

### Fix: Promise.all for Parallel Data
```typescript
// BEFORE: Sequential waterfalls
const user = await prisma.user.findUnique({ where: { id: userId } });
const purchase = await prisma.purchase.findUnique({ ... });
const settings = await prisma.settings.findFirst({ ... });

// AFTER: Parallel with Promise.all
const [user, purchase, settings] = await Promise.all([
  prisma.user.findUnique({ where: { id: userId }, select: { name: true } }),
  prisma.purchase.findUnique({ where: { ... }, select: { status: true } }),
  prisma.settings.findFirst({ where: { userId }, select: { theme: true } }),
]);
```

### Fix: Share Data Between Layout and Page
```typescript
// BEFORE: Both layout and page fetch user
// layout.tsx
const user = await getUser(userId);
// page.tsx
const user = await getUser(userId); // DUPLICATE

// AFTER: Use cache() for request dedup
// lib/loaders.ts
import { cache } from "react";
export const getUser = cache(async (userId: string) => {
  return prisma.user.findUnique({ where: { id: userId } });
});

// Both layout.tsx and page.tsx call getUser() — only 1 DB query
```

### Fix: Avoid Fetching Own API Routes from Server
```typescript
// BEFORE: Server component calling own API
const res = await fetch("http://localhost:3000/api/user/purchase");

// AFTER: Direct DB query in Server Component
const purchase = await prisma.purchase.findUnique({
  where: { one_purchase_per_product: { userId, productType: "KING_TEMPLATE" } },
  select: { id: true, status: true },
});
```
