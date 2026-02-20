# Font Optimization

> Source: nextjs.org/docs/app/getting-started/fonts (v16.1.6)

## `next/font` Features

- Auto self-hosting (no external requests to Google)
- Zero layout shift
- Fonts served as static assets from same domain
- Scoped to component where used — apply to root layout for app-wide

## Google Fonts

Import from `next/font/google`. Self-hosted automatically.

```tsx
// app/layout.tsx
import { Geist } from 'next/font/google'

const geist = Geist({ subsets: ['latin'] })

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={geist.className}>
      <body>{children}</body>
    </html>
  )
}
```

Prefer **variable fonts** for best performance. For non-variable fonts, specify `weight`:

```tsx
import { Roboto } from 'next/font/google'
const roboto = Roboto({ weight: '400', subsets: ['latin'] })
```

## Local Fonts

Import from `next/font/local`. Store in `public/` or colocate in `app/`.

```tsx
import localFont from 'next/font/local'
const myFont = localFont({ src: './my-font.woff2' })
```

Multiple files for one font family — `src` as array:

```ts
const roboto = localFont({
  src: [
    { path: './Roboto-Regular.woff2', weight: '400', style: 'normal' },
    { path: './Roboto-Italic.woff2', weight: '400', style: 'italic' },
    { path: './Roboto-Bold.woff2', weight: '700', style: 'normal' },
    { path: './Roboto-BoldItalic.woff2', weight: '700', style: 'italic' },
  ],
})
```

## Using with Tailwind CSS 4

Set as CSS variable, then use in Tailwind config:

```tsx
const geist = Geist({ subsets: ['latin'], variable: '--font-geist' })

// In layout: className={geist.variable}
```

```css
/* app/globals.css */
@import 'tailwindcss';
@theme { --font-sans: var(--font-geist); }
```

## Quick Reference

| Option | Type | Notes |
|--------|------|-------|
| `subsets` | `string[]` | Required for Google fonts (`['latin']`) |
| `weight` | `string \| string[]` | Required for non-variable Google fonts |
| `style` | `string \| string[]` | `'normal'`, `'italic'` |
| `variable` | `string` | CSS variable name (e.g., `'--font-geist'`) |
| `display` | `string` | `font-display` value (default `'swap'`) |
| `preload` | `boolean` | Default `true` |
| `className` | — | Return value — apply to element |
