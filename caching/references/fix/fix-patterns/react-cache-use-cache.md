# Fix Patterns: React cache() + `"use cache"` Directive

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

## `"use cache"` Directive Fixes

### Fix: Cache Expensive Public Query
```typescript
import { cacheTag, cacheLife } from "next/cache";
import prisma from "@/lib/db";

// Cache product listing (public, changes rarely)
async function getProducts() {
  "use cache";
  cacheTag("products");
  cacheLife("hours");

  return prisma.product.findMany({
    select: { id: true, name: true, price: true, description: true },
    orderBy: { createdAt: "desc" },
  });
}

// Invalidate after product update:
import { revalidateTag } from "next/cache";
revalidateTag("products");
```

### Fix: Cache with User-Scoped Tags
```typescript
import { cacheTag, cacheLife } from "next/cache";
import prisma from "@/lib/db";

// For frequently read user data (purchase status):
async function getUserPurchase(userId: string) {
  "use cache";
  cacheTag(`user-${userId}-purchase`);
  cacheLife("minutes");

  return prisma.purchase.findUnique({
    where: {
      one_purchase_per_product: { userId, productType: "KING_TEMPLATE" },
    },
    select: { id: true, status: true, githubInviteSent: true },
  });
}

// Invalidate after purchase:
import { revalidateTag } from "next/cache";
revalidateTag(`user-${userId}-purchase`);
```

### When NOT to Use `"use cache"`
- User-specific data that changes frequently (session, real-time)
- Data that must be fresh on every request (payment status during checkout)
- Small apps where query cost is negligible
