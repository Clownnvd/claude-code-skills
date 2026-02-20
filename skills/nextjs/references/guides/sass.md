# Sass

> Source: https://nextjs.org/docs/app/guides/sass (v16.1.6)

## Overview

Next.js has built-in Sass support for `.scss` and `.sass` files, including CSS Modules (`.module.scss` / `.module.sass`).

## Installation

```bash
npm install --save-dev sass
```

## Syntax Options

| Extension | Syntax | Description |
|-----------|--------|-------------|
| `.scss` | SCSS | Superset of CSS (recommended) |
| `.sass` | Indented | Whitespace-based, no braces/semicolons |

## Customizing Sass Options

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  sassOptions: {
    additionalData: `$var: red;`,
  },
}
export default nextConfig
```

### Custom Implementation

Use `sass-embedded` for faster compilation:

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  sassOptions: {
    implementation: 'sass-embedded',
  },
}
export default nextConfig
```

## Sass Variables with CSS Modules

Export Sass variables for use in components:

```scss
// app/variables.module.scss
$primary-color: #64ff00;

:export {
  primaryColor: $primary-color;
}
```

```typescript
// app/page.tsx
import variables from './variables.module.scss'

export default function Page() {
  return <h1 style={{ color: variables.primaryColor }}>Hello, Next.js!</h1>
}
```

## Quick Reference

| Task | How |
|------|-----|
| Install | `npm install --save-dev sass` |
| CSS Modules | Use `.module.scss` extension |
| Global styles | Import `.scss` in layout |
| Config options | `sassOptions` in `next.config.ts` |
| Faster builds | `implementation: 'sass-embedded'` |
| Export variables | `:export { name: $var; }` in `.module.scss` |
