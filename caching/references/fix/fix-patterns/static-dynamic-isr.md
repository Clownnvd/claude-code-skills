# Fix Patterns: Static/Dynamic Classification + ISR

## Static/Dynamic Fixes

### Fix: Move Header Auth to Client-Side
```typescript
// BEFORE: Server component reading session (makes page dynamic)
// landing-header.tsx
import { auth } from "@/lib/auth";
export async function LandingHeader() {
  const session = await auth.api.getSession({ headers: await headers() });
  return <LandingHeaderClient isAuthed={!!session} />;
}

// AFTER: Client component checks session (page stays static)
// landing-header.tsx
export function LandingHeader() {
  return <LandingHeaderClient />;
}

// landing-header-client.tsx
"use client";
import { useSession } from "@/lib/auth-client";
export function LandingHeaderClient() {
  const { data: session } = useSession();
  const isAuthed = !!session?.user;
  // ...
}
```

### Fix: Remove force-dynamic from Static Pages
```typescript
// BEFORE: Unnecessary force-dynamic on landing page
export const dynamic = "force-dynamic";

// AFTER: Remove it — landing page is static
// (no export const dynamic needed for static pages)
```

### Fix: Add force-dynamic to API Routes Explicitly
```typescript
// API routes MUST be explicit about dynamic:
export const runtime = "nodejs";
export const dynamic = "force-dynamic";
```

### Fix: Verify Build Output
```bash
# After changes, check build output:
pnpm build

# Look for:
# ○ (Static)  /                    <- landing page should be static
# λ (Dynamic) /api/stripe/checkout <- API routes should be dynamic
# λ (Dynamic) /dashboard           <- auth pages should be dynamic
```

## ISR Fixes

### Fix: Add ISR to Semi-Static Page
```typescript
// For pages with content that changes infrequently:
export const revalidate = 3600; // Revalidate every hour

export default async function BlogPage() {
  const posts = await getPosts(); // Cached for 1 hour
  return <PostList posts={posts} />;
}
```

### Fix: On-Demand ISR via Webhook
```typescript
// In webhook handler:
import { revalidatePath } from "next/cache";

// After content update:
revalidatePath("/blog");
```

### N/A: When ISR Doesn't Apply
For pure dashboard apps with no public content pages:
- Landing page is fully static (no ISR needed)
- Dashboard pages are dynamic (auth-dependent)
- API routes are dynamic
- Score ISR based on correct classification, not ISR usage
