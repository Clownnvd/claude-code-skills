# Tailwind CSS v3 Setup

> Source: https://nextjs.org/docs/app/guides/tailwind-v3-css (v16.1.6)

Guide for installing Tailwind CSS **v3** with Next.js. For Tailwind v4, see the main CSS docs.

## Installation

```bash
pnpm add -D tailwindcss@^3 postcss autoprefixer
npx tailwindcss init -p
```

## Configuration

### tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Global CSS (app/globals.css)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Import in Root Layout

```tsx
// app/layout.tsx
import './globals.css'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

## Usage

```tsx
// app/page.tsx
export default function Page() {
  return <h1 className="text-3xl font-bold underline">Hello, Next.js!</h1>
}
```

## Turbopack

Tailwind CSS and PostCSS are supported with Turbopack since Next.js 13.1.

## Quick Reference

| Step | Action |
|---|---|
| Install | `pnpm add -D tailwindcss@^3 postcss autoprefixer` |
| Init config | `npx tailwindcss init -p` |
| Content paths | `./app/**/*.{js,ts,jsx,tsx,mdx}` (+ pages, components) |
| CSS directives | `@tailwind base; @tailwind components; @tailwind utilities;` |
| Import CSS | `import './globals.css'` in root layout |
| Turbopack | Supported since Next.js 13.1 |
| Tailwind v4 | See `/docs/app/getting-started/css#tailwind-css` |
