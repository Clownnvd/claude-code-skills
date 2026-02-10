# Fix Patterns: Input Validation + Secrets Management

## Input Validation Fixes

### Add Zod validation to API route

```typescript
// Before: raw input
const body = await req.json();
const { email } = body;

// After: validated input
import { emailSchema } from "@/lib/validations/user";

const body = await req.json();
const parsed = emailSchema.safeParse(body);
if (!parsed.success) {
  return validationError(parsed.error);
}
const { email } = parsed.data;
```

### Centralize schemas

Move inline schemas to `src/lib/validations/`:
```typescript
// src/lib/validations/user.ts
import { z } from "zod";

export const emailSchema = z.object({
  email: z.string().email().max(255),
}).strict();

export type EmailInput = z.infer<typeof emailSchema>;
```

### Add .strict() to existing schemas

```typescript
// Before
z.object({ name: z.string() })

// After
z.object({ name: z.string() }).strict()
```

### Range-check numbers

```typescript
z.object({
  amount: z.number().int().min(1).max(999999),
  page: z.number().int().min(1).max(1000),
})
```

## Secrets Management Fixes

### Move hardcoded value to env

```typescript
// Before
const webhookSecret = "whsec_xxx";

// After
const webhookSecret = env.STRIPE_WEBHOOK_SECRET;
```

### Sync env files

1. Add to `.env.example`:
   ```
   NEW_VAR=your_value_here  # Description
   ```

2. Add to `src/lib/env.ts`:
   ```typescript
   NEW_VAR: z.string().min(1),
   ```

3. Add to `env.d.ts`:
   ```typescript
   NEW_VAR: string;
   ```

### Check NEXT_PUBLIC_ variables

Audit all `NEXT_PUBLIC_` vars — none should contain secrets:
```typescript
// WRONG
NEXT_PUBLIC_STRIPE_SECRET_KEY  // Secret exposed to client!

// RIGHT
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY  // Public key, OK
STRIPE_SECRET_KEY  // Server-only
```

### Fail fast on missing env

```typescript
// In env.ts — Zod validates at import time
const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
});

export const env = envSchema.parse(process.env);
```
