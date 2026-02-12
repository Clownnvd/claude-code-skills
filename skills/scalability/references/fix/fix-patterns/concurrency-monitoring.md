# Fix Patterns: Concurrency & Parallel Processing + Performance Monitoring

## Concurrency Fixes

### Promise.all for Independent Fetches
```typescript
// BEFORE: Sequential (waterfall)
const user = await getUser(id);
const prefs = await getPreferences(id);
const history = await getHistory(id);

// AFTER: Parallel
const [user, prefs, history] = await Promise.all([
  getUser(id),
  getPreferences(id),
  getHistory(id),
]);
```

### Promise.allSettled for Partial OK
```typescript
// BEFORE: One failure breaks everything
const [a, b, c] = await Promise.all([fetchA(), fetchB(), fetchC()]);

// AFTER: Partial failure acceptable
const results = await Promise.allSettled([fetchA(), fetchB(), fetchC()]);
const successful = results
  .filter((r): r is PromiseFulfilledResult<Data> => r.status === 'fulfilled')
  .map(r => r.value);
```

### Non-Blocking Side Effects
```typescript
// BEFORE: Blocks response on email
export async function POST(req: NextRequest) {
  const purchase = await createPurchase(data);
  await sendEmail(purchase.userId); // blocks response
  return NextResponse.json(purchase);
}

// AFTER: Fire-and-forget for non-critical
export async function POST(req: NextRequest) {
  const purchase = await createPurchase(data);
  // Non-critical: don't await
  sendEmail(purchase.userId).catch(err =>
    logger.warn('email_send_failed', { error: err.message })
  );
  return NextResponse.json(purchase);
}
```

### Parallel Page Data Fetching
```tsx
// BEFORE: Sequential in layout
export default async function Layout({ children }) {
  const user = await getUser();
  const nav = await getNavItems(); // waits for user first
  return <Shell user={user} nav={nav}>{children}</Shell>;
}

// AFTER: Parallel
export default async function Layout({ children }) {
  const [user, nav] = await Promise.all([getUser(), getNavItems()]);
  return <Shell user={user} nav={nav}>{children}</Shell>;
}
```

---

## Performance Monitoring Fixes

### Structured API Logging
```typescript
// Already exists in src/lib/api/logger.ts — ensure it's used in all routes
import { logRequest } from '@/lib/api/logger';

export async function GET(req: NextRequest) {
  const start = Date.now();
  try {
    const data = await getData();
    logRequest(req, 200, start);
    return NextResponse.json(data);
  } catch (error) {
    logRequest(req, 500, start);
    throw error;
  }
}
```

### Health Check Endpoint
```typescript
// src/app/api/health/route.ts
export async function GET() {
  return NextResponse.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
}
```

### Web Vitals Reporting
```typescript
// src/app/layout.tsx or a client component
'use client';
import { useReportWebVitals } from 'next/web-vitals';

export function WebVitals() {
  useReportWebVitals((metric) => {
    // Send to analytics
    console.log(metric); // Replace with analytics call
  });
  return null;
}
```

### Bundle Size Budget
```javascript
// next.config.js
module.exports = {
  experimental: {
    // Track output file sizes
    outputFileTracingExcludes: {
      '*': ['node_modules/@swc/core*', 'node_modules/esbuild*'],
    },
  },
};
```
