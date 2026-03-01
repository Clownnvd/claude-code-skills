# Better Auth -- Next.js 16 Specific Gotchas

> Section 11 from the comprehensive reference.

---

## 11. Next.js 16 Specific Gotchas

### 11.1 Async APIs

In Next.js 16, these are all async and MUST be awaited:

```typescript
// All of these need "await":
const h = await headers()
const c = await cookies()
const p = await params        // in page components
const sp = await searchParams // in page components
```

### 11.2 proxy.ts vs middleware.ts

| Feature | Next.js 15 (`middleware.ts`) | Next.js 16 (`proxy.ts`) |
|---------|-----|-----|
| File name | `middleware.ts` | `proxy.ts` |
| Export name | `export function middleware()` | `export function proxy()` |
| Runtime | Edge (default) | Node.js (default) |
| Database access | Limited (Edge constraints) | Full (Node.js runtime) |
| Better Auth cookie check | `getSessionCookie()` | `getSessionCookie()` (same API) |
| Full session validation | Not recommended (slow on Edge) | Possible (Node.js runtime) |

### 11.3 `use cache` Conflicts

```typescript
// WRONG: headers/cookies inside "use cache"
async function getData() {
  "use cache"
  const session = await auth.api.getSession({ headers: await headers() })
  // ERROR: Dynamic functions cannot be called inside "use cache"
}

// CORRECT: Extract dynamic data first
export default async function Page() {
  const headerString = (await cookies()).toString()
  const data = await getCachedData(headerString)
}

async function getCachedData(cookieStr: string) {
  "use cache"
  // Use pre-extracted cookie string
}
```

### 11.4 Turbopack Compatibility

Better Auth works with Turbopack (Next.js 16 default bundler). No special config needed. If you encounter issues, use `--webpack` flag:

```bash
pnpm dev  # uses Turbopack by default in Next.js 16
pnpm dev --webpack  # fallback to webpack
```

### 11.5 `compiler: {}` Required in next.config.ts

CViet-specific: Next.js 16.1.6 requires `compiler: {}` in next.config.ts to avoid `after-production-compile.js` crash:

```typescript
const nextConfig: NextConfig = {
  compiler: {},  // REQUIRED -- prevents undefined access
  serverExternalPackages: ["@react-pdf/renderer"],
}
```

### 11.6 Build Without Database

For CI/CD builds where DATABASE_URL is not available:

```bash
BETTER_AUTH_SECRET="dummy-secret-for-build-only" \
DATABASE_URL="postgresql://fake:fake@localhost/fake" \
NEXT_PUBLIC_APP_URL="http://localhost:3000" \
pnpm build
```
