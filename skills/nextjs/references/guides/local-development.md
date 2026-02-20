# Local Development

> Source: https://nextjs.org/docs/app/guides/local-development (v16.1.6)

Optimize your Next.js local development experience. `next dev` compiles routes on-demand (not all at once like `next build`).

## Performance Tips

### 1. Antivirus Exclusions

| OS | Action |
|----|--------|
| Windows | Add project folder to Microsoft Defender exclusion list (Virus & threat protection > Manage settings > Add exclusion) |
| macOS | Enable developer mode: `sudo spctl developer-mode enable-terminal`, then enable terminal in System Settings > Privacy & Security > Developer Tools |

### 2. Use Turbopack (Default in Next.js 16+)

```bash
npm install next@latest
npm run dev          # Turbopack is default
npm run dev -- --webpack  # opt-in to webpack if needed
```

### 3. Optimize Imports

**Icon libraries** -- import specific icons, not the entire library:

```typescript
// Bad: imports thousands of icons
import { TriangleIcon } from '@phosphor-icons/react'

// Good: imports only one
import { TriangleIcon } from '@phosphor-icons/react/dist/csr/Triangle'
```

**Barrel files** -- import directly from specific files when possible.

**Package optimization** (webpack only; Turbopack does this automatically):

```typescript
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ['package-name'],
  },
}
```

### 4. Tailwind CSS Content Config

Be specific -- avoid scanning `node_modules`:

```typescript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',           // Good
    // '../../packages/**/*.{js,ts,jsx,tsx}' // Too broad
  ],
}
```

### 5. Avoid Docker on Mac/Windows for Dev

Docker filesystem access on Mac/Windows causes slow HMR. Use local `npm run dev` instead; reserve Docker for production.

### 6. Server Component HMR Caching

```typescript
// next.config.js
module.exports = {
  experimental: {
    serverComponentsHmrCache: true, // Cache fetch across HMR refreshes
  },
}
```

## Debugging Tools

### Fetch Logging

```typescript
// next.config.js
module.exports = {
  logging: {
    fetches: { fullUrl: true },
  },
}
```

### Turbopack Tracing

```bash
NEXT_TURBOPACK_TRACING=1 npm run dev
# Navigate around, then stop server
# Trace file: .next/dev/trace-turbopack
npx next internal trace .next/dev/trace-turbopack
# View at https://trace.nextjs.org/
```

## Quick Reference

| Item | Detail |
|------|--------|
| Dev server | `next dev` (on-demand compilation) |
| Bundler | Turbopack (default), `--webpack` to opt out |
| Tracing | `NEXT_TURBOPACK_TRACING=1` env var |
| Trace viewer | https://trace.nextjs.org/ |
| Memory issues | See `/docs/app/guides/memory-usage` |
| HMR cache | `serverComponentsHmrCache` experimental option |
| Fetch logging | `logging.fetches.fullUrl: true` |
