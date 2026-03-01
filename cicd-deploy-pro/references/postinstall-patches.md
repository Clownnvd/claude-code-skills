# Postinstall Patches in CI

## Why Patches Are Needed

CViet uses `scripts/postinstall.js` to patch 6 bugs in Next.js 16.1.6. These patches MUST run in CI after `pnpm install` and before `pnpm build`.

## Patch Summary

| # | File Patched | Bug | Effect If Missing |
|---|-------------|-----|-------------------|
| 1 | `build/generate-build-id.js` | `generate()` may not be a function | Build crash: `TypeError: generate is not a function` |
| 2 | `build/swc/options.js` | `useCacheEnabled`/`cacheComponentsEnabled` undefined | SWC crash: JSON deserialization error |
| 3 | `server/web/exports/next-response.js` (stub) | Missing file | Build crash: `Module not found` |
| 4 | `server/web/exports/next-request.js` (stub) | Missing file | Build crash: `Module not found` |
| 5 | `build/after-production-compile.js` | `config.compiler` undefined | Build crash: `TypeError: Cannot read properties of undefined` |
| 6 | `build/index.js` | `picomatch` hostname undefined | Build crash: `TypeError: Cannot read properties of undefined` |
| 7 | `export/index.js` | `htmlLimitedBots?.source` undefined | Build crash: `TypeError: Cannot read properties of undefined` |

## CI Integration

The postinstall script runs automatically via pnpm's `postinstall` hook:

```json
{
  "scripts": {
    "postinstall": "node scripts/postinstall.js"
  }
}
```

**In CI, this happens automatically** during `pnpm install --frozen-lockfile`. No separate step is needed unless you want explicit logging:

```yaml
- name: Install dependencies
  run: pnpm install --frozen-lockfile
  # postinstall.js runs automatically here

# Optional: explicit verification
- name: Verify patches applied
  run: node scripts/postinstall.js
```

## Vercel Behavior

On Vercel, `pnpm install` runs the `postinstall` script automatically. No configuration needed. The patches are idempotent -- running them multiple times is safe.

## Docker Behavior

In the Dockerfile, `pnpm install --frozen-lockfile` in the deps stage does NOT copy `scripts/postinstall.js` (only `package.json` and `pnpm-lock.yaml` are copied). You must run patches explicitly in the builder stage:

```dockerfile
# In deps stage: install without postinstall (script not available yet)
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --ignore-scripts

# In builder stage: copy everything and run patches
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN node scripts/postinstall.js
```

**Alternative:** Copy `scripts/postinstall.js` into the deps stage:

```dockerfile
COPY package.json pnpm-lock.yaml scripts/postinstall.js ./scripts/
RUN pnpm install --frozen-lockfile
# postinstall runs automatically
```

## Upgrade Protocol

When upgrading Next.js (e.g., from 16.1.6 to 16.2.x):

1. Run `pnpm build` WITHOUT `postinstall.js` to see which patches are still needed
2. The patch script is idempotent -- it skips patches where the target string no longer exists
3. Remove patches that are no longer needed (target not found = bug was fixed upstream)
4. Re-enable `postinstall.js` and verify build passes
