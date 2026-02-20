# Step 2.5: Neon Adapter (Production)

> Source: King Template codebase — production-grade Neon PostgreSQL setup

## Why Neon Instead of Basic pg

| Feature | `@prisma/adapter-pg` | `@prisma/adapter-neon` |
|---------|----------------------|------------------------|
| Connection pooling | Manual | Built-in via pgbouncer |
| Serverless | No | Yes (auto-suspend) |
| Branching | No | Yes (DB branches) |
| Cold start | Slow | Fast (HTTP protocol) |

## Install

```bash
npm install @prisma/adapter-neon
# Remove if present:
npm uninstall @prisma/adapter-pg pg
```

## Dual Connection URLs

Neon requires two URLs: pooled (queries) and direct (migrations).

```env
# Pooled — for app queries (pgbouncer=true)
DATABASE_URL=postgresql://user:pass@ep-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&pgbouncer=true

# Direct — for migrations (no pgbouncer)
DIRECT_URL=postgresql://user:pass@ep-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

## Update `prisma.config.ts`

```typescript
import "dotenv/config";
import { defineConfig } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
    seed: `tsx prisma/seed.ts`,
  },
  datasource: {
    // Migrations use DIRECT_URL (bypasses pgbouncer) — falls back to DATABASE_URL
    url: process.env["DIRECT_URL"] || process.env["DATABASE_URL"],
  },
});
```

## Update `src/lib/db/index.ts`

```typescript
import { PrismaClient } from "@prisma/client";
import { PrismaNeon } from "@prisma/adapter-neon";

// Append statement_timeout (10s) to prevent long-running queries
const dbUrl = new URL(process.env.DATABASE_URL!);
if (!dbUrl.searchParams.has("options")) {
  dbUrl.searchParams.set("options", "-c statement_timeout=10000");
}
const adapter = new PrismaNeon({ connectionString: dbUrl.toString() });

const globalForPrisma = global as unknown as {
  prisma: PrismaClient;
};

const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({ adapter });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export default prisma;
```

## Key Differences from Basic Setup

| Concern | Basic (`adapter-pg`) | Neon (`adapter-neon`) |
|---------|---------------------|----------------------|
| Import | `PrismaPg` | `PrismaNeon` |
| URL | Single `DATABASE_URL` | Dual: pooled + direct |
| Migrations | Uses `DATABASE_URL` | Uses `DIRECT_URL` (no pgbouncer) |
| Timeout | Not included | 10s `statement_timeout` via URL params |
| Protocol | TCP | HTTP (serverless-optimized) |
