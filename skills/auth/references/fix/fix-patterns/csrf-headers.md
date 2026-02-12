# Fix Patterns: CSRF & Origin Validation + Security Headers

## CSRF Fixes

### Fix: Origin Validation in Proxy
```typescript
// src/proxy.ts — add to auth route handling
function validateOrigin(request: NextRequest): boolean {
  const origin = request.headers.get("origin");
  const referer = request.headers.get("referer");

  // Safe methods don't need origin check
  if (["GET", "HEAD", "OPTIONS"].includes(request.method)) {
    return true;
  }

  const allowedOrigin = process.env.BETTER_AUTH_URL
    ?? process.env.NEXT_PUBLIC_APP_URL;
  if (!allowedOrigin) return false;

  const allowedHost = new URL(allowedOrigin).host;

  if (origin) {
    return new URL(origin).host === allowedHost;
  }
  if (referer) {
    return new URL(referer).host === allowedHost;
  }

  // Both missing on POST = reject
  return false;
}
```

### Fix: CSRF Header Check (API Routes)
```typescript
// src/lib/csrf.ts
export function validateCsrf(request: Request): boolean {
  if (["GET", "HEAD", "OPTIONS"].includes(request.method)) {
    return true;
  }
  // Check Origin header matches allowed host
  // Check Referer as fallback
  // Reject if both missing on state-changing requests
}
```

### Fix: SameSite Cookie
Better Auth config:
```typescript
advanced: {
  defaultCookieSameSite: "lax",
  // "lax" allows OAuth redirects
  // "strict" would block OAuth callback cookies
},
```

## Security Headers Fixes

### Fix: Comprehensive Security Headers
```typescript
// src/proxy.ts — apply to ALL routes
function applySecurityHeaders(response: NextResponse): NextResponse {
  const headers = response.headers;

  // Prevent MIME sniffing
  headers.set("X-Content-Type-Options", "nosniff");
  // Prevent clickjacking
  headers.set("X-Frame-Options", "DENY");
  // XSS protection (legacy browsers)
  headers.set("X-XSS-Protection", "1; mode=block");
  // Referrer policy
  headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  // Permissions policy
  headers.set("Permissions-Policy",
    "camera=(), microphone=(), geolocation=(), payment=()");
  // HSTS (production only)
  if (process.env.NODE_ENV === "production") {
    headers.set("Strict-Transport-Security",
      "max-age=31536000; includeSubDomains; preload");
  }

  return response;
}
```

### Fix: Content Security Policy
```typescript
// CSP must allow Tailwind inline styles + external images
headers.set("Content-Security-Policy", [
  "default-src 'self'",
  "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data: https:",
  "font-src 'self'",
  "connect-src 'self' https:",
  "frame-ancestors 'none'",
].join("; "));
```
**Note**: `unsafe-inline` needed for Tailwind. Use nonces for stricter CSP.

### Fix: Apply Headers to ALL Routes
```typescript
// In proxy.ts matcher config:
export const config = {
  matcher: [
    // Match all routes except static files
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
};
```
Security headers MUST apply to landing, auth, dashboard, AND API routes.

### Fix: Remove Server Header
```typescript
// next.config.ts
const nextConfig = {
  poweredByHeader: false, // Remove X-Powered-By: Next.js
};
```
