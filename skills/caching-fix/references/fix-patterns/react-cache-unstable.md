# Fix Patterns: React cache() + unstable_cache

## React cache() Fixes

### Fix: Wrap getServerSession with cache()
```typescript
// BEFORE: Multiple session lookups per request
// layout.tsx calls auth.api.getSession
// page.tsx calls auth.api.getSession
// Each = separate DB query

// AFTER: Request-level dedup with cache()
// src/lib/auth/server.ts
import { cache } from "react";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

export const getServerSession = cache(async () => {
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  return session;
});

export const requireUserId = cache(async (): Promise<string> => {
  const session = await getServerSession();
  if (!session?.user?.id) {
    throw new Error("Unauthorized");
  }
  return session.user.id;
});
```

### Fix: Shared Data Loader with cache()
```typescript
import { cache } from "react";
import prisma from "@/lib/db";

// Called from multiple Server Components in same request:
export const getUserProfile = cache(async (userId: string) => {
  return prisma.user.findUnique({
    where: { id: userId },
    select: { id: true, name: true, email: true, image: true },
  });
});
```

## unstable_cache Fixes

### Fix: Cache Expensive Public Query
```typescript
import { unstable_cache } from "next/cache";
import prisma from "@/lib/db";

// Cache product listing (public, changes rarely)
export const getProducts = unstable_cache(
  async () => {
    return prisma.product.findMany({
      select: { id: true, name: true, price: true, description: true },
      orderBy: { createdAt: "desc" },
    });
  },
  ["products-list"],
  { tags: ["products"], revalidate: 3600 }
);

// Invalidate after product update:
import { revalidateTag } from "next/cache";
revalidateTag("products");
```

### Fix: Cache with User-Scoped Tags
```typescript
// For frequently read user data (purchase status):
export const getUserPurchase = unstable_cache(
  async (userId: string) => {
    return prisma.purchase.findUnique({
      where: {
        one_purchase_per_product: { userId, productType: "KING_TEMPLATE" },
      },
      select: { id: true, status: true, githubInviteSent: true },
    });
  },
  ["user-purchase"],
  { tags: [`user-${userId}-purchase`], revalidate: 300 }
);

// Invalidate after purchase:
revalidateTag(`user-${userId}-purchase`);
```

### When NOT to Use unstable_cache
- User-specific data that changes frequently (session, real-time)
- Data that must be fresh on every request (payment status during checkout)
- Small apps where query cost is negligible
