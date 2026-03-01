# Performance Patterns

> Tree shaking, content detection, spacing scale, and production build for Tailwind CSS v4

---

## Automatic Tree Shaking

v4 only generates CSS for classes actually used in your templates. There is no "purge" step -- unused classes are never generated. Output is typically under 10KB gzipped.

## Content Auto-Detection

v4 automatically:
- Respects `.gitignore` (skips `node_modules`, build output)
- Ignores binary files (images, videos, archives)
- Scans all text files for class patterns

No `content` configuration needed.

## Spacing Scale (Single Variable)

v4 derives ALL spacing utilities from a single `--spacing` variable:

```css
@theme {
  --spacing: 0.25rem;  /* 4px base */
}
```

This means `p-4` = `1rem`, `mt-8` = `2rem`, `gap-6` = `1.5rem`. You can use ANY integer, not just predefined values: `p-13`, `w-17`, `gap-29` all work.

## Dynamic Utility Values

v4 accepts any reasonable value without configuration:

```html
<div class="grid grid-cols-15">   <!-- 15-column grid -->
<div class="mt-13">               <!-- 13 * 0.25rem = 3.25rem -->
<div class="w-[calc(100%-2rem)]"> <!-- arbitrary calc -->
```

## Production Build

```bash
# Next.js builds Tailwind as part of the build step
pnpm build

# Output CSS is automatically minified and tree-shaken
```

## Avoid

- Do NOT dynamically construct class names with string concatenation:
  ```ts
  // BAD: Tailwind can't detect these
  const color = 'red';
  className={`bg-${color}-500`}

  // GOOD: Use complete class names
  const colorClass = isError ? 'bg-red-500' : 'bg-green-500';
  ```

- Do NOT use `@apply` excessively -- it defeats the purpose of utility-first CSS and increases bundle size.
