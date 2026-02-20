# Package Bundling Optimization

> Source: https://nextjs.org/docs/app/guides/package-bundling (v16.1.6)

## Bundle Analysis Tools

| Tool | Engine | Command |
|------|--------|---------|
| Next.js Bundle Analyzer (experimental, v16.1+) | Turbopack | `npx next experimental-analyze` |
| `@next/bundle-analyzer` | Webpack | `ANALYZE=true npm run build` |

### Turbopack Bundle Analyzer (v16.1+)

```bash
# Interactive view in browser
npx next experimental-analyze

# Save to disk for sharing/diffing
npx next experimental-analyze --output
# Output: .next/diagnostics/analyze
```

Features: filter by route, environment (client/server), type (JS/CSS/JSON), search by file, trace import chains.

### Webpack Bundle Analyzer

```bash
pnpm add @next/bundle-analyzer
```

```typescript
// next.config.ts
import type { NextConfig } from 'next'
import bundleAnalyzer from '@next/bundle-analyzer'

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})

const config: NextConfig = {}
export default withBundleAnalyzer(config)
```

```bash
ANALYZE=true pnpm build
```

## Optimizing Large Bundles

### optimizePackageImports

For packages with many exports (icon/utility libraries), only load what you use:

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  experimental: {
    optimizePackageImports: ['icon-library'],
  },
}
export default config
```

> Some libraries are auto-optimized. See [full list](https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports).

### Move Heavy Work to Server Components

Heavy rendering libraries (syntax highlighting, charts, markdown) should run on the server when they don't need browser APIs:

```typescript
// BEFORE: Client Component -- library bundled to client
'use client'
import Highlight from 'prism-react-renderer'
// ... entire prism library shipped to browser

// AFTER: Server Component -- library stays on server
import { codeToHtml } from 'shiki'

export default async function Page() {
  const code = `export function hello() { console.log("hi") }`
  const html = await codeToHtml(code, { lang: 'tsx', theme: 'github-dark' })

  return (
    <pre>
      <code dangerouslySetInnerHTML={{ __html: html }} />
    </pre>
  )
}
```

### serverExternalPackages

Opt specific packages out of server-side bundling:

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  serverExternalPackages: ['package-name'],
}
export default config
```

## Quick Reference

| Need | Solution |
|------|----------|
| Analyze bundles (Turbopack) | `npx next experimental-analyze` |
| Analyze bundles (Webpack) | `@next/bundle-analyzer` + `ANALYZE=true` |
| Optimize barrel imports | `experimental.optimizePackageImports` |
| Reduce client bundle | Move heavy rendering to Server Components |
| Exclude server packages from bundling | `serverExternalPackages` |
| Save analysis for comparison | `npx next experimental-analyze --output` |
