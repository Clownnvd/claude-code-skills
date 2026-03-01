# CViet Design System Implementation

> Complete design token mapping, spacing, radius, shadow, and standard patterns for CViet

---

## Current globals.css

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import "tailwindcss";

@theme inline {
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
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
}
```

## Design Token Mapping

| Token | CSS Variable | Utility Classes | Usage |
|-------|-------------|----------------|-------|
| Background | `--color-background` | `bg-background` | Page background |
| Surface | `--color-surface` | `bg-surface` | Cards, modals |
| Brand | `--color-brand` | `bg-brand`, `text-brand` | CTAs, links, active states |
| Brand Dark | `--color-brand-dark` | `bg-brand-dark` | Hover state for brand |
| Accent | `--color-accent` | `text-accent`, `bg-accent` | Secondary highlights |
| Success | `--color-success` | `text-success`, `bg-success` | Pro badge, confirmations |
| Warning | `--color-warning` | `text-warning`, `bg-warning` | Alerts |
| Error | `--color-error` | `text-error`, `bg-error` | Form errors, destructive |
| Text | `--color-text` | `text-text` | Primary text |
| Muted | `--color-muted` | `text-muted` | Secondary text, placeholders |
| Border | `--color-border` | `border-border` | Dividers, card borders |

## MANDATORY: Use Canonical Token Classes

**NEVER use arbitrary hex values when a design token exists.** This is a hard rule.

| WRONG (arbitrary hex) | CORRECT (canonical token) |
|---|---|
| `bg-[#1B4FD8]` | `bg-brand` |
| `text-[#1B4FD8]` | `text-brand` |
| `border-[#1B4FD8]` | `border-brand` |
| `hover:bg-[#1440A8]` | `hover:bg-brand-dark` |
| `text-[#0F172A]` | `text-text` |
| `text-[#64748B]` | `text-muted` |
| `border-[#E2E8F0]` | `border-border` |
| `bg-[#FAFAF8]` | `bg-background` |
| `bg-[#10B981]` | `bg-success` |
| `text-[#10B981]` | `text-success` |
| `bg-[#0EA5E9]` | `bg-accent` |

Opacity modifiers use the canonical name too: `bg-brand/10` not `bg-[#1B4FD8]/10`.

**Exception**: PDF templates (`src/lib/pdf/templates/*.tsx`) use react-pdf StyleSheet objects with inline `color: "#..."` values -- those are NOT Tailwind classes and should NOT be changed.

## Spacing System

| Class | Value | Use |
|-------|-------|-----|
| `p-1` | 4px | Tight padding (badges) |
| `p-2` | 8px | Small padding (chips) |
| `p-3` | 12px | Nav items |
| `p-4` | 16px | Standard content |
| `p-6` | 24px | Card padding |
| `p-8` | 32px | Section padding |
| `gap-1` | 4px | Tight grouping |
| `gap-2` | 8px | Related items |
| `gap-3` | 12px | Form fields |
| `gap-4` | 16px | Standard spacing |
| `gap-6` | 24px | Section gap |
| `gap-8` | 32px | Page sections |

## Border Radius

| Class | Value | Use |
|-------|-------|-----|
| `rounded-sm` | 0.125rem (2px) | Subtle rounding |
| `rounded-md` | 0.375rem (6px) | Badges, small elements |
| `rounded-lg` | 0.5rem (8px) | Buttons, inputs |
| `rounded-xl` | 0.75rem (12px) | Cards |
| `rounded-2xl` | 1rem (16px) | Modals |
| `rounded-full` | 9999px | Avatars, pills |

## Shadow Scale

| Class | Use |
|-------|-----|
| `shadow-xs` | Subtle card elevation (was `shadow-sm` in v3) |
| `shadow-sm` | Default card shadow (was `shadow` in v3) |
| `shadow-md` | Dropdowns, popovers |
| `shadow-lg` | Modals |
| `shadow-xl` | Toast notifications |

## Standard Patterns

```html
<!-- Page layout -->
<div class="min-h-screen bg-background">
  <main class="max-w-5xl mx-auto px-4 py-8">
    ...
  </main>
</div>

<!-- Form group -->
<div class="flex flex-col gap-6">
  <div class="flex flex-col gap-1.5">
    <label class="text-sm font-medium text-text">Label</label>
    <input class="w-full px-4 py-3 rounded-lg border border-border bg-surface text-text text-sm focus:border-brand focus:outline-hidden focus:ring-1 focus:ring-brand transition-colors duration-200" />
  </div>
</div>

<!-- Card grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div class="bg-surface rounded-xl border border-border p-6 shadow-xs hover:shadow-sm transition-all duration-200 cursor-pointer">
    ...
  </div>
</div>

<!-- Flex row with spacing (prefer gap over space-*) -->
<div class="flex items-center gap-3">
  <span>Item 1</span>
  <span>Item 2</span>
</div>
```

## Interaction Patterns

```html
<!-- All interactive elements need: -->
<!-- 1. cursor-pointer (v4 buttons default to cursor:default) -->
<!-- 2. hover state with transition -->
<!-- 3. Min touch target 44x44px -->
<!-- 4. focus-visible ring -->

<button class="
  cursor-pointer
  hover:bg-brand-dark
  transition-colors duration-200
  min-h-11 min-w-11
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand
">
```
