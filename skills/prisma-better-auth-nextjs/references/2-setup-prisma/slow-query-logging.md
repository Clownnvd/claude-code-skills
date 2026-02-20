# Step 2.6: Slow Query Logging

> Source: King Template codebase — production-grade query monitoring

## Overview

Detect and log slow queries with structured output. JSON in production, readable in development.

## Implementation

Add to your Prisma client (`src/lib/db/index.ts`):

```typescript
const SLOW_QUERY_THRESHOLD_MS = 1000;

const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    adapter,
    log: [
      { emit: "event", level: "query" },
      { emit: "stdout", level: "warn" },
      { emit: "stdout", level: "error" },
    ],
  });

// Structured slow query detection
// @ts-expect-error -- Prisma event typing varies by adapter; runtime works correctly
prisma.$on("query", (e: { duration: number; query: string }) => {
  if (e.duration > SLOW_QUERY_THRESHOLD_MS) {
    const sanitized = e.query.replace(/\$\d+/g, "?");
    if (process.env.NODE_ENV === "production") {
      console.warn(
        JSON.stringify({
          level: "warn",
          event: "slow_query",
          durationMs: e.duration,
          threshold: SLOW_QUERY_THRESHOLD_MS,
          timestamp: new Date().toISOString(),
        })
      );
    } else {
      console.warn(
        `[SLOW QUERY] ${e.duration}ms: ${sanitized.slice(0, 200)}`
      );
    }
  }
});
```

## Key Patterns

| Pattern | Details |
|---------|---------|
| Threshold | 1000ms (configurable) |
| Sanitization | Replace `$1`, `$2` params with `?` (no PII in logs) |
| Production | Structured JSON for log aggregation (Datadog, etc.) |
| Development | Readable `[SLOW QUERY] 1234ms: SELECT ...` format |
| Truncation | `.slice(0, 200)` prevents log flooding from large queries |

## Statement Timeout

Prevent queries from running forever by appending timeout to the connection URL:

```typescript
const dbUrl = new URL(process.env.DATABASE_URL!);
if (!dbUrl.searchParams.has("options")) {
  dbUrl.searchParams.set("options", "-c statement_timeout=10000"); // 10 seconds
}
```

This is set at the PostgreSQL level — any query exceeding 10s is killed automatically.
