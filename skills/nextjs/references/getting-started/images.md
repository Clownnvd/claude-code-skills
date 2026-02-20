# Image Optimization

> Source: nextjs.org/docs/app/getting-started/images (v16.1.6)

## `next/image` Features

- Auto size optimization (serves correct size per device, WebP format)
- Prevents layout shift (CLS) via required width/height
- Lazy loading (native browser, viewport-based)
- Blur-up placeholder support
- On-demand resizing (local + remote)

## Local Images

### From `public/` (string path)

```tsx
import Image from 'next/image'

<Image src="/profile.png" alt="Profile" width={500} height={500} />
```

Must provide `width` and `height` manually.

### Static import (auto dimensions)

```tsx
import Image from 'next/image'
import ProfileImage from './profile.png'

<Image
  src={ProfileImage}
  alt="Profile"
  // width/height auto-provided
  // blurDataURL auto-provided
  placeholder="blur"  // optional blur-up while loading
/>
```

## Remote Images

Provide URL string + manual `width`/`height` (or use `fill`).

```tsx
<Image
  src="https://s3.amazonaws.com/my-bucket/profile.png"
  alt="Profile"
  width={500}
  height={500}
/>
```

### `fill` property (alternative to width/height)

Makes image fill parent element size. Parent must have `position: relative`.

### Remote patterns config (required for security)

```ts
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 's3.amazonaws.com',
        port: '',
        pathname: '/my-bucket/**',
        search: '',
      },
    ],
  },
}
export default config
```

Be as specific as possible to prevent malicious usage.

## Quick Reference

| Prop | Required | Notes |
|------|----------|-------|
| `src` | Yes | String path, URL, or static import |
| `alt` | Yes | Always provide for accessibility |
| `width` | Yes* | Auto if static import. Required for remote/public. |
| `height` | Yes* | Auto if static import. Required for remote/public. |
| `fill` | No | Alternative to width/height — fills parent |
| `placeholder` | No | `"blur"` for blur-up effect |
| `blurDataURL` | No | Auto for static imports. Manual for remote. |
| `priority` | No | Set `true` for LCP image (disables lazy loading) |
| `sizes` | No | Media query string for responsive sizing |
| `quality` | No | 1-100 (default 75) |
