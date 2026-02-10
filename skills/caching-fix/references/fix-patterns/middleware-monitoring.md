# Fix Patterns: Middleware Caching + Monitoring

## Middleware Fixes

### Fix: Add Matcher to Skip Static Assets
```typescript
// BEFORE: Middleware runs on every request
export default async function middleware(req: NextRequest) {
  // ... runs on _next/static, images, etc.
}

// AFTER: Matcher skips static assets
export const config = {
  matcher: [
    // Skip static files, images, favicon, API routes that handle own auth
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
```

### Fix: Lightweight Auth Check in Middleware
```typescript
// BEFORE: Full DB session lookup in middleware
const session = await prisma.session.findUnique({ where: { token } });

// AFTER: Cookie-based check only (no DB)
export default async function middleware(req: NextRequest) {
  const sessionCookie = req.cookies.get("better-auth.session_token");
  const isAuthenticated = !!sessionCookie?.value;

  // Protect dashboard routes
  if (req.nextUrl.pathname.startsWith("/dashboard") && !isAuthenticated) {
    return NextResponse.redirect(new URL("/sign-in", req.url));
  }

  return NextResponse.next();
}
```

### Fix: Early Return for Public Routes
```typescript
export default async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  // Public routes — skip all checks
  if (
    pathname === "/" ||
    pathname.startsWith("/sign-") ||
    pathname.startsWith("/api/webhooks")
  ) {
    return NextResponse.next();
  }

  // Protected routes — check auth
  // ...
}
```

## Cache Monitoring Fixes

### Fix: Log Revalidation Events
```typescript
import { revalidatePath } from "next/cache";

// Wrapper with logging
function revalidateWithLog(path: string, context: string) {
  if (process.env.NODE_ENV === "development") {
    console.info(`[cache:revalidate] ${path} (trigger: ${context})`);
  }
  revalidatePath(path);
}

// Usage:
revalidateWithLog("/dashboard", "stripe-webhook:purchase-created");
```

### Fix: Review Build Output for Route Classification
```bash
# After build, check output:
pnpm build

# Expected:
# Route (app)                    Size     First Load JS
# ┌ ○ /                          1.2 kB   85 kB       <- STATIC
# ├ λ /api/stripe/checkout       0 B      0 B         <- DYNAMIC
# ├ λ /api/user/purchase         0 B      0 B         <- DYNAMIC
# ├ λ /dashboard                 2.1 kB   90 kB       <- DYNAMIC
# └ ○ /sign-in                   1.8 kB   88 kB       <- STATIC

# ○ = Static, λ = Dynamic
# If landing page shows λ instead of ○, investigate what's making it dynamic
```

### Fix: Add Cache Debug Header (Dev Only)
```typescript
// In middleware or API route:
if (process.env.NODE_ENV === "development") {
  const response = NextResponse.next();
  response.headers.set("x-cache-debug", "miss");
  return response;
}
```
