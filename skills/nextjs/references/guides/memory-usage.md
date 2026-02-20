# Memory Usage Optimization

> Source: https://nextjs.org/docs/app/guides/memory-usage (v16.1.6)

## Strategies Overview

| Strategy | Description | Config/Command |
|----------|-------------|----------------|
| Reduce dependencies | Use Bundle Analyzer to find large deps | See package-bundling guide |
| Webpack memory opt | Reduces max memory, slightly slower builds | `experimental.webpackMemoryOptimizations: true` |
| Debug memory usage | Prints heap/GC stats during build | `next build --experimental-debug-memory-usage` |
| Heap profile | Record `.heapprofile` for Chrome DevTools | `node --heap-prof node_modules/next/dist/bin/next build` |
| Heap snapshot | Inspector-based analysis | `NODE_OPTIONS=--inspect next build` |
| Webpack build worker | Run compilations in separate worker | `experimental.webpackBuildWorker: true` (default since v14.1) |
| Disable webpack cache | Reduce memory from cached modules | Custom webpack config (see below) |
| Disable typechecking | Skip "Running TypeScript" step | `typescript.ignoreBuildErrors: true` |
| Disable source maps | Skip source map generation | `productionBrowserSourceMaps: false` + `experimental.serverSourceMaps: false` |
| Disable preload entries | Don't preload page JS modules on start | `experimental.preloadEntriesOnStart: false` |

## Webpack Memory Optimizations (v15+)

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  experimental: {
    webpackMemoryOptimizations: true,
  },
}
export default config
```

## Disable Webpack Cache

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  webpack: (config, { dev }) => {
    if (config.cache && !dev) {
      config.cache = Object.freeze({ type: 'memory' })
    }
    return config
  },
}
export default config
```

## Disable Source Maps

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  productionBrowserSourceMaps: false,
  experimental: {
    serverSourceMaps: false,
  },
  // If using cacheComponents and prerender OOMs:
  // enablePrerenderSourceMaps: false,
}
export default config
```

## Disable Preloading Entries

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  experimental: {
    preloadEntriesOnStart: false,
  },
}
export default config
```

## Heap Analysis Commands

```bash
# Record heap profile
node --heap-prof node_modules/next/dist/bin/next build

# Debug memory usage (v14.2+)
next build --experimental-debug-memory-usage

# Inspect with Chrome DevTools
NODE_OPTIONS=--inspect next build
# Send SIGUSR2 to take heap snapshot while running
```

## Notes

- `--experimental-debug-memory-usage` is incompatible with Webpack build worker (auto-enabled without custom webpack config)
- `webpackBuildWorker` may not work with all custom Webpack plugins
- `typescript.ignoreBuildErrors` can cause faulty deploys -- run type checks in CI separately
- Edge runtime memory issue fixed in v14.1.3
- Preloaded entries will eventually load anyway when pages are requested

## Quick Reference

| Need | Solution |
|------|----------|
| Reduce build memory | `webpackMemoryOptimizations: true` |
| Debug OOM builds | `next build --experimental-debug-memory-usage` |
| Profile heap | `node --heap-prof ... next build` |
| Skip typechecking in build | `typescript.ignoreBuildErrors: true` |
| Skip source maps | `productionBrowserSourceMaps: false` |
| Reduce server startup memory | `experimental.preloadEntriesOnStart: false` |
| Disable webpack cache | Custom webpack config with `cache: { type: 'memory' }` |
