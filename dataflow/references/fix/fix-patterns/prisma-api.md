# Fix Patterns: Prisma Optimization + API Route Design

## Prisma Fixes

### Fix: Add select to Every Query
```typescript
// BEFORE (returns all columns)
const user = await prisma.user.findUnique({ where: { id: userId } });

// AFTER (only needed fields)
const user = await prisma.user.findUnique({
  where: { id: userId },
  select: {
    id: true,
    name: true,
    email: true,
    image: true,
  },
});
```

### Fix: Use findUnique for Unique Fields
```typescript
// BEFORE
const purchase = await prisma.purchase.findFirst({
  where: { stripePaymentId: paymentIntentId },
});

// AFTER (stripePaymentId is @unique)
const purchase = await prisma.purchase.findUnique({
  where: { stripePaymentId: paymentIntentId },
});
```

### Fix: Add Indexes to Schema
```prisma
model Purchase {
  id              String   @id @default(cuid())
  userId          String
  stripePaymentId String?  @unique
  status          String

  @@index([userId, status]) // Composite index for user + status queries
  @@index([paymentCode])    // Lookup by payment code
}
```

### Fix: Singleton PrismaClient
```typescript
// src/lib/db/index.ts
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

const prisma = globalForPrisma.prisma ?? new PrismaClient({ ... });

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}

export default prisma;
```

## API Route Design Fixes

### Fix: Consistent Response Envelope
```typescript
// src/lib/api/response.ts
export function successResponse<T>(
  data: T,
  status = 200,
  headers?: Record<string, string>
): NextResponse<ApiResponse<T>> {
  return NextResponse.json({ success: true, data }, { status, headers });
}

export function errorResponse(
  error: string,
  status = 400,
  errors?: Record<string, string[]>,
  code?: string
): NextResponse<ApiResponse> {
  return NextResponse.json({ success: false, error, code, errors }, { status });
}
```

### Fix: Standard API Route Pipeline
```typescript
export async function POST(req: NextRequest) {
  // 1. CSRF
  const csrfResult = verifyCsrf(req);
  if (csrfResult) return csrfResult;

  // 2. Content-Type
  const ctCheck = requireJsonBody(req);
  if (ctCheck) return ctCheck;

  // 3. Auth
  const session = await auth.api.getSession({ headers: req.headers });
  if (!session?.user) return unauthorizedError();

  // 4. Rate limit
  const rl = await rateLimit(req, rateLimitPresets.strict, "endpoint", session.user.id);
  if (rl) return rl;

  // 5. Validation
  const body = await req.json();
  const result = schema.safeParse(body);
  if (!result.success) return validationError(result.error);

  // 6. Service call
  const data = await service.doThing(result.data);

  // 7. Response
  return successResponse(data, 200, NO_CACHE_HEADERS);
}
```

### Fix: Service Layer Separation
```typescript
// BAD: Prisma in route handler
export async function GET(req: NextRequest) {
  const user = await prisma.user.findUnique({ where: { id } });
  return NextResponse.json(user);
}

// GOOD: Service layer
export async function GET(req: NextRequest) {
  const user = await userService.getProfile(userId);
  return successResponse(user, 200, NO_CACHE_HEADERS);
}
```
