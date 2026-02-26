# Fix Patterns: Environment Management + Monitoring

## Environment Management Fixes

### Env Validation with Zod

```typescript
// src/lib/env.ts
import { z } from "zod";

const serverSchema = z.object({
  DATABASE_URL: z.string().url(),
  STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith("whsec_"),
  RESEND_API_KEY: z.string().optional(),
  GITHUB_TOKEN: z.string().startsWith("ghp_").optional(),
  BETTER_AUTH_SECRET: z.string().min(32),
  BETTER_AUTH_URL: z.string().url(),
});

const clientSchema = z.object({
  NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: z.string().startsWith("pk_"),
  NEXT_PUBLIC_APP_URL: z.string().url(),
});

// Validate at import time (startup)
export const serverEnv = serverSchema.parse(process.env);
export const clientEnv = clientSchema.parse({
  NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY:
    process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY,
  NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
});
```

### .env.example Sync

Keep `.env.example` in sync with `env.ts`:
```bash
# Database
DATABASE_URL="postgresql://user:pass@host:5432/db"

# Auth
BETTER_AUTH_SECRET="at-least-32-characters-long-secret-here"
BETTER_AUTH_URL="http://localhost:3000"

# Stripe
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_test_..."

# Optional
RESEND_API_KEY="re_..."
GITHUB_TOKEN="ghp_..."
```

### Env Sync Verification Script

```typescript
// scripts/verify-env.ts
// Compare .env.example keys against env.ts schema
// Run in CI to catch drift
```

### .gitignore for Secrets

```
.env
.env.local
.env.*.local
!.env.example
```

---

## Monitoring & Observability Fixes

### Structured Logger

```typescript
// src/lib/api/logger.ts
type LogLevel = "info" | "warn" | "error" | "debug";

interface LogEntry {
  level: LogLevel;
  message: string;
  timestamp: string;
  [key: string]: unknown;
}

function log(level: LogLevel, message: string, meta?: Record<string, unknown>) {
  const entry: LogEntry = {
    level,
    message,
    timestamp: new Date().toISOString(),
    ...meta,
  };

  if (level === "error") {
    console.error(JSON.stringify(entry));
  } else {
    console.log(JSON.stringify(entry));
  }
}

export const logger = {
  info: (msg: string, meta?: Record<string, unknown>) => log("info", msg, meta),
  warn: (msg: string, meta?: Record<string, unknown>) => log("warn", msg, meta),
  error: (msg: string, meta?: Record<string, unknown>) => log("error", msg, meta),
  debug: (msg: string, meta?: Record<string, unknown>) => log("debug", msg, meta),
};
```

### Health Endpoint

```typescript
// src/app/api/health/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || "unknown",
    uptime: process.uptime(),
  });
}
```

### Readiness Endpoint

```typescript
// src/app/api/ready/route.ts
import { NextResponse } from "next/server";
import { prisma } from "@/lib/db";

export async function GET() {
  const checks: Record<string, string> = {};

  // Check database
  try {
    await prisma.$queryRaw`SELECT 1`;
    checks.database = "ok";
  } catch {
    checks.database = "error";
  }

  const allHealthy = Object.values(checks).every((v) => v === "ok");

  return NextResponse.json(
    { status: allHealthy ? "ready" : "degraded", checks },
    { status: allHealthy ? 200 : 503 }
  );
}
```

### Request Logging in API Routes

```typescript
// Pattern for API route handlers
import { logger } from "@/lib/api/logger";

export async function POST(request: Request) {
  const startMs = Date.now();
  try {
    // ... handle request
    logger.info("request completed", {
      method: "POST",
      path: "/api/example",
      status: 200,
      durationMs: Date.now() - startMs,
    });
    return NextResponse.json({ success: true });
  } catch (error) {
    logger.error("request failed", {
      method: "POST",
      path: "/api/example",
      status: 500,
      durationMs: Date.now() - startMs,
      error: error instanceof Error ? error.message : "Unknown error",
    });
    return NextResponse.json({ error: "Internal error" }, { status: 500 });
  }
}
```
