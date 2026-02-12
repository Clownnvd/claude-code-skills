# Fix Patterns: Input Validation + Error Handling

Covers api-scoring categories 3 (Input Validation, 12%) and 4 (Error Handling, 10%).

## Content-Type Enforcement

### Problem: JSON parsing without Content-Type check
```typescript
const body = await req.json(); // parses anything, no type check
```

### Fix: Reject non-JSON requests
```typescript
export function requireJsonBody(req: NextRequest): NextResponse | null {
  const contentType = req.headers.get("content-type");
  if (!contentType?.includes("application/json")) {
    return errorResponse("Content-Type must be application/json", 415);
  }
  return null;
}

// Usage in route handler:
const ctCheck = requireJsonBody(req);
if (ctCheck) return ctCheck;
const body = await req.json();
```

## Machine-Readable Error Codes

### Problem: Only human-readable messages, no stable codes
```typescript
return errorResponse("Validation failed", 400);
// Client can't programmatically distinguish error types
```

### Fix: Add error code to envelope
```typescript
// Update response.ts
export function errorResponse(
  error: string,
  status = 400,
  errors?: Record<string, string[]>,
  code?: string
): NextResponse<ApiResponse> {
  return NextResponse.json(
    { success: false, error, code, errors },
    { status }
  );
}

// Define error codes
export const ErrorCodes = {
  VALIDATION_ERROR: "VALIDATION_ERROR",
  UNAUTHORIZED: "UNAUTHORIZED",
  FORBIDDEN: "FORBIDDEN",
  NOT_FOUND: "NOT_FOUND",
  CONFLICT: "CONFLICT",
  RATE_LIMITED: "RATE_LIMITED",
  SERVER_ERROR: "SERVER_ERROR",
} as const;

// Usage:
return errorResponse("Validation failed", 400, errors, ErrorCodes.VALIDATION_ERROR);
```

## Consistent Response Helpers Everywhere

### Problem: Some routes use inline NextResponse.json
```typescript
// send/route.ts — inline instead of centralized helpers
return NextResponse.json({ success: false, error: "..." }, { status: 401 });
```

### Fix: Replace with centralized helpers
```typescript
// Before:
return NextResponse.json({ success: false, error: "Authentication required" }, { status: 401 });
// After:
return unauthorizedError("Authentication required");

// Before:
return NextResponse.json({ success: true, data });
// After:
return successResponse(data);
```

Audit all API routes: `grep -r "NextResponse.json" src/app/api/` — every hit should use helpers instead.

## Webhook Response Consistency

### Problem: Webhooks use different format from API routes
```typescript
// Stripe webhook: { received: true }
// SePay webhook: { success: false }
// API routes: { success: true, data: {...} }
```

### Fix: Standardize or document webhook exceptions
Option A: Standardize webhooks too:
```typescript
return successResponse({ received: true }); // envelope wrapper
```
Option B: Document that webhooks intentionally use minimal format (Stripe expects simple responses). Add comment:
```typescript
// Webhook responses use minimal format per Stripe/SePay requirements
return NextResponse.json({ received: true });
```

## Validation Schema for Webhook Bodies

### Problem: Manual type checking instead of schema validation
```typescript
// Before: manual runtime type check
if (typeof obj.id !== "number") return false;
```

### Fix: Use Zod for webhook validation too
```typescript
const sepayTransactionSchema = z.object({
  id: z.number(),
  transferType: z.string(),
  transferAmount: z.number(),
  content: z.string(),
  referenceCode: z.string(),
  // ...optional fields
});
```
