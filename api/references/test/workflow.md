# API Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| Security (20%) | Integration | CORS headers present, XSS prevention, no sensitive data leak |
| Auth & AuthZ (15%) | Integration | 401 without token, 403 wrong role, ownership check |
| Input Validation (12%) | Unit + Integration | Invalid input → 400, missing fields, type coercion |
| Error Handling (10%) | Integration | 500 → proper envelope, no stack trace, request ID |
| Rate Limiting (10%) | Integration | 429 after N requests, reset after window |
| Response Design (8%) | Integration | Correct status codes, pagination, consistent shape |
| Performance (8%) | Performance | Response time < threshold, no N+1 queries |
| Observability (7%) | Unit | Logger called with context, request ID propagated |
| Documentation (5%) | Static analysis | Types exported, JSDoc present |
| Testing (5%) | Meta | Test coverage > 80%, all methods covered |

2. **Generate Test Files** — One test file per route file:
   - `__tests__/api/[route]/route.test.ts`
   - Use `describe` per HTTP method, `it` per test case
   - Mock auth, database, rate limiter

3. **Test Structure Template**:
```typescript
import { POST, GET } from "@/app/api/[resource]/route";
import { NextRequest } from "next/server";

// Mock dependencies
vi.mock("@clerk/nextjs/server", () => ({ auth: vi.fn() }));
vi.mock("@/lib/db", () => ({ prisma: { resource: { findMany: vi.fn(), create: vi.fn() } } }));

describe("POST /api/[resource]", () => {
  it("returns 401 without auth", async () => { /* ... */ });
  it("returns 400 with invalid input", async () => { /* ... */ });
  it("returns 429 when rate limited", async () => { /* ... */ });
  it("returns 201 with valid input", async () => { /* ... */ });
  it("returns proper error envelope on failure", async () => { /* ... */ });
});
```

4. **Output** — Test file(s) + coverage matrix showing which categories are covered
