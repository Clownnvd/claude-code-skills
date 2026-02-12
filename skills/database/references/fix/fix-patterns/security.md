# Fix Patterns: Security

## Env Var Validation

### Problem: Missing DATABASE_URL validation
```typescript
// Before: only DATABASE_URL validated, DIRECT_URL missing
const ServerEnvSchema = z.object({
  DATABASE_URL: z.string().min(1),
  // DIRECT_URL not validated!
})
```

### Fix: Add all DB-related env vars
```typescript
const ServerEnvSchema = z.object({
  DATABASE_URL: z
    .string()
    .min(1, "DATABASE_URL is required")
    .refine(
      (url) => url.includes("sslmode=require"),
      "DATABASE_URL must include ?sslmode=require"
    ),
  DIRECT_URL: z
    .string()
    .min(1, "DIRECT_URL is required for migrations")
    .optional(),
})
```

### Also update .env.example
```env
# Pooled connection (for queries) — must include ?sslmode=require&pgbouncer=true
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/db?sslmode=require&pgbouncer=true
# Direct connection (for migrations) — must include ?sslmode=require
DIRECT_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/db?sslmode=require
```

## SSL Enforcement

### Problem: Connection string missing sslmode
```env
# Before: no SSL
DATABASE_URL=postgresql://user:pass@host/db
```

### Fix: Add sslmode=require
```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

For Neon: SSL is always required. Connections without `?sslmode=require` may still work but aren't explicitly enforced.

## Sensitive Field Exposure

### Problem: API returns full model including secrets
```typescript
// Before: returns everything including password hash
const user = await prisma.user.findUnique({
  where: { id: userId }
})
return NextResponse.json(user)
```

### Fix: Always use select
```typescript
const user = await prisma.user.findUnique({
  where: { id: userId },
  select: {
    id: true,
    email: true,
    name: true,
    image: true,
    // Never: password, accessToken, refreshToken
  }
})
return NextResponse.json(user)
```

### Audit checklist
Search all API routes for `findUnique`, `findFirst`, `findMany` without `select`:
```
grep -r "findUnique\|findFirst\|findMany" src/app/api/ --include="*.ts"
```
Every result should have a `select` clause.

## Raw Query Safety

### Problem: Using $queryRawUnsafe with user input
```typescript
// DANGEROUS: SQL injection
const result = await prisma.$queryRawUnsafe(
  `SELECT * FROM user WHERE email = '${email}'`
)
```

### Fix: Use parameterized $queryRaw or Prisma ORM
```typescript
// Option 1: Parameterized raw query
const result = await prisma.$queryRaw`
  SELECT * FROM user WHERE email = ${email}
`

// Option 2: Prisma ORM (preferred)
const result = await prisma.user.findUnique({
  where: { email },
  select: { id: true, email: true }
})
```

## Connection String Hardcoding

### Problem: Credentials in source code
```typescript
// NEVER do this
const prisma = new PrismaClient({
  datasources: {
    db: { url: "postgresql://admin:secret@host/db" }
  }
})
```

### Fix: Always use env vars
```typescript
// prisma.config.ts
export default defineConfig({
  datasource: {
    url: process.env.DATABASE_URL,
    directUrl: process.env.DIRECT_URL,
  }
})
```

Verify `.env` is in `.gitignore`. Verify no credentials in git history.

## Rate Limiting on DB-Heavy Endpoints

### Problem: Unbounded queries without rate limit
```typescript
// Before: anyone can spam this endpoint
export async function GET() {
  const data = await prisma.purchase.findMany()
  return NextResponse.json(data)
}
```

### Fix: Add rate limiting + pagination
```typescript
import { rateLimit } from "@/lib/rate-limit"

export async function GET(request: Request) {
  const ip = getClientIp(request)
  const { success } = await rateLimit.standard.limit(ip)
  if (!success) return new Response("Too many requests", { status: 429 })

  const data = await prisma.purchase.findMany({
    take: 20,
    select: { id: true, status: true, amount: true }
  })
  return NextResponse.json(data)
}
```

## Error Message Leaking

### Problem: Database errors exposed to client
```typescript
// Before: leaks schema details
catch (error) {
  return NextResponse.json({ error: error.message }, { status: 500 })
}
```

### Fix: Generic message, log internally
```typescript
catch (error) {
  console.error("Database error:", error) // Internal log
  return NextResponse.json(
    { error: "An unexpected error occurred" },
    { status: 500 }
  )
}
```
