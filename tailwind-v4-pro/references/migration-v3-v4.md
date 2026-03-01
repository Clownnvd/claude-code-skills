# Migration from v3 to v4

> Complete checklist for upgrading Tailwind CSS v3 projects to v4

---

## Automated Upgrade Tool

```bash
npx @tailwindcss/upgrade
```

Handles ~90% of changes: class renames, config migration, directive updates.

## Breaking Changes Checklist

### Import System

```css
/* v3 -- REMOVED */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* v4 -- NEW */
@import "tailwindcss";
```

### Renamed Utilities

| v3 | v4 | Why |
|----|-----|-----|
| `shadow-sm` | `shadow-xs` | Scale shifted down |
| `shadow` (bare) | `shadow-sm` | Scale shifted down |
| `drop-shadow-sm` | `drop-shadow-xs` | Scale shifted down |
| `drop-shadow` (bare) | `drop-shadow-sm` | Scale shifted down |
| `blur-sm` | `blur-xs` | Scale shifted down |
| `blur` (bare) | `blur-sm` | Scale shifted down |
| `backdrop-blur-sm` | `backdrop-blur-xs` | Scale shifted down |
| `backdrop-blur` (bare) | `backdrop-blur-sm` | Scale shifted down |
| `rounded-sm` | `rounded-xs` | Scale shifted down |
| `rounded` (bare) | `rounded-sm` | Scale shifted down |
| `outline-none` | `outline-hidden` | `outline-none` now = `outline-style: none` |
| `ring` (bare) | `ring-3` | `ring` now = 1px (consistency) |

### Removed Utilities (Use Opacity Modifier Instead)

| v3 Deprecated | v4 Replacement |
|--------------|----------------|
| `bg-opacity-50` | `bg-black/50` |
| `text-opacity-50` | `text-black/50` |
| `border-opacity-50` | `border-black/50` |
| `divide-opacity-50` | `divide-black/50` |
| `ring-opacity-50` | `ring-black/50` |
| `placeholder-opacity-50` | `placeholder-black/50` |
| `flex-shrink-0` | `shrink-0` |
| `flex-grow` | `grow` |
| `overflow-ellipsis` | `text-ellipsis` |
| `decoration-slice` | `box-decoration-slice` |
| `decoration-clone` | `box-decoration-clone` |

### Default Behavior Changes

| Behavior | v3 | v4 |
|----------|-----|-----|
| Border color | `gray-200` | `currentColor` |
| Ring width | 3px | 1px |
| Ring color | `blue-500` | `currentColor` |
| Placeholder color | `gray-400` | Current text at 50% opacity |
| Button cursor | `pointer` | `default` (browser native) |
| Dark mode | Configurable | `prefers-color-scheme` by default |
| Hover variant | Always applies | Only when `(hover: hover)` media |
| Important `!` | Prefix: `!flex` | Suffix: `flex!` |
| Variant stacking | Right-to-left | Left-to-right |
| Color palette | RGB | OKLch (wider gamut) |
| `space-*` selector | `> :not([hidden]) ~ :not([hidden])` | `> :not(:last-child)` |

### Restoring v3 Defaults (If Needed)

```css
@import "tailwindcss";

/* Restore v3 border color */
@layer base {
  *, ::after, ::before, ::backdrop, ::file-selector-button {
    border-color: var(--color-gray-200, currentColor);
  }
}

/* Restore v3 button cursor */
@layer base {
  button:not(:disabled),
  [role="button"]:not(:disabled) {
    cursor: pointer;
  }
}

/* Restore v3 placeholder color */
@layer base {
  input::placeholder,
  textarea::placeholder {
    color: var(--color-gray-400);
  }
}

/* Restore v3 dialog centering */
@layer base {
  dialog {
    margin: auto;
  }
}

/* Restore v3 hover behavior (no media query guard) */
@custom-variant hover (&:hover);
```

### Syntax Changes

```html
<!-- Variables in arbitrary values -->
<!-- v3 --> <div class="bg-[--brand-color]"></div>
<!-- v4 --> <div class="bg-(--brand-color)"></div>

<!-- Important modifier -->
<!-- v3 --> <div class="!flex"></div>
<!-- v4 --> <div class="flex!"></div>

<!-- Variant stacking (now left-to-right) -->
<!-- v3 --> <ul class="first:*:pt-0 last:*:pb-0">
<!-- v4 --> <ul class="*:first:pt-0 *:last:pb-0">

<!-- Grid arbitrary values (commas -> underscores) -->
<!-- v3 --> <div class="grid-cols-[max-content,auto]"></div>
<!-- v4 --> <div class="grid-cols-[max-content_auto]"></div>

<!-- Gradient rename -->
<!-- v3 --> <div class="bg-gradient-to-r"></div>
<!-- v4 --> <div class="bg-linear-to-r"></div>
```

### Custom Utilities Migration

```css
/* v3 -- @layer utilities */
@layer utilities {
  .tab-4 {
    tab-size: 4;
  }
}

/* v4 -- @utility directive */
@utility tab-4 {
  tab-size: 4;
}
```
