# Directives and Functions Reference

> Complete reference for all Tailwind CSS v4 directives and built-in functions

---

## Directives

| Directive | Purpose | Example |
|-----------|---------|---------|
| `@import` | Import CSS files (Tailwind, fonts, etc.) | `@import "tailwindcss"` |
| `@theme` | Define design tokens that generate utilities | `@theme { --color-brand: #1B4FD8 }` |
| `@theme inline` | Keeps var() references in output | `@theme inline { --font-sans: var(--font-inter) }` |
| `@theme static` | Generates utilities without :root vars | `@theme static { ... }` |
| `@utility` | Define custom utilities (v4 replaces @layer utilities) | `@utility btn { ... }` |
| `@variant` | Apply a Tailwind variant in CSS | `@variant dark { background: black }` |
| `@custom-variant` | Create a custom variant | `@custom-variant dark (&:where(.dark, .dark *))` |
| `@layer` | Native CSS cascade layer | `@layer base { body { ... } }` |
| `@apply` | Inline utility classes into CSS | `@apply rounded-lg shadow-md` |
| `@source` | Add extra content sources for scanning | `@source "../node_modules/@co/ui"` |
| `@reference` | Import theme vars for scoped styles (no output) | `@reference "../../app.css"` |
| `@config` | Load legacy JS config (migration) | `@config "../../tailwind.config.js"` |
| `@plugin` | Load legacy JS plugins | `@plugin "@tailwindcss/typography"` |

## Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `--alpha()` | Adjust color opacity at build time | `color: --alpha(var(--color-brand) / 50%)` |
| `--spacing()` | Generate spacing calc from theme | `margin: --spacing(4)` |
| `theme()` | Access theme values (deprecated, use CSS vars) | `theme(--breakpoint-xl)` (only in `@media`) |

## Using Theme Variables in Custom CSS

```css
@layer base {
  h1 {
    font-size: var(--text-2xl);
    font-weight: var(--font-weight-bold);
    color: var(--color-text);
    letter-spacing: var(--tracking-tight);
  }
}
```

## Using Theme Variables in JavaScript

```ts
// Read theme variable at runtime
const styles = getComputedStyle(document.documentElement);
const brandColor = styles.getPropertyValue('--color-brand');

// Use in inline styles
<div style={{ backgroundColor: 'var(--color-brand)' }} />

// Use in animation libraries (e.g., Framer Motion)
<motion.div animate={{ backgroundColor: 'var(--color-brand)' }} />
```
