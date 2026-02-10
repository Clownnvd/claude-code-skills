# Fix Patterns: Server Component Architecture + Database Performance

## Server Component Fixes

### Extract Client Interactivity
```tsx
// BEFORE: Entire page is client
'use client';
export default function ProductPage() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <h1>Product</h1>
      <p>Description...</p>
      <button onClick={() => setCount(c => c + 1)}>Add ({count})</button>
    </div>
  );
}

// AFTER: Page is server, only button is client
// add-to-cart-button.tsx
'use client';
export function AddToCartButton() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>Add ({count})</button>;
}

// page.tsx (Server Component - no 'use client')
import { AddToCartButton } from './add-to-cart-button';
export default function ProductPage() {
  return (
    <div>
      <h1>Product</h1>
      <p>Description...</p>
      <AddToCartButton />
    </div>
  );
}
```

### Add Suspense Boundaries
```tsx
// BEFORE: Blocking render
export default async function Page() {
  const data = await slowQuery(); // blocks entire page
  return <div>{data.title}</div>;
}

// AFTER: Streaming with Suspense
import { Suspense } from 'react';
export default function Page() {
  return (
    <Suspense fallback={<Skeleton />}>
      <SlowContent />
    </Suspense>
  );
}
async function SlowContent() {
  const data = await slowQuery();
  return <div>{data.title}</div>;
}
```

### Add Error Boundaries
```tsx
// Create src/app/dashboard/error.tsx
'use client';
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

---

## Database Performance Fixes

### Add Select to Queries
```typescript
// BEFORE: Fetches all columns
const user = await prisma.user.findUnique({ where: { id } });

// AFTER: Fetches only needed columns
const user = await prisma.user.findUnique({
  where: { id },
  select: { id: true, name: true, email: true },
});
```

### Add Database Indexes
```prisma
// BEFORE: No index on query field
model Purchase {
  id     String @id @default(cuid())
  userId String
  status PurchaseStatus
}

// AFTER: Index on frequently queried fields
model Purchase {
  id     String @id @default(cuid())
  userId String
  status PurchaseStatus

  @@index([userId])
  @@index([status])
}
```

### Use findUnique for Unique Fields
```typescript
// BEFORE: findFirst for unique lookup
const user = await prisma.user.findFirst({ where: { email } });

// AFTER: findUnique (uses unique index, more efficient)
const user = await prisma.user.findUnique({ where: { email } });
```

### Batch Independent Queries
```typescript
// BEFORE: Sequential
const user = await prisma.user.findUnique({ where: { id } });
const purchases = await prisma.purchase.findMany({ where: { userId: id } });
const stats = await prisma.stats.findFirst();

// AFTER: Parallel
const [user, purchases, stats] = await Promise.all([
  prisma.user.findUnique({ where: { id } }),
  prisma.purchase.findMany({ where: { userId: id } }),
  prisma.stats.findFirst(),
]);
```
