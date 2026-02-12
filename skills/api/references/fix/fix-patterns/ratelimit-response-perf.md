# Fix Patterns: Rate Limiting + Response Design + Performance

Covers api-scoring categories 5 (Rate Limiting, 10%), 6 (Response Design, 8%), 7 (Performance, 8%).

## Per-User Rate Limiting

### Problem: All rate limiting is per-IP only
```typescript
const key = `${identifier}:${ip}`; // Only IP-based
```

### Fix: Use userId when authenticated
```typescript
export async function rateLimit(
  req: NextRequest,
  config: RateLimitConfig,
  identifier: string = "default",
  userId?: string  // NEW parameter
): Promise<NextResponse | null> {
  const ip = getClientIP(req);
  const key = userId
    ? `${identifier}:user:${userId}`
    : `${identifier}:ip:${ip}`;
  // ...rest stays the same
}

// Usage in authenticated routes:
const rateLimitResult = await rateLimit(req, rateLimitPresets.standard, "purchase-get", userId);
```

## Rate Limit Headers on Success Responses

### Problem: Rate limit headers only on 429 responses

### Fix: Return headers on all responses
```typescript
// After successful rate limit check, attach headers to final response
export function withRateLimitHeaders(
  response: NextResponse,
  limit: number,
  remaining: number,
  reset: number
): NextResponse {
  response.headers.set("X-RateLimit-Limit", String(limit));
  response.headers.set("X-RateLimit-Remaining", String(remaining));
  response.headers.set("X-RateLimit-Reset", String(reset));
  return response;
}
```

## DB Query Timeouts

### Problem: No explicit timeout on database queries

### Fix: Add statement timeout to Prisma
```typescript
// Option 1: Connection string parameter (Neon supports this)
// DATABASE_URL=...&statement_timeout=10000  (10 seconds)

// Option 2: Per-query timeout via Prisma extension
const prisma = new PrismaClient().$extends({
  query: {
    $allModels: {
      async $allOperations({ args, query }) {
        return Promise.race([
          query(args),
          new Promise((_, reject) =>
            setTimeout(() => reject(new Error("Query timeout")), 10000)
          ),
        ]);
      },
    },
  },
});
```

## Response Compression

### Problem: No explicit compression configuration

### Fix: Next.js enables gzip by default. Verify in next.config:
```typescript
// next.config.ts — compression is ON by default
// Only add if explicitly disabled:
const nextConfig = {
  compress: true, // default, ensures gzip/brotli
};
```

Verify with: `curl -sI -H "Accept-Encoding: gzip" http://localhost:3000/api/health | grep content-encoding`

## Pagination Pattern

### Problem: No pagination established for collection endpoints

### Fix: Add pagination helpers
```typescript
// src/lib/api/pagination.ts
import { z } from "zod";

export const paginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

export function paginate(page: number, limit: number) {
  return { skip: (page - 1) * limit, take: limit };
}

export function paginationMeta(total: number, page: number, limit: number) {
  return { total, page, limit, totalPages: Math.ceil(total / limit) };
}
```

## Caching Headers

### Problem: No Cache-Control on read endpoints

### Fix: Add caching hints where appropriate
```typescript
// Static content (product config): cache short
return successResponse(data, 200, {
  "Cache-Control": "public, max-age=60, s-maxage=300",
});

// User-specific data: never cache
return successResponse(data, 200, {
  "Cache-Control": "private, no-store",
});
```
