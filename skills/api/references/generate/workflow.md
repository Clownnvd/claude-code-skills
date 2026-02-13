# API Generate Workflow

## Process

1. **Parse Request** — Extract: endpoint path, HTTP method(s), business logic, auth requirements
2. **Load Criteria** — Read all 10 api scoring categories from SKILL.md
3. **Map Criteria to Code** — Each category becomes a code section:

| Category | Code Pattern |
|----------|-------------|
| Security (20%) | CORS headers, helmet, CSP, input sanitization |
| Auth & AuthZ (15%) | `auth()` guard, role check, ownership validation |
| Input Validation (12%) | Zod schema + `safeParse`, field-level errors |
| Error Handling (10%) | Try/catch, error envelope `{ success, data, error }` |
| Rate Limiting (10%) | Identifier extraction, Upstash/memory limiter |
| Response Design (8%) | Consistent shape, pagination, status codes |
| Performance (8%) | Select fields, no N+1, connection reuse |
| Observability (7%) | Structured logging, request ID, timing |
| Documentation (5%) | JSDoc on handler, OpenAPI-compatible types |
| Testing (5%) | Testable structure, pure business logic extraction |

4. **Generate** — Write full route handler with ALL patterns integrated
5. **Self-Check** — Verify checklist: all 10 categories addressed, no `any`, no TODO, no placeholders
6. **Output** — Code + compliance checklist + integration notes

## Code Structure Template

```typescript
import { auth } from "@clerk/nextjs/server";
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { ratelimit } from "@/lib/rate-limit";

// 1. Validation Schema (Input Validation)
const requestSchema = z.object({ /* fields */ });

// 2. Response Types (Documentation & DX)
type SuccessResponse = { success: true; data: ResponseData };
type ErrorResponse = { success: false; error: { code: string; message: string } };

export async function POST(request: NextRequest): Promise<NextResponse<SuccessResponse | ErrorResponse>> {
  const requestId = crypto.randomUUID();
  const start = performance.now();

  try {
    // 3. Auth Guard (Auth & AuthZ)
    const { userId } = await auth();
    if (!userId) return NextResponse.json({ success: false, error: { code: "UNAUTHORIZED", message: "Authentication required" } }, { status: 401 });

    // 4. Rate Limiting
    const { success: allowed } = await ratelimit.limit(userId);
    if (!allowed) return NextResponse.json({ success: false, error: { code: "RATE_LIMITED", message: "Too many requests" } }, { status: 429 });

    // 5. Input Validation
    const body = await request.json();
    const parsed = requestSchema.safeParse(body);
    if (!parsed.success) return NextResponse.json({ success: false, error: { code: "VALIDATION_ERROR", message: "Invalid input", details: parsed.error.flatten().fieldErrors } }, { status: 400 });

    // 6. Business Logic (Performance — use select, no N+1)
    const result = await prisma.resource.create({
      data: { ...parsed.data, userId },
      select: { id: true, /* only needed fields */ },
    });

    // 7. Observability
    console.info("[API_NAME]", { requestId, userId, action: "create", duration: performance.now() - start });

    // 8. Response Design
    return NextResponse.json({ success: true, data: result }, {
      status: 201,
      headers: { "Cache-Control": "no-store", "X-Request-Id": requestId },
    });
  } catch (error) {
    console.error("[API_NAME]", { requestId, error: error instanceof Error ? error.message : "Unknown", userId });
    return NextResponse.json({ success: false, error: { code: "INTERNAL_ERROR", message: "An unexpected error occurred" } }, { status: 500 });
  }
}
```

## Quality Contract

- All 10 categories addressed with concrete code
- Score >= 90 (A-) if audited with api scoring
- No `any` types, no TODO stubs, no placeholders
- Copy-paste ready with all imports
