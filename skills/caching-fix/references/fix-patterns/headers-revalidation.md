# Fix Patterns: Cache-Control Headers + Revalidation

## Cache-Control Headers Fixes

### Fix: Add NO_CACHE_HEADERS to Authenticated API Response
```typescript
// BEFORE: No cache headers
return successResponse(data);

// AFTER: Private no-store on auth response
import { NO_CACHE_HEADERS } from "@/lib/api/response";
return successResponse(data, 200, NO_CACHE_HEADERS);
```

### Fix: Add export const dynamic to API Route
```typescript
// Add to every API route file:
export const runtime = "nodejs";
export const dynamic = "force-dynamic";
```

### Fix: Import NO_CACHE_HEADERS
```typescript
// In API route — add to import:
import {
  successResponse,
  unauthorizedError,
  serverError,
  NO_CACHE_HEADERS,  // ADD THIS
} from "@/lib/api/response";
```

### Fix: Public Cache on Health/Ready Endpoints
```typescript
// Health endpoint — cacheable for short time
return successResponse({ status: "ok" }, 200, {
  "Cache-Control": "public, max-age=10, s-maxage=10",
});
```

## Revalidation Fixes

### Fix: Add revalidatePath After Prisma Mutation
```typescript
import { revalidatePath } from "next/cache";

// After prisma.purchase.create/update:
revalidatePath("/dashboard");

// After prisma.user.update:
revalidatePath("/dashboard/settings/profile");
```

### Fix: Revalidate in Webhook Handler
```typescript
// In stripe webhook after purchase:
await prisma.purchase.create({ ... });
revalidatePath("/dashboard");

// In sepay webhook after transaction:
await processSepayTransaction(payload);
revalidatePath("/dashboard");
```

### Fix: Revalidate in Server Action
```typescript
"use server";
import { revalidatePath } from "next/cache";

export async function updateProfile(formData: FormData) {
  // ... validation + DB update
  revalidatePath("/dashboard/settings/profile");
  return { success: true };
}
```

### Fix: Tag-Based Revalidation
```typescript
import { revalidateTag } from "next/cache";

// After write:
revalidateTag("user-purchases");

// In cached query:
const getPurchases = unstable_cache(
  async (userId) => prisma.purchase.findMany({ where: { userId } }),
  ["user-purchases"],
  { tags: ["user-purchases"] }
);
```
