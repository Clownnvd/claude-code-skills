# Step 4.2: Rate Limiting + Account Lockout

> Source: King Template codebase — Upstash Redis with in-memory fallback

## Dependencies

```bash
npm install @upstash/ratelimit @upstash/redis
```

## Environment Variables

```env
# Optional — falls back to in-memory for development
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
```

## Rate Limiter (`src/lib/rate-limit.ts`)

### Core Pattern

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const redis = process.env.UPSTASH_REDIS_REST_URL && process.env.UPSTASH_REDIS_REST_TOKEN
  ? new Redis({
      url: process.env.UPSTASH_REDIS_REST_URL,
      token: process.env.UPSTASH_REDIS_REST_TOKEN,
    })
  : null;

// In-memory fallback for development (cleaned up via setInterval)
const inMemoryStore = new Map<string, { count: number; resetAt: number }>();
```

### Presets

```typescript
export const rateLimitPresets = {
  strict:   { interval: 60_000, maxRequests: 5 },   // Auth endpoints
  standard: { interval: 60_000, maxRequests: 20 },  // General API
  relaxed:  { interval: 60_000, maxRequests: 60 },  // Read-heavy
  webhook:  { interval: 60_000, maxRequests: 100 },  // Webhook receivers
} as const;
```

### Usage in Route Handlers

```typescript
import { rateLimit, rateLimitPresets, addRateLimitHeaders } from "@/lib/rate-limit";

export async function POST(req: NextRequest) {
  const rateLimitResult = await rateLimit(req, rateLimitPresets.strict, "auth");
  if (rateLimitResult) return rateLimitResult; // 429 response

  const response = await handler(req);
  return addRateLimitHeaders(req, response);
}
```

## Account Lockout (Auth Route)

Tracks consecutive failed login attempts per IP:

```typescript
const MAX_FAILURES = 10;
const WINDOW_MS = 15 * 60 * 1000;   // 15 min window
const LOCKOUT_MS = 30 * 60 * 1000;  // 30 min lockout

// Uses Redis in production, in-memory fallback for dev
async function isLockedOut(ip: string): Promise<boolean> { /* ... */ }
async function recordFailure(ip: string): Promise<void> { /* ... */ }
async function clearFailures(ip: string): Promise<void> { /* ... */ }
```

### Auth Route Integration

```typescript
export async function POST(req: NextRequest) {
  const rateLimitResult = await rateLimit(req, rateLimitPresets.strict, "auth");
  if (rateLimitResult) return rateLimitResult;

  const ip = getClientIP(req);
  if (isSignInPath(req.nextUrl.pathname) && await isLockedOut(ip)) {
    return new Response(
      JSON.stringify({ error: "Account temporarily locked." }),
      { status: 429 }
    );
  }

  const response = await authPost(req);

  // Track failures / clear on success
  if (isSignInPath(req.nextUrl.pathname)) {
    if (response.status !== 200) await recordFailure(ip);
    else await clearFailures(ip);
  }

  return addRateLimitHeaders(req, response);
}
```

## IP Extraction

```typescript
function getClientIP(req: NextRequest): string {
  const forwarded = req.headers.get("x-forwarded-for");
  if (forwarded) {
    const ips = forwarded.split(",").map((ip) => ip.trim());
    return ips[ips.length - 1]; // LAST IP = proxy-set, not spoofable
  }
  return req.headers.get("x-real-ip") ?? "unknown";
}
```

> **Security**: Always use the LAST IP from `X-Forwarded-For` (set by the reverse proxy). The first IP is client-spoofable.

## Quick Reference

| Feature | Details |
|---------|---------|
| Redis | Upstash (optional, falls back to in-memory) |
| Headers | `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` |
| Lockout | 10 failures in 15 min → 30 min lockout |
| IP source | Last `X-Forwarded-For` IP (proxy-set) |
| Presets | strict (5/min), standard (20/min), relaxed (60/min), webhook (100/min) |
