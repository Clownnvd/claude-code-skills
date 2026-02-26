# Fix Patterns: CSP + Data Protection

## CSP Fixes

### Add CSP to proxy

```typescript
// src/proxy.ts
const cspDirectives = [
  "default-src 'self'",
  "script-src 'self'",
  "style-src 'self' 'unsafe-inline'",  // Tailwind needs inline
  "img-src 'self' data: https:",
  "font-src 'self'",
  "connect-src 'self' https://api.stripe.com",
  "frame-ancestors 'none'",
  "base-uri 'self'",
  "form-action 'self'",
].join("; ");

response.headers.set("Content-Security-Policy", cspDirectives);
```

### Add missing security headers

```typescript
response.headers.set("X-Content-Type-Options", "nosniff");
response.headers.set("X-Frame-Options", "DENY");
response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
response.headers.set("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
```

### Add HSTS (production only)

```typescript
if (process.env.NODE_ENV === "production") {
  response.headers.set(
    "Strict-Transport-Security",
    "max-age=31536000; includeSubDomains"
  );
}
```

### Adjust CSP for specific needs

```typescript
// If using external images (avatars, etc.)
"img-src 'self' data: https://avatars.githubusercontent.com https://lh3.googleusercontent.com"

// If using external scripts (analytics)
"script-src 'self' https://js.stripe.com"

// If embedding iframes
"frame-src 'self' https://js.stripe.com"
```

## Data Protection Fixes

### Use Prisma select

```typescript
// Before: returns ALL fields including password hash
const user = await prisma.user.findUnique({ where: { id } });

// After: only needed fields
const user = await prisma.user.findUnique({
  where: { id },
  select: {
    id: true,
    name: true,
    email: true,
    image: true,
  },
});
```

### Strip internal IDs from responses

```typescript
// Before: database PK exposed
return successResponse({ id: user.id, stripeId: user.stripeCustomerId });

// After: only public-facing data
return successResponse({ name: user.name, email: user.email });
```

### Sanitize user objects

```typescript
function sanitizeUser(user: User) {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    image: user.image,
  };
  // Explicitly OMIT: passwordHash, stripeCustomerId, etc.
}
```

### Don't log PII

```typescript
// Before
logger.info("User login", { user });  // Logs entire user object

// After
logger.info("User login", { userId: user.id });  // Only ID
```

### Force-dynamic on private pages

```typescript
// Pages showing user data must not be statically cached
export const dynamic = "force-dynamic";
```
