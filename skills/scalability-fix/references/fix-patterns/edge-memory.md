# Fix Patterns: Edge & CDN Optimization + Memory & Resource Management

## Edge & CDN Fixes

### Static Generation for Public Pages
```typescript
// BEFORE: Dynamic rendering (SSR every request)
export const dynamic = 'force-dynamic';
export default function AboutPage() { ... }

// AFTER: Static generation (built once)
// Remove force-dynamic, page auto-detects as static
export default function AboutPage() { ... }
```

### Add ISR for Semi-Static Content
```typescript
// Page with data that changes infrequently
export const revalidate = 3600; // Revalidate every hour

export default async function BlogPage() {
  const posts = await getPosts();
  return <PostList posts={posts} />;
}
```

### Optimize Middleware Matcher
```typescript
// BEFORE: Runs on every request
export function middleware(request: NextRequest) { ... }

// AFTER: Specific matcher excluding static assets
export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|images/|robots.txt|sitemap.xml).*)',
  ],
};
```

### Lightweight Middleware
```typescript
// BEFORE: DB query in middleware
export async function middleware(request: NextRequest) {
  const user = await prisma.user.findUnique({ where: { id: session.userId } }); // BAD
}

// AFTER: Edge-compatible check only
export async function middleware(request: NextRequest) {
  const session = request.cookies.get('session');
  if (!session) return NextResponse.redirect(new URL('/login', request.url));
  return NextResponse.next();
}
```

---

## Memory & Resource Management Fixes

### Prisma Singleton Pattern
```typescript
// src/lib/db/index.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

### Bounded In-Memory Cache
```typescript
// BEFORE: Unbounded Map
const cache = new Map<string, Data>();

// AFTER: Bounded with eviction
class BoundedCache<K, V> {
  private cache = new Map<K, { value: V; expiry: number }>();
  constructor(private maxSize: number, private ttlMs: number) {}

  get(key: K): V | undefined {
    const entry = this.cache.get(key);
    if (!entry || Date.now() > entry.expiry) {
      this.cache.delete(key);
      return undefined;
    }
    return entry.value;
  }

  set(key: K, value: V): void {
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      if (firstKey !== undefined) this.cache.delete(firstKey);
    }
    this.cache.set(key, { value, expiry: Date.now() + this.ttlMs });
  }
}
```

### Event Listener Cleanup
```typescript
// BEFORE: No cleanup
useEffect(() => {
  window.addEventListener('resize', handleResize);
}, []);

// AFTER: Cleanup on unmount
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

### AbortController for External Calls
```typescript
// Wrap external API calls with timeout
async function fetchExternal(url: string, timeoutMs = 5000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { signal: controller.signal });
    return await res.json();
  } finally {
    clearTimeout(timeout);
  }
}
```
