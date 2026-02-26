# CSS

> Source: nextjs.org/docs/app/getting-started/css (v16.1.6)

## Styling Options

| Method | Scope | Use case |
|--------|-------|----------|
| Tailwind CSS | Utility classes | Primary styling (recommended) |
| CSS Modules | Component-scoped | Custom scoped CSS when Tailwind insufficient |
| Global CSS | Application-wide | Truly global styles (resets, base) |
| External stylesheets | Package CSS | Third-party (e.g., Bootstrap) |
| Sass | File-scoped | `.scss`/`.sass` support |
| CSS-in-JS | Component-scoped | Runtime styling libraries |

## Tailwind CSS Setup

```bash
pnpm add -D tailwindcss @tailwindcss/postcss
```

```js
// postcss.config.mjs
export default {
  plugins: { '@tailwindcss/postcss': {} },
}
```

```css
/* app/globals.css */
@import 'tailwindcss';
```

```tsx
// app/layout.tsx — import in root layout
import './globals.css'
```

Usage:
```tsx
<h1 className="text-4xl font-bold">Welcome</h1>
```

## CSS Modules

File extension: `.module.css`. Generates unique class names — no collisions.

```css
/* app/blog/blog.module.css */
.blog { padding: 24px; }
```

```tsx
import styles from './blog.module.css'
export default function Page() {
  return <main className={styles.blog}></main>
}
```

## Global CSS

Import in root layout — applies to all routes.

```css
/* app/global.css */
body { padding: 20px 20px 60px; max-width: 680px; margin: 0 auto; }
```

```tsx
// app/layout.tsx
import './global.css'
```

Global styles can be imported in any layout/page/component in `app/`. But stylesheets aren't removed on navigation (Suspense integration limitation) — prefer Tailwind or CSS Modules for component styling.

## External Stylesheets

Import anywhere in `app/`:
```tsx
import 'bootstrap/dist/css/bootstrap.css'
```

React 19: `<link rel="stylesheet" href="..." />` also supported.

## CSS Ordering & Merging

CSS order = import order in code. Production builds auto-chunk and merge.

### Recommendations

- Import global/Tailwind styles in root layout
- Use Tailwind for most styling
- CSS Modules for component-specific styles when needed
- Contain CSS imports to single entry files where possible
- Consistent naming: `<name>.module.css`
- Extract shared styles into shared components
- Disable auto-sort imports (ESLint `sort-imports`) — breaks CSS ordering
- Control chunking: `cssChunking` option in `next.config.js`

## Dev vs Production

| | Development (`next dev`) | Production (`next build`) |
|--|--------------------------|---------------------------|
| Updates | Instant (Fast Refresh) | Minified + code-split `.css` files |
| JS required | Yes (for Fast Refresh) | No (CSS loads without JS) |
| Ordering | May differ from prod | Final CSS order — always verify |
