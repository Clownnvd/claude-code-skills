# Step 2.2: Configure Prisma

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Create `prisma.config.ts`

In Prisma 7, the datasource URL is configured in `prisma.config.ts` (not in `schema.prisma`).

```typescript
// prisma.config.ts (project root)
import "dotenv/config";
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  datasource: {
    url: env("DATABASE_URL"),
  },
});
```

## Update `.env`

```env
DATABASE_URL="postgresql://user:password@host:5432/database?sslmode=require"
```

## Key Points

| Config | Value |
|--------|-------|
| Config file | `prisma.config.ts` (project root) |
| Schema file | `prisma/schema.prisma` |
| Migrations | `prisma/migrations/` |
| URL source | `DATABASE_URL` env var |

> **Important**: In Prisma 7, `datasource` URL must be in `prisma.config.ts`, NOT in `schema.prisma`.

## Next Step

Proceed to [generate-client.md](generate-client.md).
