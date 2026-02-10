# Fix Patterns: Monitoring + Supply Chain

## Security Monitoring Fixes

### Create structured logger

```typescript
// src/lib/api/logger.ts
type LogLevel = "info" | "warn" | "error";

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

  if (process.env.NODE_ENV === "production") {
    // JSON for production log aggregators
    process[level === "error" ? "stderr" : "stdout"].write(
      JSON.stringify(entry) + "\n"
    );
  } else {
    console[level](message, meta);
  }
}

export const logger = {
  info: (msg: string, meta?: Record<string, unknown>) => log("info", msg, meta),
  warn: (msg: string, meta?: Record<string, unknown>) => log("warn", msg, meta),
  error: (msg: string, meta?: Record<string, unknown>) => log("error", msg, meta),
};
```

### Log security events

```typescript
// Rate limit hit
logger.warn("Rate limit exceeded", { ip, path, limit });

// Failed auth attempt
logger.warn("Authentication failed", { email: "***", ip, reason });

// Webhook processed
logger.info("Webhook processed", { eventType, eventId, result: "success" });

// Invalid input
logger.warn("Validation failed", { route: "/api/xxx", errors: parsed.error.issues });
```

### Add request IDs

```typescript
// In middleware
const requestId = crypto.randomUUID();
response.headers.set("X-Request-Id", requestId);

// In API routes — extract from headers
const requestId = req.headers.get("x-request-id") ?? crypto.randomUUID();
logger.info("Processing request", { requestId, route });
```

### No PII in logs

```typescript
// Before
logger.info("User registered", { email: user.email, name: user.name });

// After
logger.info("User registered", { userId: user.id });
```

## Supply Chain Fixes

### Disable poweredByHeader

```javascript
// next.config.js
const nextConfig = {
  poweredByHeader: false,
  // ...
};
```

### Disable production source maps

```javascript
// next.config.js
const nextConfig = {
  productionBrowserSourceMaps: false,
  // ...
};
```

### Verify no eval() usage

```bash
# Search for eval in codebase
grep -r "eval(" src/ --include="*.ts" --include="*.tsx"
grep -r "new Function(" src/ --include="*.ts" --include="*.tsx"
```

### Ensure lockfile is committed

```bash
git ls-files pnpm-lock.yaml  # Should exist
```

### Check server-only imports

```typescript
// Ensure server-only modules aren't imported in client components
// Add "server-only" package for runtime protection
import "server-only";  // Add to server-only modules
```
