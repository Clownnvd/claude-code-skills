# Middleware Guard — Protect Paid Routes

## Next.js Middleware (Edge)

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Routes that require an active subscription
const PAID_ROUTES = ["/dashboard", "/app", "/settings"];

// Routes that require authentication only (free tier OK)
const AUTH_ROUTES = ["/account", "/billing"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check if route needs protection
  const isPaidRoute = PAID_ROUTES.some((r) => pathname.startsWith(r));
  const isAuthRoute = AUTH_ROUTES.some((r) => pathname.startsWith(r));

  if (!isPaidRoute && !isAuthRoute) return NextResponse.next();

  // TODO: Replace with your auth check (read session cookie/token)
  // Example with NextAuth:
  // const token = await getToken({ req: request });
  // if (!token) return redirect("/login");
  const hasSession = request.cookies.has("session"); // Replace
  if (!hasSession) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // For paid routes, check subscription status
  // NOTE: Middleware runs at the Edge — no direct DB access.
  // Options: (1) encode plan in JWT, (2) use edge-compatible DB, (3) API call
  if (isPaidRoute) {
    // Option 1: Read plan from JWT claims
    // const plan = token.plan;
    // if (plan === "free") return redirect("/pricing");

    // Option 2: Read from cookie set by webhook handler
    const plan = request.cookies.get("plan")?.value;
    if (!plan || plan === "free") {
      return NextResponse.redirect(new URL("/pricing", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/app/:path*", "/settings/:path*", "/account/:path*", "/billing/:path*"],
};
```

## Server Component Guard (Alternative)

For more reliable checks with direct DB access:

```typescript
// lib/guards.ts
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth"; // Your auth
import { hasActiveSubscription } from "@/lib/subscription";

export async function requireAuth() {
  const session = await auth();
  if (!session?.user) redirect("/login");
  return session.user;
}

export async function requireSubscription() {
  const user = await requireAuth();
  const active = await hasActiveSubscription(user.id);
  if (!active) redirect("/pricing");
  return user;
}
```

```typescript
// app/dashboard/page.tsx
import { requireSubscription } from "@/lib/guards";

export default async function DashboardPage() {
  const user = await requireSubscription(); // Redirects if no subscription

  return <div>Welcome, {user.name}</div>;
}
```

## Layout-Level Guard

Protect all routes under a layout:

```typescript
// app/(paid)/layout.tsx
import { requireSubscription } from "@/lib/guards";

export default async function PaidLayout({ children }: { children: React.ReactNode }) {
  await requireSubscription();
  return <>{children}</>;
}
```

All pages under `app/(paid)/` are automatically gated.

## Set Plan Cookie from Webhook

```typescript
// In webhook handler — set plan cookie for middleware checks
import { cookies } from "next/headers";

async function handleSubscriptionChange(subscription: Stripe.Subscription) {
  // Update DB first (see database-sync.md)
  // ...

  // Note: cookies() only works in Server Actions / Route Handlers,
  // not in webhook handlers. For webhook → cookie, use an API:
  // Store plan in DB, read in middleware via edge-compatible query,
  // or encode plan in JWT at login time.
}
```

## Approach Comparison

| Approach | Pros | Cons |
|----------|------|------|
| Middleware + JWT claims | Fast, runs on Edge | Plan changes need JWT refresh |
| Middleware + cookie | Simple | Cookie can be stale |
| Server Component guard | Accurate, DB access | Per-page, not layout-level |
| Layout guard | Protects entire section | Slightly slower (DB call per request) |

## Key Points
- Middleware runs at Edge — no direct DB/ORM access
- Encode plan in JWT or cookie for middleware checks
- Use Server Component guards for authoritative checks
- Layout guards protect all child routes automatically
- Always check server-side — never trust client-only checks
- Update plan claim/cookie when subscription changes (webhook → DB → next login)
