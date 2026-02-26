# Design Tokens

## Color System

| Role | Class | Hex |
|------|-------|-----|
| Page background | `bg-[#F9F6F0]` / `bg-cream` | `#F9F6F0` warm cream |
| Card / Input | `bg-white` | `#FFFFFF` |
| Brand (coral) | `bg-[#C96A4A]` / `bg-brand` | `#C96A4A` |
| Brand hover | `hover:bg-[#B05A3C]` | `#B05A3C` |
| Text primary | `text-gray-900` | `#0F0F0F` |
| Text muted | `text-[#6B6B6B]` | `#6B6B6B` |
| Border | `border-[#E0E0E0]` | `#E0E0E0` |
| CTA button | `bg-black text-white` | `#000000` |
| Upgrade badge | `bg-[#E8F4F8] text-[#3B82A0]` | teal |
| Input focus ring | `focus:ring-2 focus:ring-[#C96A4A]/30` | coral/30 |
| Active nav | `bg-black/8` | valid Tailwind v4 |

## Typography

```
Headings:  Georgia, 'Times New Roman', serif
           → apply inline: style={{ fontFamily: "Georgia,'Times New Roman',serif" }}
Body:      system-ui sans-serif (globals.css body)
Code:      font-mono
```

## Tailwind v4 Tokens (globals.css @theme inline)

```css
--color-cream: #F9F6F0;
--color-brand: #C96A4A;
--color-brand-hover: #B05A3C;
--color-surface: #FFFFFF;
--color-text-primary: #0F0F0F;
--color-text-muted: #6B6B6B;
--color-border: #E0E0E0;
```

Both `bg-[#F9F6F0]` and `bg-cream` compile correctly. IDE may warn to prefer tokens — both work.

## Sizing / Spacing Conventions

| Element | Value |
|---------|-------|
| Sidebar collapsed | `w-12` (48px) |
| Sidebar expanded | `w-64` (256px) |
| Avatar (sidebar bottom) | `w-8 h-8 rounded-full` |
| Avatar (messages) | `w-7 h-7 rounded-full` |
| Min touch target | `44×44px` |
| Chat max-width | `max-w-2xl mx-auto` |
| Input border radius | `rounded-xl` |
| Modal panel | `rounded-2xl` |
| Pill buttons | `rounded-full` |
| Nav item border radius | `rounded-lg` |

## Transition Convention

All interactive elements: `transition-colors duration-200`

## Common Class Patterns

```tsx
// Active nav item
"bg-black/8 text-gray-900 font-medium"

// Inactive nav item
"text-[#6B6B6B] hover:bg-black/5 hover:text-gray-900 transition-colors duration-200"

// Section header (sidebar)
"text-xs font-medium text-[#6B6B6B] mb-1 px-2 py-1"

// Modal overlay
"fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"

// Modal panel (default)
"bg-white rounded-2xl p-6 max-w-sm w-full shadow-xl"

// Pill filter (active)
"bg-gray-900 text-white rounded-full px-4 py-1.5 text-sm"

// Pill filter (inactive)
"border border-[#E0E0E0] text-[#6B6B6B] rounded-full px-4 py-1.5 text-sm hover:border-gray-400"
```
