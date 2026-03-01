# Design Tokens (@theme Directive)

> How to define, extend, and share design tokens in Tailwind CSS v4

---

## Core Concept

The `@theme` directive defines CSS custom properties that ALSO generate corresponding utility classes. This is the key difference from regular `:root` variables.

```css
@theme {
  --color-brand: #1B4FD8;
}
/* Generates: bg-brand, text-brand, border-brand, fill-brand, etc. */

:root {
  --app-sidebar-width: 280px;
}
/* Generates: nothing (just a CSS variable, no utilities) */
```

## @theme Modifiers

| Modifier | Behavior | Use When |
|----------|----------|----------|
| `@theme` (bare) | Resolves values statically into `:root` | Default for most tokens |
| `@theme inline` | Keeps `var()` references in generated CSS | Token references another variable |
| `@theme static` | Generates utilities but does NOT emit `:root` vars | Private tokens that shouldn't leak |

```css
/* inline: keeps var() reference in output */
@theme inline {
  --color-brand: #1B4FD8;
  --font-sans: 'Inter', system-ui, sans-serif;
}

/* static: generates utilities but no :root CSS vars */
@theme static {
  --color-primary: var(--color-red-500);
}
```

## Complete Namespace Reference

| Namespace | Utilities Generated | Example Declaration |
|-----------|-------------------|-------------------|
| `--color-*` | `bg-*`, `text-*`, `border-*`, `fill-*`, `stroke-*`, etc. | `--color-brand: #1B4FD8` |
| `--font-*` | `font-*` (family) | `--font-sans: 'Inter', sans-serif` |
| `--text-*` | `text-*` (size) | `--text-xs: 0.75rem` |
| `--font-weight-*` | `font-*` (weight) | `--font-weight-bold: 700` |
| `--tracking-*` | `tracking-*` | `--tracking-tight: -0.025em` |
| `--leading-*` | `leading-*` | `--leading-tight: 1.25` |
| `--breakpoint-*` | `sm:`, `md:`, `lg:`, etc. | `--breakpoint-sm: 40rem` |
| `--container-*` | `@sm:`, `@md:` container queries | `--container-sm: 24rem` |
| `--spacing` | `p-*`, `m-*`, `gap-*`, `w-*`, `h-*`, etc. | `--spacing: 0.25rem` |
| `--radius-*` | `rounded-*` | `--radius-lg: 0.5rem` |
| `--shadow-*` | `shadow-*` | `--shadow-md: 0 4px 6px ...` |
| `--inset-shadow-*` | `inset-shadow-*` | `--inset-shadow-xs: inset 0 1px ...` |
| `--drop-shadow-*` | `drop-shadow-*` | `--drop-shadow-md: 0 3px 3px ...` |
| `--blur-*` | `blur-*` | `--blur-md: 12px` |
| `--perspective-*` | `perspective-*` | `--perspective-normal: 500px` |
| `--aspect-*` | `aspect-*` | `--aspect-video: 16 / 9` |
| `--ease-*` | `ease-*` | `--ease-out: cubic-bezier(0, 0, 0.2, 1)` |
| `--animate-*` | `animate-*` | `--animate-spin: spin 1s linear infinite` |

## Extending vs Replacing

```css
/* EXTEND: adds to existing defaults */
@theme {
  --color-brand: #1B4FD8;
  /* All default colors (red, blue, etc.) still available */
}

/* REPLACE: wipe namespace, define only yours */
@theme {
  --color-*: initial;        /* Remove ALL default colors */
  --color-brand: #1B4FD8;
  --color-surface: #FFFFFF;
  --color-text: #0F172A;
  /* Only brand, surface, text available now */
}

/* NUKE EVERYTHING: start from zero */
@theme {
  --*: initial;              /* Remove ALL defaults */
  --spacing: 4px;
  --color-brand: #1B4FD8;
}
```

## Animations with Keyframes

```css
@theme {
  --animate-fade-in: fade-in 0.3s ease-out;
  --animate-slide-up: slide-up 0.3s ease-out;

  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes slide-up {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }
}
```

Usage: `<div class="animate-fade-in">` or `<div class="animate-slide-up">`

## Sharing Tokens Across Projects

```css
/* packages/brand/theme.css */
@theme {
  --color-*: initial;
  --color-brand: #1B4FD8;
  --color-accent: #0EA5E9;
  --font-sans: 'Inter', sans-serif;
}

/* packages/app/globals.css */
@import "tailwindcss";
@import "../brand/theme.css";
```
