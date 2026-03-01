# Setup & Version Compatibility

> Tailwind CSS v4 setup for Next.js 16 + PostCSS

---

## Tested Stack (CViet Project)

| Package | Version | Notes |
|---------|---------|-------|
| tailwindcss | ^4 | Core framework |
| @tailwindcss/postcss | ^4 | PostCSS plugin (NEW in v4) |
| Next.js | 16.1.6 | App Router |
| React | 19.2.3 | Server + Client Components |
| Node.js | 20+ | Required minimum |
| PostCSS | (peer dep) | Bundled with @tailwindcss/postcss |

## Browser Support

| Browser | Minimum Version |
|---------|----------------|
| Safari | 16.4+ |
| Chrome | 111+ |
| Firefox | 128+ |

## What Was Removed

- `tailwind.config.js` -- no longer auto-detected (use `@config` directive to load legacy configs)
- `postcss-import` -- handled natively by Tailwind v4
- `autoprefixer` -- handled natively by Tailwind v4
- `content` array -- auto-detected via heuristics (respects `.gitignore`)
- `@tailwind base/components/utilities` directives -- replaced by `@import "tailwindcss"`
- `tailwindcss` as PostCSS plugin -- replaced by `@tailwindcss/postcss`
- JIT mode toggle -- always on (no separate JIT mode; it is the only mode)
- `npx tailwindcss init` -- command removed entirely
- `resolveConfig()` JS function -- use CSS variables with `getComputedStyle()` instead
- `corePlugins` config option -- cannot disable core plugins
- `safelist` config option -- use `@source inline()` instead
- `separator` config option -- removed
- Sass/Less/Stylus support -- Tailwind v4 IS your preprocessor

## Build Performance (vs v3.4)

| Metric | v3.4 | v4.0 | Improvement |
|--------|------|------|-------------|
| Full build | 378ms | 100ms | 3.78x faster |
| Incremental (new CSS) | 44ms | 5ms | 8.8x faster |
| Incremental (no new CSS) | 35ms | 192us | 182x faster |

---

## PostCSS Configuration (Next.js)

File: `postcss.config.mjs` (MUST be `.mjs`, not `.js`)

```js
const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};

export default config;
```

**Critical**: Do NOT include `postcss-import` or `autoprefixer` -- Tailwind v4 handles both natively.

## CSS Entry Point

File: `src/app/globals.css`

```css
/* 1. External font imports FIRST */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* 2. Tailwind import SECOND */
@import "tailwindcss";

/* 3. Theme configuration THIRD */
@theme inline {
  --color-brand: #1B4FD8;
  --font-sans: 'Inter', system-ui, sans-serif;
}

/* 4. Custom variants (if needed) */
@custom-variant dark (&:where(.dark, .dark *));

/* 5. Layer overrides and base styles */
@layer base {
  body {
    font-family: var(--font-sans);
  }
}

/* 6. Custom utilities */
@utility container-app {
  max-width: 1280px;
  margin-inline: auto;
  padding-inline: 1rem;
}
```

**Import order matters**: Google Fonts `@import url()` MUST come BEFORE `@import "tailwindcss"`.

## CSS Layers (Cascade Order)

Tailwind v4 uses native CSS `@layer` for organizing styles:

```
@layer theme    -- Design tokens / CSS custom properties
@layer base     -- Reset / preflight styles
@layer components -- Component classes (from @utility with complex selectors)
@layer utilities -- Atomic utility classes
```

Cascade layers guarantee utilities always override component styles regardless of source order.

To control third-party CSS ordering:

```css
@layer theme, base, third-party, components, utilities;
@import "tailwindcss";
@import "some-library/styles.css" layer(third-party);
```

## Package Dependencies

```json
{
  "devDependencies": {
    "tailwindcss": "^4",
    "@tailwindcss/postcss": "^4"
  }
}
```

No separate `postcss` peer dependency needed -- it is included with `@tailwindcss/postcss`.

## Content Detection

Tailwind v4 automatically detects template files:
- Respects `.gitignore` (skips `node_modules`, dist, etc.)
- Ignores binary files (images, videos, zip, etc.)
- Scans all text files for class usage

To add extra sources manually:

```css
@import "tailwindcss";

/* Add sources not auto-detected */
@source "../node_modules/@my-company/ui-lib";
```
