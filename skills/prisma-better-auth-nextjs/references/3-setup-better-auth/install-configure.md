# Step 3.1: Install and Configure Better Auth

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Install

```bash
npm install better-auth
```

## Generate Secret

```bash
npx @better-auth/cli@latest secret
```

This adds `BETTER_AUTH_SECRET` to your `.env` file.

## Update `.env`

```env
BETTER_AUTH_SECRET=your-generated-secret
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL="your-database-url"
```

## Create `src/lib/auth.ts`

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import prisma from "@/lib/prisma";

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),
  emailAndPassword: {
    enabled: true,
  },
});
```

## Configuration Summary

| Setting | Value |
|---------|-------|
| Database adapter | `prismaAdapter` (Prisma + PostgreSQL) |
| Auth method | Email + Password |
| Secret | Auto-generated via CLI |
| Base URL | `BETTER_AUTH_URL` env var |

## Next Step

Proceed to [add-auth-models.md](add-auth-models.md).
