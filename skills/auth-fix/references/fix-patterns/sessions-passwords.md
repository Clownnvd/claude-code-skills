# Fix Patterns: Session Management + Password Security

## Session Management Fixes

### Fix: Cookie Security Flags
```typescript
// In auth.ts betterAuth() config
session: {
  cookieCache: {
    enabled: true,
    maxAge: 5 * 60, // 5 min cache
  },
},
advanced: {
  cookiePrefix: "king",
  useSecureCookies: process.env.NODE_ENV === "production",
  defaultCookieSameSite: "lax", // NOT "strict" (breaks OAuth)
},
```

### Fix: Session Expiry
```typescript
session: {
  expiresIn: 60 * 60 * 24 * 7, // 7 days (seconds)
  updateAge: 60 * 60 * 24,      // refresh daily
},
```
**Warning**: Changing expiry logs out users with existing sessions.

### Fix: Idle Timeout (Custom)
Better Auth doesn't have native idle timeout. Implement via `databaseHooks`:
```typescript
databaseHooks: {
  session: {
    create: {
      after: async (session) => {
        // Store lastActivity timestamp
      },
    },
  },
},
```

### Fix: Session Invalidation on Password Change
```typescript
// In password change handler, after successful change:
// Better Auth handles this if using built-in changePassword
// Verify: after password change, all other sessions are revoked
```

### Fix: Concurrent Session Limit
Better Auth `session` plugin option:
```typescript
session: {
  // No native concurrent limit — implement via databaseHooks
  // On session.create.after: count active sessions, revoke oldest
},
```

## Password Security Fixes

### Fix: Strong Password Schema (Single Source)
```typescript
// src/lib/validations/auth.ts
import { z } from "zod";

export const strongPasswordSchema = z
  .string()
  .min(8, "Password must be at least 8 characters")
  .max(128, "Password must be at most 128 characters")
  .regex(/[a-z]/, "Must contain a lowercase letter")
  .regex(/[A-Z]/, "Must contain an uppercase letter")
  .regex(/[0-9]/, "Must contain a number")
  .regex(/[^a-zA-Z0-9]/, "Must contain a special character");
```
Use this SAME schema for: sign-up, password change, password reset.

### Fix: Better Auth Password Config
```typescript
emailAndPassword: {
  enabled: true,
  minPasswordLength: 8,
  maxPasswordLength: 128,
  autoSignIn: true,
},
```

### Fix: Password Breach Check (Enhancement)
```typescript
// Optional: Check HaveIBeenPwned API
// Add as custom validator in sign-up route, NOT in Better Auth config
// This is a MEDIUM priority enhancement, not critical
```

### Fix: Consistent Validation
Verify the SAME `strongPasswordSchema` is used in:
1. `src/components/auth/sign-up-form.tsx` (client)
2. `src/app/api/auth/[...all]/route.ts` (server via Better Auth)
3. Any password change/reset forms
