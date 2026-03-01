# Common Errors and Fixes

> 20 documented Tailwind CSS v4 errors (TW-001 through TW-020) with exact messages, causes, and fixes

---

## TW-001: PostCSS Plugin Not Found

**Error**:
```
It looks like you're trying to use `tailwindcss` directly as a PostCSS plugin.
The PostCSS plugin has moved to a separate package.
```

**Cause**: Using `tailwindcss` instead of `@tailwindcss/postcss` in PostCSS config.

**Fix**:
```js
// postcss.config.mjs
const config = {
  plugins: {
    "@tailwindcss/postcss": {},  // NOT "tailwindcss"
  },
};
export default config;
```

---

## TW-002: @tailwind Directive Not Recognized

**Error**:
```
Unknown at rule @tailwind
```

**Cause**: Using v3 `@tailwind` directives with v4.

**Fix**:
```css
/* Remove these: */
/* @tailwind base; */
/* @tailwind components; */
/* @tailwind utilities; */

/* Replace with: */
@import "tailwindcss";
```

---

## TW-003: Styles Not Applied in Development

**Error**: Classes render in HTML but no CSS is generated. Page appears unstyled.

**Cause**: `NODE_ENV=production` set by VSCode terminal or IDE, causing webpack to skip Tailwind CSS processing.

**Fix**:
```json
{
  "scripts": {
    "dev": "cross-env NODE_ENV=development next dev --webpack"
  }
}
```

---

## TW-004: Duplicate PostCSS Config

**Error**: Tailwind processes twice, duplicated styles, or conflicting behavior.

**Cause**: Having BOTH `postcss.config.js` AND `postcss.config.mjs`.

**Fix**: Delete `postcss.config.js`, keep ONLY `postcss.config.mjs`.

---

## TW-005: @import Order Error

**Error**: Google Fonts not loading, or Tailwind styles override font imports.

**Cause**: `@import "tailwindcss"` placed BEFORE external font imports.

**Fix**:
```css
/* External fonts FIRST */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Tailwind SECOND */
@import "tailwindcss";
```

---

## TW-006: Custom Classes Not Generating

**Error**: Using `bg-brand` but no CSS is generated.

**Cause**: Color defined in `:root` instead of `@theme`.

**Fix**:
```css
/* WRONG: `:root` does not generate utilities */
:root {
  --color-brand: #1B4FD8;
}

/* CORRECT: `@theme` generates utilities */
@theme inline {
  --color-brand: #1B4FD8;
}
```

---

## TW-007: shadow/rounded/blur Scale Mismatch

**Error**: `shadow-sm` appears smaller than expected, `rounded` seems too small.

**Cause**: v4 renamed the scale. What was `shadow-sm` in v3 is now `shadow-xs` in v4.

**Fix**: Apply the rename mapping:
```
v3 shadow-sm  ->  v4 shadow-xs
v3 shadow     ->  v4 shadow-sm
v3 rounded-sm ->  v4 rounded-xs
v3 rounded    ->  v4 rounded-sm
v3 blur-sm    ->  v4 blur-xs
v3 blur       ->  v4 blur-sm
```

---

## TW-008: outline-none Not Working

**Error**: `outline-none` does not remove focus outlines as expected.

**Cause**: In v4, `outline-none` sets `outline-style: none` (truly removes outline). The old behavior (invisible outline for accessibility) is now `outline-hidden`.

**Fix**:
```html
<!-- v3 behavior (visually hidden but accessible) -->
<input class="focus:outline-hidden" />

<!-- v4 true removal (avoid for accessibility) -->
<input class="focus:outline-none" />
```

---

## TW-009: Ring Width Default Changed

**Error**: `ring ring-blue-500` produces a 1px ring instead of 3px.

**Cause**: v4 changed `ring` from 3px to 1px.

**Fix**:
```html
<!-- v4: specify width explicitly -->
<input class="focus:ring-3 focus:ring-blue-500" />
```

---

## TW-010: Border Color Default Changed

**Error**: Borders appear in unexpected color (black/currentColor instead of gray).

**Cause**: v4 changed default border color from `gray-200` to `currentColor`.

**Fix**: Always specify border color explicitly:
```html
<div class="border border-border">...</div>
<!-- Or -->
<div class="border border-gray-200">...</div>
```

---

## TW-011: dark: Classes Not Working

**Error**: `dark:bg-gray-900` has no effect when `.dark` class is on `<html>`.

**Cause**: v4 defaults to `prefers-color-scheme` media query, not class-based.

**Fix**: Add `@custom-variant` to your CSS:
```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
```

---

## TW-012: hover: Styles Not Working on Mobile

**Error**: `hover:bg-blue-600` does not apply on tap on mobile devices.

**Cause**: v4 wraps hover in `@media (hover: hover)` to prevent sticky hover states on touch devices.

**Fix** (if you want v3 behavior):
```css
@custom-variant hover (&:hover);
```

---

## TW-013: @layer utilities Not Working for Custom Utilities

**Error**: Custom styles in `@layer utilities { ... }` are ignored or have wrong specificity.

**Cause**: v4 uses `@utility` directive instead of `@layer utilities`.

**Fix**:
```css
/* WRONG (v3 pattern) */
@layer utilities {
  .text-balance { text-wrap: balance; }
}

/* CORRECT (v4 pattern) */
@utility text-balance {
  text-wrap: balance;
}
```

---

## TW-014: @apply Not Working in Vue/Svelte Scoped Styles

**Error**: `@apply text-red-500` fails in `<style scoped>` blocks.

**Cause**: Scoped styles don't have access to Tailwind theme variables.

**Fix**: Use `@reference`:
```vue
<style scoped>
  @reference "../../app.css";
  h1 {
    @apply text-2xl font-bold text-red-500;
  }
</style>
```

Or use CSS variables directly:
```vue
<style scoped>
  h1 {
    color: var(--color-red-500);
  }
</style>
```

---

## TW-015: tailwind.config.js Being Ignored

**Error**: Theme customizations in `tailwind.config.js` have no effect.

**Cause**: v4 no longer auto-detects JS config files.

**Fix** (migration path): Load explicitly or migrate to CSS:
```css
/* Option A: Load legacy config */
@config "../../tailwind.config.js";

/* Option B (recommended): Migrate to @theme */
@theme {
  --color-brand: #1B4FD8;
}
```

---

## TW-016: Button cursor:default (Not pointer)

**Error**: Buttons don't show pointer cursor.

**Cause**: v4 changed default button cursor to match browser native `default`.

**Fix**: Add `cursor-pointer` explicitly, or restore globally:
```css
@layer base {
  button:not(:disabled),
  [role="button"]:not(:disabled) {
    cursor: pointer;
  }
}
```

---

## TW-017: Webpack HMR Not Detecting Tailwind Changes

**Error**: Adding new Tailwind classes requires dev server restart.

**Cause**: Known issue with Tailwind v4 + Webpack 5 HMR.

**Fix**: Use `--webpack` flag with Next.js and ensure `NODE_ENV=development`:
```json
{
  "scripts": {
    "dev": "cross-env NODE_ENV=development next dev --webpack"
  }
}
```

If still broken, restart dev server. This is a known upstream issue.

---

## TW-018: `@theme` Variables Inside Media Queries Fail

**Error**: `@theme` inside `@media` or nested selector fails.

**Cause**: `@theme` must be top-level, not nested.

**Fix**: Keep `@theme` at the top level of your CSS file. Use `:root` for variables that need media-query scoping:
```css
/* WRONG */
@media (prefers-color-scheme: dark) {
  @theme { --color-bg: #000; }
}

/* CORRECT */
@theme inline {
  --color-bg: #FAFAF8;
}
.dark {
  --color-bg: #0F172A;
}
```

---

## TW-019: Sass/Less Import Conflicts

**Error**: Sass `@import` or `@use` conflicts with Tailwind.

**Cause**: Tailwind v4 is not compatible with Sass, Less, or Stylus.

**Fix**: Remove Sass/Less entirely. Use Tailwind's native `@import`, `@theme`, `@layer`, and `@utility` directives instead. Tailwind v4 IS your CSS preprocessor.

---

## TW-020: Content Detection Missing Files

**Error**: Classes in certain files not detected (no CSS generated).

**Cause**: Files are gitignored, or in unexpected locations.

**Fix**: Add explicit sources:
```css
@import "tailwindcss";
@source "../node_modules/@my-company/ui-lib";
@source "./content/**/*.mdx";
```
