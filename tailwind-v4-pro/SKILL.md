---
name: tailwind-v4-pro
description: "Tailwind CSS v4 for Next.js 16. @theme tokens, v3 migration, dark mode, PostCSS setup, design system patterns, 20 documented errors. Triggers: tailwind, tailwind v4, css, @theme, design tokens, dark mode, postcss, styling, tw classes."
---

# Tailwind V4 Pro -- Styling for Next.js 16

## When to Use

Trigger on any mention of: tailwind, tailwind v4, css styling, @theme, design tokens, dark mode, postcss, tailwind classes, tailwind migration, css variables, color system, responsive design.

## Reference Files

| File | Description |
|------|-------------|
| `references/setup.md` | Version compatibility (stack, browser support, removed features, build perf) + PostCSS config, CSS entry point, layers, package deps, content detection |
| `references/migration-v3-v4.md` | Automated upgrade tool, renamed/removed utilities, default behavior changes, syntax changes, restoring v3 defaults, custom utilities migration |
| `references/design-tokens.md` | @theme directive (bare/inline/static), 17 namespace reference, extending vs replacing, animations with keyframes, sharing tokens across projects |
| `references/color-system.md` | Opacity modifiers (slash syntax), color-mix(), custom color palette, arbitrary values, OKLch palette |
| `references/typography.md` | Font registration, Vietnamese text support (diacriticals, subset), text size customization, responsive typography |
| `references/dark-mode.md` | System preference, class-based toggle, data attribute strategy, three-way toggle (light/dark/system), CSS variable approach, @variant directive |
| `references/components.md` | Button (primary/secondary/ghost), Card, Input, Badge (Pro/Free/Status), Sidebar navigation -- all CViet patterns |
| `references/vscode.md` | IntelliSense extension, activation for v4, settings (classRegex for clsx/cn), NODE_ENV fix, restart procedure, file associations |
| `references/errors.md` | 20 errors (TW-001 through TW-020) with exact messages, causes, and fixes |
| `references/performance.md` | Tree shaking, content auto-detection, spacing scale (single variable), dynamic utility values, production build, anti-patterns |
| `references/cviet-design-system.md` | Current globals.css, design token mapping table, spacing system, border radius, shadow scale, standard layout/form/card/flex patterns, interaction patterns |
| `references/directives.md` | All 13 directives (@import, @theme, @utility, @variant, @custom-variant, @layer, @apply, @source, @reference, @config, @plugin) + 3 functions (--alpha, --spacing, theme) + using vars in CSS/JS |
| `references/new-utilities.md` | Container queries, 3D transforms, gradient angles, stacked shadows, field-sizing, color-scheme, not-*/in-*/nth-* variants, @starting-style, dynamic data attributes, sources list |

## Error Quick Lookup

| ID | Error | Fix |
|----|-------|-----|
| TW-001 | PostCSS plugin not found | Use `@tailwindcss/postcss` (not `tailwindcss`) |
| TW-002 | `@tailwind` directive deprecated | Replace with `@import "tailwindcss"` |
| TW-003 | No styles in development | `cross-env NODE_ENV=development next dev --webpack` |
| TW-004 | Duplicate PostCSS config | Delete `.js`, keep ONLY `.mjs` |
| TW-005 | Google Fonts @import ignored | Must be BEFORE `@import "tailwindcss"` |
| TW-006 | Custom classes not generating | Use `@theme` not `:root` for utility generation |
| TW-007 | `shadow-sm` not working | Renamed: use `shadow-xs` (v4 scale shift) |
| TW-008 | `outline-none` not working | Use `outline-hidden` for v3 behavior |
| TW-009 | Ring width too thin | `ring` is now 1px; use `ring-3` for v3 behavior |
| TW-010 | Border color unexpected | Default changed to `currentColor`; specify explicitly |
| TW-011 | Dark mode not toggling | Use `@custom-variant dark (&:where(.dark, .dark *))` |
| TW-012 | Hover not working on mobile | v4 guards with `@media (hover: hover)` |
| TW-013 | `@layer utilities` ignored | Use `@utility` directive instead |
| TW-014 | `@apply` fails in scoped styles | Use `@reference "../../app.css"` |
| TW-015 | `tailwind.config.js` ignored | Use `@config` or migrate to `@theme` |
| TW-016 | Button cursor:default | Add `cursor-pointer` explicitly |
| TW-017 | Webpack HMR not detecting changes | Use `--webpack` flag + `NODE_ENV=development` |
| TW-018 | `@theme` inside media query fails | `@theme` must be top-level; use `:root` for scoped vars |
| TW-019 | Sass/Less conflicts | Remove Sass/Less; Tailwind v4 IS your preprocessor |
| TW-020 | Content detection missing files | Add `@source` directives for non-auto-detected paths |

## MANDATORY: Canonical Token Classes

**NEVER write arbitrary hex classes when a `@theme` token exists.** Always use canonical names:

| Hex | Token Class |
|-----|-------------|
| `#1B4FD8` | `brand` (bg-brand, text-brand, border-brand) |
| `#1440A8` | `brand-dark` |
| `#0F172A` | `text` (text-text, bg-text) |
| `#64748B` | `muted` (text-muted) |
| `#E2E8F0` | `border` (border-border) |
| `#FAFAF8` | `background` (bg-background) |
| `#10B981` | `success` (bg-success, text-success) |
| `#0EA5E9` | `accent` (bg-accent) |

Opacity: `bg-brand/10` not `bg-[#1B4FD8]/10`. Exception: react-pdf StyleSheet (inline CSS, not Tailwind).

## Key Patterns

### PostCSS Config (Required)
```js
// postcss.config.mjs -- MUST be .mjs, not .js
export default { plugins: { "@tailwindcss/postcss": {} } }
```

### CSS Entry Point
```css
/* globals.css -- @import order matters! */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import "tailwindcss";

@theme inline {
  --color-brand: #1B4FD8;
  --color-accent: #0EA5E9;
  --color-surface: #FFFFFF;
  --color-background: #FAFAF8;
  --font-sans: 'Inter', system-ui, sans-serif;
}
```

### Dev Script (VSCode Fix)
```json
{ "scripts": { "dev": "cross-env NODE_ENV=development next dev --webpack" } }
```
