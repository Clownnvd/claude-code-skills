# Fix Patterns: Observability + Documentation + Testing

Covers api-scoring categories 8 (Observability, 7%), 9 (Documentation, 5%), 10 (Testing, 5%).

## Request-Level Structured Logging

### Problem: Only slow DB queries are logged, no per-request logging

### Fix: Add request logging middleware or helper
```typescript
// src/lib/api/logger.ts
export function logRequest(req: NextRequest, status: number, startMs: number) {
  const duration = Date.now() - startMs;
  const entry = {
    level: status >= 500 ? "error" : status >= 400 ? "warn" : "info",
    event: "api_request",
    method: req.method,
    path: req.nextUrl.pathname,
    status,
    durationMs: duration,
    ip: req.headers.get("x-forwarded-for")?.split(",").pop()?.trim(),
    userAgent: req.headers.get("user-agent")?.slice(0, 100),
    timestamp: new Date().toISOString(),
  };

  if (process.env.NODE_ENV === "production") {
    console.info(JSON.stringify(entry));
  } else {
    console.info(`[${entry.method}] ${entry.path} ${entry.status} ${entry.durationMs}ms`);
  }
}
```

### Usage pattern in route handlers:
```typescript
export async function GET(req: NextRequest) {
  const start = Date.now();
  try {
    // ... handler logic
    const response = successResponse(data);
    logRequest(req, 200, start);
    return response;
  } catch {
    logRequest(req, 500, start);
    return serverError();
  }
}
```

## Request/Correlation ID

### Problem: No way to trace a request across logs

### Fix: Generate X-Request-Id in proxy
```typescript
// In proxy.ts
import { randomUUID } from "crypto";

const requestId = req.headers.get("x-request-id") || randomUUID();
response.headers.set("X-Request-Id", requestId);
```

Then include `requestId` in all log entries.

## API Documentation

### Problem: No endpoint documentation

### Fix: Add API docs section to README
Create a table listing every endpoint with method, path, auth requirement, rate limit, and description. Include error response format and example requests. See `observability-docs-testing` criteria in api-scoring for required elements.

## Integration Tests for API Routes

### Problem: No route handler tests, only service layer

### Fix: Test each endpoint with auth, validation, and error scenarios
```typescript
// src/app/api/user/purchase/__tests__/route.test.ts
import { describe, it, expect, vi } from "vitest";

describe("GET /api/user/purchase", () => {
  it("returns 401 when not authenticated", async () => {
    // Mock auth to return null session
    vi.mocked(auth.api.getSession).mockResolvedValue(null);
    const req = new NextRequest("http://localhost/api/user/purchase");
    const response = await GET(req);
    expect(response.status).toBe(401);
  });

  it("returns purchase data for authenticated user", async () => {
    vi.mocked(auth.api.getSession).mockResolvedValue(mockSession);
    vi.mocked(prisma.purchase.findFirst).mockResolvedValue(mockPurchase);
    const req = new NextRequest("http://localhost/api/user/purchase");
    const response = await GET(req);
    const data = await response.json();
    expect(data.success).toBe(true);
    expect(data.data.purchased).toBe(true);
  });
});
```

### Test Coverage Targets
| Test Type | Minimum | Target |
|-----------|---------|--------|
| Auth (401/403) | Every protected endpoint | 100% |
| Validation (400) | Every POST/PATCH body | 100% |
| Happy path (200) | Every endpoint | 100% |
| Rate limit (429) | At least 1 endpoint | Sample |
| Error (500) | Service failures | Key paths |

## Validation Edge Case Tests

### Problem: Only happy path tested for validation

### Fix: Test boundary values and injection payloads
```typescript
describe("GitHub username validation", () => {
  it.each([
    ["", "too short"],
    ["a".repeat(40), "too long"],
    ["-invalid", "starts with hyphen"],
    ["invalid--name", "consecutive hyphens"],
    ["<script>alert(1)</script>", "XSS attempt"],
  ])("rejects invalid username: %s (%s)", async (username) => {
    const result = githubUsernameSchema.safeParse(username);
    expect(result.success).toBe(false);
  });
});
```
