# Step 2.4: Set Up a Global Prisma Client

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Create `src/lib/prisma.ts`

A global singleton prevents multiple Prisma Client instances during hot reload in development.

```typescript
// src/lib/prisma.ts
import { PrismaClient } from "@/generated/prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL!,
});

const globalForPrisma = global as unknown as {
  prisma: PrismaClient;
};

const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    adapter,
  });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export default prisma;
```

## How It Works

| Concern | Solution |
|---------|----------|
| Hot reload duplicates | Store instance on `globalThis` |
| PostgreSQL driver | `PrismaPg` adapter with connection string |
| Production safety | Only cache on global in non-production |

## Usage

```typescript
import prisma from "@/lib/prisma";

const users = await prisma.user.findMany();
```

## Next Step

Proceed to [3-setup-better-auth/install-configure.md](../3-setup-better-auth/install-configure.md).
