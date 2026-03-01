# Better Auth -- Setup & Compatibility

> Sections 1-2 from the comprehensive reference.
> Tested with: better-auth ^1.2.7 | Next.js 16.1.6 | Prisma ^6.0.0 | React 19

---

## 1. Compatibility Matrix

### Better Auth Versions + Next.js 16

| Better Auth Version | Next.js 16 | Prisma 7 | React 19 | Notes |
|---------------------|-----------|----------|----------|-------|
| ^1.2.7 | WORKS | WORKS | WORKS | CViet production version |
| ^1.4.0 | WORKS | WORKS | WORKS | Adds experimental joins for Prisma |
| 1.4.4+ | CAUTION | WORKS | WORKS | state_mismatch regressions reported with social providers |
| ^1.5.x | WORKS | WORKS | WORKS | Latest stable; fixes state_mismatch |

### Package Dependencies

```json
{
  "better-auth": "^1.2.7",
  "next": "16.1.6",
  "react": "19.2.3",
  "@prisma/client": "^6.0.0"
}
```

### Import Map

| Context | Import |
|---------|--------|
| Server config | `import { betterAuth } from "better-auth"` |
| Prisma adapter | `import { prismaAdapter } from "better-auth/adapters/prisma"` |
| Next.js handler | `import { toNextJsHandler } from "better-auth/next-js"` |
| React client | `import { createAuthClient } from "better-auth/react"` |
| Server-only client | `import { createAuthClient } from "better-auth/client"` |
| Cookie helpers | `import { getSessionCookie } from "better-auth/cookies"` |
| Cookie cache | `import { getCookieCache } from "better-auth/cookies"` |
| nextCookies plugin | `import { nextCookies } from "better-auth/next-js"` |
| API errors | `import { APIError } from "better-auth/api"` |

---

## 2. Setup Guide

### 2.1 Environment Variables

```env
# REQUIRED - at least 32 characters
BETTER_AUTH_SECRET=<openssl rand -base64 32>

# REQUIRED - your app URL (used for OAuth callbacks, CSRF)
BETTER_AUTH_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql://user:pass@host/db

# OAuth (optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# App URL (for client-side)
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 2.2 Server Configuration (`src/lib/auth.ts`)

```typescript
import { betterAuth } from "better-auth"
import { prismaAdapter } from "better-auth/adapters/prisma"
import { db } from "@/lib/db"

export const auth = betterAuth({
  database: prismaAdapter(db, {
    provider: "postgresql",
  }),
  emailAndPassword: {
    enabled: true,
    // minPasswordLength: 8,         // default
    // maxPasswordLength: 128,        // default
    // autoSignIn: true,              // sign in after signup (default)
    // requireEmailVerification: false // default
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  trustedOrigins: [process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"],
  // session: {
  //   expiresIn: 60 * 60 * 24 * 7,  // 7 days (default)
  //   updateAge: 60 * 60 * 24,       // refresh daily (default)
  //   cookieCache: {
  //     enabled: true,
  //     maxAge: 5 * 60,              // 5 minutes
  //     strategy: "compact",         // "compact" | "jwt" | "jwe"
  //   },
  // },
  // rateLimit: {
  //   window: 60,
  //   max: 100,
  // },
})

export type Session = typeof auth.$Infer.Session
```

### 2.3 Client Configuration (`src/lib/auth-client.ts`)

```typescript
"use client"

import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
})

// Destructure for convenience
export const { signIn, signUp, signOut, useSession, getSession } = authClient
```

**CRITICAL**: Use `"better-auth/react"` for client components, NOT `"better-auth/client"`.
The `"better-auth/client"` import is for server-side-only usage (middleware, server actions).

### 2.4 API Route Handler (`src/app/api/auth/[...all]/route.ts`)

```typescript
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { GET, POST } = toNextJsHandler(auth)
```

**Path must be `/api/auth/[...all]`** -- this is the default Better Auth expects. Changing it requires updating `basePath` in auth config.

### 2.5 Prisma Adapter Setup

#### Schema Requirements

Better Auth requires these 4 models with exact field names:

```prisma
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String?
  image         String?
  emailVerified Boolean   @default(false)
  sessions      Session[]
  accounts      Account[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model Session {
  id        String   @id @default(cuid())
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  token     String   @unique
  expiresAt DateTime
  ipAddress String?
  userAgent String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Account {
  id                    String    @id @default(cuid())
  userId                String
  user                  User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  accountId             String
  providerId            String
  accessToken           String?
  refreshToken          String?
  idToken               String?
  accessTokenExpiresAt  DateTime?
  refreshTokenExpiresAt DateTime?
  scope                 String?
  password              String?
  createdAt             DateTime  @default(now())
  updatedAt             DateTime  @updatedAt

  @@unique([providerId, accountId])
}

model Verification {
  id         String   @id @default(cuid())
  identifier String
  value      String
  expiresAt  DateTime
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt

  @@unique([identifier, value])
}
```

#### Prisma 7 Notes

- Prisma 7 requires the `output` field in `generator client`. If using custom output (e.g., `output = "../src/generated/prisma"`), import PrismaClient from that path instead of `@prisma/client`.
- Default `@prisma/client` works fine when no custom output is specified.

#### Schema Generation via CLI

```bash
# Generate Prisma schema from Better Auth config
npx @better-auth/cli@latest generate

# Apply schema to database
pnpm db:push
```

#### Experimental Joins (v1.4.0+)

Enable for 2-3x performance improvement on session lookups:

```typescript
export const auth = betterAuth({
  database: prismaAdapter(db, { provider: "postgresql" }),
  experimental: { joins: true },
})
```

Requires `@relation` directives in your Prisma schema (included in the schema above).

### 2.6 Database Client Singleton (`src/lib/db.ts`)

```typescript
import { PrismaClient } from "@prisma/client"

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const db =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["query", "error", "warn"] : ["error"],
  })

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = db
```
