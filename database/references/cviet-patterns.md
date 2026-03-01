# CViet Project Specifics

> Current setup, schema summary, known issues, upgrade path, package.json scripts, CI/CD build command.
> Sources: CViet project experience.
> Date: 2026-02-27

---

## Current Setup (Prisma 6 on Next.js 16.1.6)

The CViet project currently uses:
- `@prisma/client@^6.0.0` with `prisma@^6.0.0`
- Traditional `provider = "prisma-client-js"` (no driver adapter)
- Connection URL in `datasource db { url = env("DATABASE_URL") }`
- Singleton pattern in `src/lib/db.ts`
- No `prisma.config.ts` file
- No `DIRECT_URL` configured (uses single connection string)

## Schema Summary

```
User (id, email, name, image, emailVerified, polarCustomerId, plan, aiUsageThisMonth, aiUsageResetAt)
  -> Session (id, userId, token, expiresAt, ipAddress, userAgent)
  -> Account (id, userId, accountId, providerId, accessToken, refreshToken, ...)
  -> CV (id, userId, title, template, language, data:Json)
Verification (id, identifier, value, expiresAt)
Plan enum (FREE, PRO)
```

## Known Issues & Workarounds

| Issue | Current Workaround |
|-------|-------------------|
| `Prisma.JsonValue` not castable to CVData | `cv.data as unknown as CVData` double-cast |
| Build fails without DB connection | `DATABASE_URL="postgresql://fake:fake@localhost/fake" pnpm build` |
| Edge/Serverless TCP failure | proxy.ts uses Node.js runtime (not edge) |
| Client not generated on deploy | `prisma generate` in postinstall script |
| Better Auth + `use cache` | Extract cookies outside cache scope |
| Prisma version pinning | `@prisma/client` and `prisma` must match exact versions |

## Upgrade Path: Prisma 6 -> 7

When ready to upgrade CViet to Prisma 7:

```bash
# 1. Update packages
pnpm add @prisma/client@7 @prisma/adapter-neon
pnpm add -D prisma@7

# 2. Update schema.prisma
# Change: provider = "prisma-client-js"  ->  provider = "prisma-client"
# Add:    output = "../src/generated/prisma"

# 3. Create prisma.config.ts (see prisma7-features.md)

# 4. Update src/lib/db.ts (see Prisma 7 + Neon pattern in prisma7-features.md)

# 5. Update all imports
# Change: from "@prisma/client"  ->  from "../generated/prisma" (or "@/generated/prisma")

# 6. Update Better Auth import
# In src/lib/auth.ts: import { PrismaClient } from "../generated/prisma"

# 7. Regenerate client
npx prisma generate

# 8. Add dotenv to prisma.config.ts (env vars no longer auto-loaded)

# 9. Test build
DATABASE_URL="postgresql://..." pnpm build
```

## Package.json Scripts

```json
{
  "scripts": {
    "dev": "cross-env NODE_ENV=development next dev --webpack",
    "build": "next build --webpack",
    "start": "next start",
    "lint": "eslint",
    "db:push": "prisma db push",
    "db:studio": "prisma studio",
    "db:generate": "prisma generate",
    "db:migrate": "prisma migrate dev",
    "db:deploy": "prisma migrate deploy",
    "db:seed": "prisma db seed",
    "postinstall": "prisma generate && node scripts/postinstall.js"
  }
}
```

## Build Command (CI/CD with Fake DB)

```bash
BETTER_AUTH_SECRET="2vLtX7+4SyiGL3w46Z12LRKZA29ZdvxHliaEx9JH+lI=" \
DATABASE_URL="postgresql://fake:fake@localhost/fake" \
NEXT_PUBLIC_APP_URL="http://localhost:3000" \
pnpm build
```
