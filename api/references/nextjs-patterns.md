# Next.js App Router API Patterns

Framework-specific scoring adjustments for Next.js 16+ App Router.

## Route Handler Conventions

### File Structure
```
src/app/api/
  health/route.ts          # Health check
  auth/[...all]/route.ts   # Auth catch-all
  stripe/checkout/route.ts # Stripe checkout
  webhooks/stripe/route.ts # Stripe webhook
  user/purchase/route.ts   # User purchase
```

### Export Patterns
```typescript
// GOOD: Named exports for HTTP methods
export async function GET(req: NextRequest) { ... }
export async function POST(req: NextRequest) { ... }

// GOOD: Runtime + caching hints
export const runtime = "nodejs";       // or "edge"
export const dynamic = "force-dynamic"; // no caching for auth endpoints
```

## Auth Patterns

### Two-Layer Auth (expected in enterprise)
```
Layer 1: Proxy (Node) — fast cookie check for redirects
Layer 2: API Route (Node) — full session + DB verification
```

Score +1 if both layers present; -1 if only one layer.

### Auth Helper Pattern
```typescript
// GOOD: Centralized auth helper
const session = await requireAuth(); // throws 401 if invalid

// BAD: Inline auth in every route
const session = await auth.api.getSession({ headers: req.headers });
if (!session) return new Response("Unauthorized", { status: 401 });
```

## Proxy Patterns

### Security Headers (apply to ALL routes)
```typescript
const securityHeaders = {
  "X-Frame-Options": "DENY",
  "X-Content-Type-Options": "nosniff",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
  "Content-Security-Policy": "default-src 'self'; ...",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=()",
};
```

## Webhook Patterns

### Signature + Idempotency
```typescript
// Verify → check idempotency → process → mark processed
const event = stripe.webhooks.constructEvent(body, signature, secret);
if (await isEventProcessed(event.id)) return ok();
await processEvent(event);
await markEventProcessed(event.id, event.type);
```

### Non-Fatal Side Effects
```typescript
// GitHub invite = non-fatal (user can retry via dashboard)
try { await inviteCollaborator(username); } catch { /* log only */ }
```

## Response Helpers (expected pattern)

```typescript
// Centralized in src/lib/api/response.ts
export function successResponse<T>(data: T) { ... }
export function errorResponse(message: string, status = 400) { ... }
export function validationError(zodError: ZodError) { ... }
export function unauthorizedError() { ... }
export function serverError() { ... }
```

Score +1 if centralized; -1 if inline NextResponse.json everywhere.

## Env Validation (expected pattern)

```typescript
// Zod validation at startup — crash early
const ServerEnvSchema = z.object({
  DATABASE_URL: z.string().min(1),
  STRIPE_SECRET_KEY: z.string().regex(/^sk_/),
});
```

Score +1 for Zod env; -1 for raw `process.env.X!`.

## Common Anti-Patterns (scoring penalties)

| Anti-Pattern | Penalty |
|-------------|---------|
| `console.log` in API routes | -1 Observability |
| No `select` on DB queries | -1 Performance, -1 Security |
| Missing CSRF on POST/PATCH/DELETE | -1 Security |
| Auth proxy only (no DB check) | -1 Auth |
| Hardcoded URLs/emails | -1 DX |
| Secrets without env validation | -1 Security |
| Empty catch blocks | -1 Observability |
