# Self-Hosting

> Source: https://nextjs.org/docs/app/guides/self-hosting (v16.1.6)

## Reverse Proxy

Use nginx (or similar) in front of Next.js to handle: malformed requests, slow connection attacks, payload limits, rate limiting.

## Image Optimization

Works with zero config via `next start`. Options:

| Option | Details |
|--------|---------|
| Default | Built-in optimizer with `next start` |
| Custom loader | Configure in `next.config.js` |
| Static export | Define custom image loader |
| Disable | Set `unoptimized: true` |

Note: On glibc Linux, may need [sharp memory config](https://sharp.pixelplumbing.com/install#linux-memory-allocator).

## Environment Variables

- Server-only by default; prefix `NEXT_PUBLIC_` for browser
- Runtime env vars: use Dynamic APIs (`cookies`, `headers`, `connection`)

```typescript
import { connection } from 'next/server'

export default async function Component() {
  await connection() // opts into dynamic rendering
  const value = process.env.MY_VALUE // evaluated at runtime
}
```

## Caching & ISR

| Behavior | Details |
|----------|---------|
| Default cache | Filesystem (disk) on Next.js server |
| Immutable assets | `Cache-Control: public, max-age=31536000, immutable` |
| ISR | `s-maxage: <revalidate>, stale-while-revalidate` |
| Dynamic pages | `private, no-cache, no-store, max-age=0, must-revalidate` |
| Static assets CDN | Use `assetPrefix` in config |

### Custom Cache Handler

```javascript
// next.config.js
module.exports = {
  cacheHandler: require.resolve('./cache-handler.js'),
  cacheMaxMemorySize: 0, // disable in-memory cache
}
```

```javascript
// cache-handler.js
const cache = new Map()
module.exports = class CacheHandler {
  async get(key) { return cache.get(key) }
  async set(key, data, ctx) {
    cache.set(key, { value: data, lastModified: Date.now(), tags: ctx.tags })
  }
  async revalidateTag(tags) {
    tags = [tags].flat()
    for (let [key, value] of cache) {
      if (value.tags.some((tag) => tags.includes(tag))) cache.delete(key)
    }
  }
  resetRequestCache() {}
}
```

## Multi-Server / Containers

### Build ID Consistency

```javascript
// next.config.js
module.exports = {
  generateBuildId: async () => process.env.GIT_HASH,
}
```

### Server Actions Encryption Key

All instances must share the same key:

```bash
NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=your-base64-key next build
```

### Version Skew Protection

```javascript
// next.config.js
module.exports = {
  deploymentId: process.env.DEPLOYMENT_VERSION,
}
```

On mismatch: triggers hard navigation (full reload) to get correct assets.

## Streaming

Disable proxy buffering for streaming/Suspense:

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [{
      source: '/:path*{/}?',
      headers: [{ key: 'X-Accel-Buffering', value: 'no' }],
    }]
  },
}
```

## CDN Behavior

| Page Type | Cache-Control |
|-----------|---------------|
| Dynamic (uses Dynamic APIs) | `private` (not CDN-cacheable) |
| Fully static (prerendered) | `public` (CDN-cacheable) |

## `after()` Support

Fully supported with `next start`. Send `SIGINT`/`SIGTERM` for graceful shutdown.

## Quick Reference

| Concern | Solution |
|---------|----------|
| Security | Reverse proxy (nginx) in front |
| Images | Built-in; or custom loader |
| Runtime env vars | Use `connection()` + Dynamic APIs |
| Shared cache | Custom `cacheHandler` (Redis, S3) |
| Multi-instance | Shared build ID + encryption key + `deploymentId` |
| Streaming | `X-Accel-Buffering: no` header |
| Static assets CDN | `assetPrefix` config |
