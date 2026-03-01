# Common Errors & Fixes

## CD-001: Build Fails -- `prisma generate` No DB Connection

```
Error: Can't reach database server at `localhost:5432`
```

**Cause:** `prisma generate` trying to connect (usually with TypedSQL `--sql` flag).
**Fix:** Use fake DATABASE_URL for build. Standard `prisma generate` (without `--sql`) does NOT need a DB connection.

```bash
DATABASE_URL="postgresql://fake:fake@localhost:5432/fake" pnpm db:generate
```

---

## CD-002: Build Fails -- Missing Environment Variables

```
Error: Missing required environment variable: BETTER_AUTH_SECRET
```

**Cause:** Better Auth validates `BETTER_AUTH_SECRET` at import time during build.
**Fix:** Provide a dummy value at build time:

```bash
BETTER_AUTH_SECRET="ci-build-secret-placeholder-32chars" pnpm build
```

---

## CD-003: Build Fails -- `generate is not a function`

```
TypeError: generate is not a function
  at generateBuildId (/node_modules/next/dist/build/generate-build-id.js)
```

**Cause:** Next.js 16.1.6 bug in `generate-build-id.js`.
**Fix:** Patch applied by `scripts/postinstall.js` (Patch 1). Ensure postinstall runs before build.

---

## CD-004: Build Fails -- SWC Deserialization Error

```
thread 'main' panicked at 'called `Result::unwrap()` on an `Err` value: Error("missing field `cacheComponentsEnabled`"'
```

**Cause:** Next.js 16.1.6 passes undefined values to SWC binary; JSON.stringify drops them.
**Fix:** Patch applied by `scripts/postinstall.js` (Patch 2). Adds `?? false` fallbacks.

---

## CD-005: Build Fails -- Module Not Found (next-response/next-request)

```
Module not found: Can't resolve 'next/dist/server/web/exports/next-response'
```

**Cause:** Next.js 16.1.6 references tree-shaking stub files that don't exist.
**Fix:** Patch applied by `scripts/postinstall.js` (Patches 3-4). Creates CJS + ESM stubs.

---

## CD-006: Build Fails -- `config.compiler` Undefined

```
TypeError: Cannot read properties of undefined (reading 'runAfterProductionCompile')
```

**Cause:** Next.js 16.1.6 accesses `config.compiler.runAfterProductionCompile` without null check.
**Fix:** Patch applied by `scripts/postinstall.js` (Patch 5). Also requires `compiler: {}` in next.config.ts.

---

## CD-007: Build Fails -- picomatch Hostname Undefined

```
TypeError: Cannot read properties of undefined (reading 'source')
  at /node_modules/next/dist/build/index.js
```

**Cause:** Remote patterns with undefined hostname passed to picomatch.
**Fix:** Patch applied by `scripts/postinstall.js` (Patch 6). Guards with `p.hostname ?`.

---

## CD-008: Build Fails -- `htmlLimitedBots.source` Undefined

```
TypeError: Cannot read properties of undefined (reading 'source')
  at /node_modules/next/dist/export/index.js:337
```

**Cause:** `nextConfig.htmlLimitedBots` is undefined when not configured.
**Fix:** Patch applied by `scripts/postinstall.js` (Patch 7). Adds optional chaining `?.source`.

---

## CD-009: Vercel Build -- `pnpm-lock.yaml` Mismatch

```
ERR_PNPM_OUTDATED_LOCKFILE  Cannot install with "frozen-lockfile" because pnpm-lock.yaml is not up-to-date
```

**Cause:** `package.json` was updated but `pnpm-lock.yaml` was not regenerated.
**Fix:** Run `pnpm install` locally and commit the updated `pnpm-lock.yaml`.

---

## CD-010: Docker Build -- Prisma Client Not Found at Runtime

```
Error: @prisma/client did not initialize yet. Please run "prisma generate"
```

**Cause:** Prisma's generated client (`node_modules/.prisma/client`) was not copied to the runner stage.
**Fix:** Add these COPY instructions to the Docker runner stage:

```dockerfile
COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma
COPY --from=builder /app/node_modules/@prisma ./node_modules/@prisma
COPY --from=builder /app/prisma ./prisma
```

---

## CD-011: Docker Build -- `@react-pdf/renderer` Native Dependencies

```
Error: Cannot find module '../build/Release/canvas.node'
```

**Cause:** `@react-pdf/renderer` may use native addons that need Alpine-compatible binaries.
**Fix:** Add build dependencies to the Docker deps stage:

```dockerfile
RUN apk add --no-cache libc6-compat python3 make g++
```

Or use `serverExternalPackages` in next.config.ts (already configured for CViet).

---

## CD-012: Vercel Deployment -- Function Timeout on PDF Export

```
FUNCTION_INVOCATION_TIMEOUT
Task timed out after 10.00 seconds
```

**Cause:** Default Vercel function timeout is 10s (Hobby) or 15s (Pro). PDF generation can be slow for complex CVs.
**Fix:** Configure longer timeout in vercel.json:

```json
{
  "functions": {
    "src/app/api/export/[id]/route.ts": {
      "maxDuration": 30
    }
  }
}
```

Or use Pro plan (allows up to 300s).

---

## CD-013: Preview Deployment -- Wrong `NEXT_PUBLIC_APP_URL`

```
OAuth redirect_uri mismatch / CORS errors on preview deployment
```

**Cause:** `NEXT_PUBLIC_APP_URL` is inlined at build time. Preview builds may use production URL.
**Fix:** Use Vercel's `VERCEL_URL` system env var at build time:

```ts
// next.config.ts or env setup
const appUrl = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'
```

---

## CD-014: GitHub Actions -- pnpm Store Cache Miss

```
Cache not found for input keys: pnpm-...
```

**Cause:** Cache key mismatch or first run.
**Fix:** Ensure `pnpm/action-setup@v4` runs BEFORE `actions/setup-node@v4`:

```yaml
- uses: pnpm/action-setup@v4
  with:
    version: '10'
- uses: actions/setup-node@v4
  with:
    node-version: '22'
    cache: 'pnpm'   # This reads the pnpm store path set by action-setup
```

---

## CD-015: Vercel -- Build Cache Not Detected

```
warn - No build cache found. Please configure build caching for faster rebuilds.
```

**Cause:** Vercel normally handles this, but custom install commands or monorepos may break it.
**Fix:** Ensure `.next/cache` is preserved between builds. On Vercel this is automatic. In GitHub Actions, use the `actions/cache@v4` step shown in build-optimization.md.

---

## CD-016: Neon Branch -- Connection Refused in Preview

```
Error: connect ECONNREFUSED - Neon branch not found
```

**Cause:** Neon branch was not created or was cleaned up prematurely.
**Fix:** Verify the `neondatabase/create-branch-action` step completed successfully. Check that branch naming matches between creation and usage (`preview/${PR_NUMBER}`).

---

## CD-017: Node.js Version Mismatch

```
error @prisma/client@6.x.x: The engine "node" is incompatible with this module. Expected version ">=18.18.0".
```

**Cause:** CI runner using old Node.js version.
**Fix:** Pin Node.js version in CI:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '22'
```

---

## CD-018: Hydration Mismatch After Deploy

```
Warning: Text content did not match. Server: "..." Client: "..."
```

**Cause:** Server and client render different content, often due to `Date.now()`, `Math.random()`, or locale differences between build server and client.
**Fix:** Wrap dynamic content in `<Suspense>` or use `suppressHydrationWarning` for intentionally different content (e.g., timestamps).

---

## CD-019: Memory Exceeded During Build

```
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
```

**Cause:** Large application or memory-intensive build (e.g., many pages, large images).
**Fix:**

```bash
# Increase Node.js memory limit
NODE_OPTIONS="--max-old-space-size=4096" pnpm build
```

In GitHub Actions:
```yaml
env:
  NODE_OPTIONS: "--max-old-space-size=4096"
```

---

## CD-020: `cross-env` Not Found in CI

```
sh: cross-env: command not found
```

**Cause:** CViet's dev script uses `cross-env` which is a dependency. In CI, the build script (`next build --webpack`) does not use `cross-env`, but if `dev` is accidentally called:
**Fix:** `cross-env` is in dependencies (not devDependencies), so `pnpm install` installs it. Ensure CI uses `pnpm build` (not `pnpm dev`).
