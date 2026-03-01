# Build Optimization

> Part of: CI/CD & Deployment Reference -- Next.js 16 + Prisma + Neon (CViet)
> Stack: Next.js 16.1.6 (App Router, Webpack mode) | Prisma 6 + Neon PostgreSQL | pnpm | TypeScript

---

## 9.1 pnpm Store Caching in GitHub Actions

```yaml
- name: Setup pnpm
  uses: pnpm/action-setup@v4
  with:
    version: '10'

- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '22'
    cache: 'pnpm'  # Caches pnpm store based on pnpm-lock.yaml hash
```

This caches the pnpm content-addressable store (`~/.local/share/pnpm/store`). On cache hit, `pnpm install` only links packages (very fast).

## 9.2 Next.js Build Cache (.next/cache)

```yaml
- name: Cache Next.js build
  uses: actions/cache@v4
  with:
    path: .next/cache
    key: nextjs-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}-${{ hashFiles('src/**/*') }}
    restore-keys: |
      nextjs-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}-
      nextjs-${{ runner.os }}-
```

Without this cache, you may see: `warn - No build cache found. Please configure build caching for faster rebuilds.`

## 9.3 Turbopack Build Cache (Next.js 16)

Next.js 16 introduced Turbopack filesystem cache for builds:

```ts
// next.config.ts
const nextConfig: NextConfig = {
  experimental: {
    turbopackFileSystemCacheForBuild: true,  // Opt-in for builds
  },
}
```

**Note:** CViet currently uses `--webpack` flag for builds due to Tailwind v4 compatibility issues. If migrating to Turbopack for production builds, enable this option and cache `.next/cache` in CI.

## 9.4 Parallel Jobs

Structure CI to run independent jobs in parallel:

```
                    ┌─ lint ──────────────┐
push/PR triggers ───┤                     ├── build ── deploy
                    └─ type-check ────────┘
```

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    # ...

  type-check:
    runs-on: ubuntu-latest
    # ...

  build:
    needs: [lint, type-check]  # Runs after both complete
    # ...

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    # ...
```

## 9.5 Selective Builds (Skip Unchanged)

```yaml
# Skip CI for docs-only changes
on:
  push:
    paths-ignore:
      - '**.md'
      - '.tmp/**'
      - 'screenshots/**'
      - '.vscode/**'
```

## 9.6 Build Performance Benchmarks

| Optimization | First Build | Cached Build |
|-------------|-------------|-------------|
| No caching | ~90-120s | ~90-120s |
| pnpm store cached | ~60-90s | ~30-50s |
| + .next/cache | ~60-90s | ~15-30s |
| + Turbopack filesystem cache | ~40-60s | ~10-20s |

---

> **Sources:**
> - [Next.js CI Build Caching Guide](https://nextjs.org/docs/pages/guides/ci-build-caching)
> - [Next.js Turbopack Filesystem Cache](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopackFileSystemCache)
> - [pnpm GitHub Actions Setup](https://pnpm.io/continuous-integration)
