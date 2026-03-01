# Color System

> Opacity modifiers, custom palettes, and OKLch colors in Tailwind CSS v4

---

## Opacity Modifiers (Slash Syntax)

v4 uses `color-mix()` under the hood, enabling opacity on ANY color value:

```html
<!-- Static colors with opacity -->
<div class="bg-blue-500/50">    <!-- 50% opacity -->
<div class="text-brand/75">     <!-- 75% opacity -->
<div class="border-black/10">   <!-- 10% opacity -->

<!-- Works with currentColor (NEW in v4!) -->
<div class="bg-current/20">     <!-- currentColor at 20% -->

<!-- Works with CSS variables -->
<div class="bg-(--my-color)/50"> <!-- var(--my-color) at 50% -->
```

Generated CSS:
```css
.bg-blue-500\/50 {
  background-color: color-mix(in oklab, var(--color-blue-500) 50%, transparent);
}
```

## Custom Color Palette

```css
@theme inline {
  /* CViet brand colors */
  --color-background: #FAFAF8;
  --color-surface: #FFFFFF;
  --color-brand: #1B4FD8;
  --color-brand-dark: #1440A8;
  --color-accent: #0EA5E9;
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-text: #0F172A;
  --color-muted: #64748B;
  --color-border: #E2E8F0;
}
```

Usage:
```html
<div class="bg-background text-text border-border">
  <button class="bg-brand text-white hover:bg-brand-dark">
    CTA Button
  </button>
  <span class="text-muted">Helper text</span>
  <span class="text-success">Pro badge</span>
</div>
```

## Arbitrary Color Values

```html
<!-- Hex -->
<div class="bg-[#1B4FD8]"></div>

<!-- RGB -->
<div class="bg-[rgb(27,79,216)]"></div>

<!-- OKLch (v4 native) -->
<div class="bg-[oklch(0.496_0.214_259)]"></div>

<!-- With opacity -->
<div class="bg-[#1B4FD8]/50"></div>
```

## OKLch Color Palette (v4 Default)

v4 moved the default palette from RGB to OKLch for wider gamut and more perceptually uniform colors:

```css
/* v3 (RGB) */
--color-blue-500: #3b82f6;

/* v4 (OKLch -- wider gamut, more vivid) */
--color-blue-500: oklch(0.623 0.214 259.815);
```
