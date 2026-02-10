# Fix Patterns: State Management + Caching

## State Management Fixes

### Fix: Replace Client Fetch with Server Component
```typescript
// BEFORE: Client component fetching on mount
"use client";
function UserProfile() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch("/api/user/profile").then(r => r.json()).then(d => setUser(d.data));
  }, []);
  if (!user) return <Skeleton />;
  return <div>{user.name}</div>;
}

// AFTER: Server Component fetches directly
async function UserProfile() {
  const session = await getServerSession();
  if (!session) return null;
  const user = await prisma.user.findUnique({
    where: { id: session.user.id },
    select: { name: true, email: true, image: true },
  });
  return <div>{user?.name}</div>;
}
```

### Fix: Use revalidatePath After Mutations
```typescript
// In server action or API route after successful mutation:
import { revalidatePath } from "next/cache";

// After profile update:
revalidatePath("/dashboard/settings/profile");

// After purchase:
revalidatePath("/dashboard");
```

### Fix: Minimal Client State
```typescript
// BEFORE: Too much client state
const [isOpen, setIsOpen] = useState(false);
const [userData, setUserData] = useState(null);  // Server data in client state
const [purchases, setPurchases] = useState([]);  // Server data in client state

// AFTER: Only UI state in client
const [isOpen, setIsOpen] = useState(false);  // UI state = OK
// userData and purchases fetched in Server Component
```

## Caching Fixes

### Fix: Add NO_CACHE_HEADERS to Authenticated Responses
```typescript
export const NO_CACHE_HEADERS = {
  "Cache-Control": "private, no-store",
} as const;

// Usage in API route:
return successResponse(data, 200, NO_CACHE_HEADERS);
```

### Fix: Request-Level Dedup with cache()
```typescript
import { cache } from "react";

export const getServerSession = cache(async () => {
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  return session;
});
```

### Fix: "use cache" Directive for Expensive Queries
```typescript
import { cacheTag, cacheLife } from "next/cache";

async function getProducts() {
  "use cache"
  cacheTag("products")
  cacheLife("hours")
  return prisma.product.findMany({
    select: { id: true, name: true, price: true },
  });
}

// Invalidate after product update:
revalidateTag("products");
```

### Fix: Remove Unnecessary force-dynamic
```typescript
// BEFORE: force-dynamic everywhere
export const dynamic = "force-dynamic"; // On a page that could be static

// AFTER: Only where needed
// Remove force-dynamic from pages that don't use cookies/headers
// Keep it on pages that read session data
```
