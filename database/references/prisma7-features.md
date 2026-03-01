# Prisma 7 New Features & Breaking Changes

> Sources: Prisma docs, GitHub issues, community blogs, CViet project experience.
> Date: 2026-02-27

---

## Architecture Overhaul

Prisma 7 removes the Rust-based query engine entirely, replacing it with a pure TypeScript implementation.

| Metric | Prisma 6 | Prisma 7 | Improvement |
|--------|----------|----------|-------------|
| Bundle size | ~15 MB (Rust binary) | ~1.5 MB | 90% smaller |
| Query execution | Baseline | 3x faster | Eliminates JS<->Rust IPC |
| Type checking | Baseline | ~70% faster | 98% fewer types to evaluate |
| CPU/Memory | Higher | Lower | No binary process overhead |
| Edge Runtime | Problematic | Native | No binary dependency |

## Breaking Changes Summary

| # | Change | Prisma 6 | Prisma 7 | Impact |
|---|--------|----------|----------|--------|
| 1 | Generator provider | `prisma-client-js` | `prisma-client` | CRITICAL -- client won't generate |
| 2 | Output path required | Optional (defaults to node_modules) | Required in schema | CRITICAL -- build fails |
| 3 | Driver adapters required | Optional | Mandatory for all DBs | CRITICAL -- client won't connect |
| 4 | prisma.config.ts | Did not exist | Required for CLI commands | HIGH -- migrations fail |
| 5 | Import paths | `from "@prisma/client"` | `from "./generated/prisma"` | HIGH -- all imports break |
| 6 | Client middleware ($use) | Supported | Removed | HIGH -- use $extends |
| 7 | Env vars in schema | `url = env("DATABASE_URL")` | Move to prisma.config.ts | HIGH -- CLI commands fail |
| 8 | ESM module support | CJS default | ESM preferred | MEDIUM |
| 9 | SSL validation | Skipped by default | Validates by default | MEDIUM -- connection errors |
| 10 | Connection pooling | Prisma internal pool | Driver adapter pool | MEDIUM -- timeout behavior changes |
| 11 | Auto env loading | .env auto-loaded | Must use dotenv manually | MEDIUM |
| 12 | Seeding | Auto on migrate dev | Must run `prisma db seed` explicitly | LOW |
| 13 | Minimum Node.js | 18.x | 20.19.0+ (rec 22.x) | LOW |
| 14 | Minimum TypeScript | 4.7+ | 5.4.0+ (rec 5.9.x) | LOW |
| 15 | MongoDB | Supported | NOT supported in v7 | BLOCKING for Mongo users |

## Prisma 7 Generator Config (schema.prisma)

```prisma
// BEFORE (Prisma 6)
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}

// AFTER (Prisma 7)
generator client {
  provider = "prisma-client"
  output   = "../src/generated/prisma"
}

datasource db {
  provider = "postgresql"
  // URL moved to prisma.config.ts
}
```

## prisma.config.ts (New in Prisma 7)

```typescript
import "dotenv/config"
import { defineConfig, env } from "prisma/config"

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
    seed: "tsx prisma/seed.ts",
  },
  datasource: {
    url: env("DATABASE_URL"),
    // shadowDatabaseUrl: env("SHADOW_DATABASE_URL"), // optional
  },
})
```

**Config file reference:**
```typescript
type PrismaConfig = {
  schema?: string               // Default: ./prisma/schema.prisma
  migrations?: {
    path: string                // Migration files directory
    seed: string                // Seed command (e.g. "tsx prisma/seed.ts")
    initShadowDb: string        // SQL to run on shadow DB before migrations
  }
  views?: { path: string }      // SQL view definitions directory
  typedSql?: { path: string }   // Typed SQL files directory
  datasource: {
    url: string                 // Database connection URL (REQUIRED)
    shadowDatabaseUrl?: string  // Shadow DB for migrations
  }
  experimental?: {
    externalTables: boolean     // External table management
  }
}
```

File naming: `prisma.config.ts`, `prisma.config.mjs`, `prisma.config.cjs`, or `.config/prisma.ts`.

## Prisma 7 Client Initialization (with Driver Adapter)

```typescript
// src/lib/db.ts — Prisma 7 pattern
import { PrismaClient } from "../generated/prisma"
import { PrismaPg } from "@prisma/adapter-pg"

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL!,
})

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const db =
  globalForPrisma.prisma ?? new PrismaClient({ adapter })

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = db
```

## Prisma 7 Client with Neon Adapter

```typescript
// src/lib/db.ts — Prisma 7 + Neon
import { PrismaClient } from "../generated/prisma"
import { PrismaNeon } from "@prisma/adapter-neon"

const adapter = new PrismaNeon({
  connectionString: process.env.DATABASE_URL!,
})

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const db =
  globalForPrisma.prisma ?? new PrismaClient({ adapter })

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = db
```

## New Features in Prisma 7.x

| Version | Feature | Description |
|---------|---------|-------------|
| 7.0.0 | Rust-free architecture | Pure TypeScript query engine |
| 7.0.0 | Mapped enums | `@map` attribute for enum members |
| 7.0.0 | Driver adapters default | Required for all databases |
| 7.1.0 | SQL Comments | Append metadata to SQL queries for observability |
| 7.2.0 | --url flag return | Restored for CLI convenience |
| 7.2.0 | Smarter prisma init | Better defaults for Node/Bun |
| 7.3.0 | compilerBuild option | `fast` vs `small` query compiler modes |

## Removed CLI Flags in Prisma 7

| Removed Flag | Command | Replacement |
|-------------|---------|-------------|
| `--skip-generate` | `migrate dev`, `db push` | None -- generate always runs |
| `--skip-seed` | `migrate dev` | Run seed separately |
| `--schema` | `db execute` | Configure in prisma.config.ts |
| `--url` | `db execute` | Configure in prisma.config.ts |
| `--from-url` | `migrate diff` | `--from-config-datasource` |
| `--to-url` | `migrate diff` | `--to-config-datasource` |

## Removed Environment Variables in Prisma 7

- `PRISMA_CLI_QUERY_ENGINE_TYPE`
- `PRISMA_CLIENT_ENGINE_TYPE`
- `PRISMA_QUERY_ENGINE_BINARY`
- `PRISMA_GENERATE_SKIP_AUTOINSTALL`
- `PRISMA_MIGRATE_SKIP_GENERATE`
- `PRISMA_MIGRATE_SKIP_SEED`
