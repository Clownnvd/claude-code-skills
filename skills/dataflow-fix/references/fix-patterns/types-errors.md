# Fix Patterns: Type Safety + Error Propagation

## Type Safety Fixes

### Fix: Shared Zod Schemas
```typescript
// src/lib/validations/profile.ts
import { z } from "zod";

export const updateProfileSchema = z.object({
  name: z.string().min(1).max(100),
  avatarUrl: z.string().url().optional().or(z.literal("")),
});

export type UpdateProfileInput = z.infer<typeof updateProfileSchema>;

// Used in BOTH:
// 1. Client form: zodResolver(updateProfileSchema)
// 2. API route: updateProfileSchema.safeParse(body)
```

### Fix: Typed API Response Generic
```typescript
// src/types/index.ts
export type ApiResponse<T = unknown> = {
  success: boolean;
  data?: T;
  error?: string;
  code?: string;
  errors?: Record<string, string[]>;
};

// Client hook usage:
const response = await fetch("/api/user/purchase");
const data: ApiResponse<PurchaseResponse> = await response.json();
// data.data is typed as PurchaseResponse
```

### Fix: Remove any Types
```typescript
// BEFORE
const data: any = await response.json();

// AFTER
const data: ApiResponse<PurchaseResponse> = await response.json();
if (data.success && data.data) {
  // data.data is fully typed
}
```

### Fix: Zod Inference Instead of Duplicate Types
```typescript
// BEFORE: Duplicate interface
interface CreateCheckoutInput {
  successUrl?: string;
  cancelUrl?: string;
}

// AFTER: Infer from schema
export const createCheckoutSchema = z.object({
  successUrl: z.string().url().optional(),
  cancelUrl: z.string().url().optional(),
});
export type CreateCheckoutInput = z.infer<typeof createCheckoutSchema>;
```

## Error Propagation Fixes

### Fix: Add error.tsx Per Route Segment
```typescript
// src/app/dashboard/error.tsx
"use client";

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center p-8">
      <h2 className="text-xl font-semibold">Something went wrong</h2>
      <p className="mt-2 text-muted-foreground">
        {error.digest ? `Error ID: ${error.digest}` : error.message}
      </p>
      <button onClick={reset} className="mt-4 rounded bg-primary px-4 py-2 text-white">
        Try again
      </button>
    </div>
  );
}
```

### Fix: Wrap External API Errors
```typescript
// BEFORE: Leaks Stripe error
try {
  await stripe.customers.create({ ... });
} catch (error) {
  throw error; // Leaks Stripe internals
}

// AFTER: Wrapped error
try {
  await stripe.customers.create({ ... });
} catch {
  throw new Error("Payment service unavailable");
}
```

### Fix: Non-Fatal Side Effects
```typescript
// BEFORE: GitHub invite failure crashes purchase
await prisma.purchase.create({ data: purchaseData });
await inviteCollaborator(username); // If this throws, purchase fails

// AFTER: Side effect is non-fatal
const purchase = await prisma.purchase.create({ data: purchaseData });
try {
  await inviteCollaborator(username);
} catch {
  // Log but don't fail the purchase
  logAuthEvent("github_invited", userId);
}
```

### Fix: Add not-found.tsx
```typescript
// src/app/dashboard/not-found.tsx
export default function DashboardNotFound() {
  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center">
      <h2 className="text-xl font-semibold">Page not found</h2>
      <p className="mt-2 text-muted-foreground">
        The page you're looking for doesn't exist.
      </p>
    </div>
  );
}
```
