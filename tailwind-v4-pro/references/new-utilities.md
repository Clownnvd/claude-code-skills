# New Utilities in v4

> Container queries, 3D transforms, gradient angles, stacked shadows, field sizing, and new variants

---

## Container Queries (Built-In, No Plugin)

```html
<div class="@container">
  <div class="grid grid-cols-1 @sm:grid-cols-2 @lg:grid-cols-4">
    ...
  </div>
</div>

<!-- Max-width container queries -->
<div class="@container">
  <div class="@max-md:hidden">Only visible in wider containers</div>
</div>
```

## 3D Transforms

```html
<div class="perspective-distant">
  <div class="rotate-x-12 rotate-y-6 transform-3d">
    3D transformed card
  </div>
</div>
```

## Gradient Angles

```html
<!-- Arbitrary angle -->
<div class="bg-linear-45 from-brand to-accent"></div>

<!-- Color interpolation -->
<div class="bg-linear-to-r/oklch from-brand to-accent"></div>

<!-- Conic gradient -->
<div class="bg-conic from-red-500 to-blue-500"></div>

<!-- Radial gradient -->
<div class="bg-radial-[at_25%_25%] from-white to-gray-900"></div>
```

## Stacked Shadows (Up to 4 Layers)

```html
<div class="shadow-md inset-shadow-xs ring-1 ring-black/5 inset-ring-1 inset-ring-white/10">
  Element with 4 shadow layers
</div>
```

## Field Sizing (Auto-Resize Textarea)

```html
<textarea class="field-sizing-content" placeholder="Type here..."></textarea>
```

## Color Scheme (Dark Mode Scrollbars)

```html
<html class="dark color-scheme-dark">
  <!-- Browser chrome (scrollbars, form controls) matches dark mode -->
</html>
```

## not-* Variant

```html
<div class="not-hover:opacity-75">Transparent when NOT hovered</div>
<div class="not-last:border-b">Border on all but last</div>
```

## in-* Variant (Group-like Without group Class)

```html
<div class="hover:text-blue-500">
  <span class="in-hover:underline">Underlines when parent is hovered</span>
</div>
```

## nth-* Variants

```html
<ul>
  <li class="nth-odd:bg-gray-50">Striped rows</li>
  <li class="nth-3:font-bold">Every 3rd item bold</li>
</ul>
```

## @starting-style (Enter Animations)

```html
<div popover class="transition-discrete starting:open:opacity-0 open:opacity-100">
  Animates in when opened
</div>
```

## Dynamic Data Attributes

```html
<div data-active class="opacity-50 data-active:opacity-100">
  No configuration needed for data-* variants
</div>
```

---

## Sources

- [Tailwind CSS v4.0 Blog Post](https://tailwindcss.com/blog/tailwindcss-v4)
- [Tailwind CSS Upgrade Guide](https://tailwindcss.com/docs/upgrade-guide)
- [Tailwind CSS Theme Variables](https://tailwindcss.com/docs/theme)
- [Tailwind CSS Dark Mode](https://tailwindcss.com/docs/dark-mode)
- [Tailwind CSS Functions and Directives](https://tailwindcss.com/docs/functions-and-directives)
- [Tailwind CSS Next.js Installation](https://tailwindcss.com/docs/installation/framework-guides/nextjs)
- [Tailwind CSS PostCSS Installation](https://tailwindcss.com/docs/installation/using-postcss)
- [Tailwind CSS Adding Custom Styles](https://tailwindcss.com/docs/adding-custom-styles)
- [Tailwind CSS v4 2026 Migration Best Practices](https://www.digitalapplied.com/blog/tailwind-css-v4-2026-migration-best-practices)
- [Tailwind CSS v4 Complete Guide 2026](https://devtoolbox.dedyn.io/blog/tailwind-css-v4-complete-guide)
- [VSCode IntelliSense Fix for Tailwind v4](https://dev.to/mrpaulishaili/vscode-intellisense-broken-in-tailwind-css-v4-heres-the-solution-4d5)
- [Dark Mode with Tailwind v4 and Next.js](https://www.thingsaboutweb.dev/en/posts/dark-mode-with-tailwind-v4-nextjs)
- [Tailwind CSS v4 Performance](https://medium.com/@mernstackdevbykevin/tailwind-css-v4-0-performance-boosts-build-times-jit-more-abf6b75e37bd)
- [GitHub: Tailwind v4 Webpack HMR Issue](https://github.com/tailwindlabs/tailwindcss/discussions/18179)
- [GitHub: Upgrading Dark Mode Discussion](https://github.com/tailwindlabs/tailwindcss/discussions/16517)
