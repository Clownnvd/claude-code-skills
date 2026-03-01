# Better Auth Integration

> Required schema models, auth configuration, Prisma 7 import changes, CLI generation, session retrieval, proxy.ts integration.
> Sources: Better Auth docs, Prisma docs, CViet project experience.
> Date: 2026-02-27

---

## Required Schema Models

Better Auth requires these four models with specific field names:

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

  // Custom fields (extend as needed)
  plan             Plan     @default(FREE)
  polarCustomerId  String?  @unique
  aiUsageThisMonth Int      @default(0)
  aiUsageResetAt   DateTime @default(now())
  cvs              CV[]
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

## Auth Configuration

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth"
import { prismaAdapter } from "better-auth/adapters/prisma"
import { db } from "@/lib/db"

export const auth = betterAuth({
  database: prismaAdapter(db, {
    provider: "postgresql",
  }),
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  trustedOrigins: [process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"],
  // Enable joins for 2-3x session lookup performance
  // experimental: { joins: true },
})

export type Session = typeof auth.$Infer.Session
```

## Prisma 7 Import Change for Better Auth

When upgrading to Prisma 7 with custom output path:
```typescript
// BEFORE (Prisma 6)
import { PrismaClient } from "@prisma/client"

// AFTER (Prisma 7)
import { PrismaClient } from "../generated/prisma"  // or wherever output points
```

## Schema Generation with CLI

```bash
# Generate Better Auth schema additions
pnpm dlx @better-auth/cli@latest generate

# This adds User, Session, Account, Verification models
# Then push to database:
npx prisma db push
```

## Session Retrieval in Server Components

```typescript
// src/lib/auth-client.ts
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
})
```

```typescript
// Server Component or Server Action
import { auth } from "@/lib/auth"
import { headers } from "next/headers"

export async function getSession() {
  const session = await auth.api.getSession({
    headers: await headers(),
  })
  return session
}
```

## Next.js 16 Proxy + Better Auth

```typescript
// src/proxy.ts (NOT middleware.ts in Next.js 16)
import { auth } from "@/lib/auth"

export function proxy(request: Request) {
  // Check session cookie for protected routes
  const sessionCookie = request.headers.get("cookie")
  const url = new URL(request.url)

  if (url.pathname.startsWith("/app") || url.pathname.startsWith("/dashboard")) {
    if (!sessionCookie?.includes("better-auth.session_token")) {
      return Response.redirect(new URL("/login", request.url))
    }
  }
}
```
