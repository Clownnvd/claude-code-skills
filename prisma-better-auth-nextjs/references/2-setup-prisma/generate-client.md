# Step 2.3: Generate the Prisma Client

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Generate

```bash
npx prisma generate
```

This reads `prisma/schema.prisma` and outputs the typed client to `src/generated/prisma/` (as configured during `prisma init --output`).

## What Gets Generated

| Output | Location |
|--------|----------|
| Prisma Client | `src/generated/prisma/client` |
| Type definitions | `src/generated/prisma/` |

## Import Path

After generation, import with:

```typescript
import { PrismaClient } from "@/generated/prisma/client";
```

## When to Re-generate

Run `npx prisma generate` after:
- Changing `schema.prisma` models
- Running `npx prisma migrate dev`
- Pulling schema with `npx prisma db pull`

## Next Step

Proceed to [global-client.md](global-client.md).
