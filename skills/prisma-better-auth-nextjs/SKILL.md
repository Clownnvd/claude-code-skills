---
name: prisma-better-auth-nextjs
description: "Step-by-step setup: Prisma 7 + Better Auth + Next.js App Router. Email/password auth with PostgreSQL. Triggers on auth setup, Prisma+BetterAuth integration."
license: Complete terms in LICENSE.txt
---

# Prisma + Better Auth + Next.js Setup Guide

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Prerequisites

- Node.js 20+
- Next.js App Router + TypeScript
- PostgreSQL database (e.g., Neon, Supabase, local)

## Steps Overview

| Step | Folder | Files | What |
|------|--------|-------|------|
| 1 | `1-setup-project/` | [create-nextjs-app](references/1-setup-project/create-nextjs-app.md) | Create Next.js project |
| 2.1 | `2-setup-prisma/` | [install-dependencies](references/2-setup-prisma/install-dependencies.md) | Install Prisma + pg |
| 2.2 | | [configure-prisma](references/2-setup-prisma/configure-prisma.md) | `prisma.config.ts` |
| 2.3 | | [generate-client](references/2-setup-prisma/generate-client.md) | Generate typed client |
| 2.4 | | [global-client](references/2-setup-prisma/global-client.md) | Singleton `src/lib/prisma.ts` |
| 3.1 | `3-setup-better-auth/` | [install-configure](references/3-setup-better-auth/install-configure.md) | Install + `src/lib/auth.ts` |
| 3.2 | | [add-auth-models](references/3-setup-better-auth/add-auth-models.md) | User, Session, Account models |
| 3.3 | | [migrate-database](references/3-setup-better-auth/migrate-database.md) | Run migration |
| 4 | `4-api-routes/` | [setup-routes](references/4-api-routes/setup-routes.md) | Catch-all + auth client |
| 5.1 | `5-pages/` | [sign-up](references/5-pages/sign-up.md) | Sign up form |
| 5.2 | | [sign-in](references/5-pages/sign-in.md) | Sign in form |
| 5.3 | | [dashboard](references/5-pages/dashboard.md) | Protected dashboard |
| 5.4 | | [home](references/5-pages/home.md) | Landing page |
| 6 | `6-test/` | [test-app](references/6-test/test-app.md) | Test + troubleshoot |

## Key Files Created

| File | Purpose |
|------|---------|
| `prisma.config.ts` | Datasource URL (Prisma 7 pattern) |
| `prisma/schema.prisma` | Database models |
| `src/lib/prisma.ts` | Global Prisma Client singleton |
| `src/lib/auth.ts` | Better Auth server config |
| `src/lib/auth-client.ts` | Better Auth React client (hooks) |
| `src/app/api/auth/[...all]/route.ts` | Auth API catch-all |

## Quick Commands

```bash
# Install
npm install prisma tsx @types/pg --save-dev
npm install @prisma/client @prisma/adapter-pg dotenv pg better-auth

# Prisma
npx prisma init --db --output ../src/generated/prisma
npx prisma generate
npx prisma migrate dev --name add-auth-models
npx prisma studio

# Better Auth
npx @better-auth/cli@latest secret
npx @better-auth/cli generate
```

## Environment Variables

```env
DATABASE_URL="postgresql://user:password@host:5432/db?sslmode=require"
BETTER_AUTH_SECRET=generated-secret
BETTER_AUTH_URL=http://localhost:3000
```

## Key Patterns

- **Prisma 7**: Datasource URL in `prisma.config.ts`, NOT in `schema.prisma`
- **Global client**: Singleton on `globalThis` to prevent hot-reload duplicates
- **PrismaPg adapter**: Direct PostgreSQL driver (not Prisma's default engine)
- **Catch-all route**: `[...all]/route.ts` handles all Better Auth endpoints
- **Auth client**: `createAuthClient()` exports `signIn`, `signUp`, `signOut`, `useSession`
- **Auth guard**: `useEffect` + `useSession` to redirect unauthenticated users
