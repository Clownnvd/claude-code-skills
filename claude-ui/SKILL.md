---
name: claude-ui
description: "Full Claude.ai UI clone: Next.js 16 + Tailwind v4. Exact tokens, all 19 flows, sidebar, chat input, messages, settings, login, onboarding, billing, artifacts. PageFlows July 2025."
---

# Claude UI — Implementation Index

Source: PageFlows (July 2025 — 19 flows, 100+ screenshots).
Project: `c:\nextjs_project\pulse-analytics` → renamed to `claude-ui` on GitHub.

---

## Design Tokens (Quick Reference)

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#F9F6F0` | Page bg — warm cream, NOT white |
| Surface | `#FFFFFF` | Cards, modals, chat bubbles |
| Brand accent | `#C96A4A` | Logo, send btn, New Chat dot |
| Text primary | `#0F0F0F` | Body text |
| Text muted | `#6B6B6B` | Secondary text, placeholders |
| Border | `#E0E0E0` | All borders, dividers |
| Active nav | `bg-black/8` | Sidebar active item (valid Tailwind v4) |
| CTA | `bg-black text-white` | Primary buttons |
| Heading font | `Georgia,'Times New Roman',serif` | h1 headings only |
| Body font | `system-ui, sans-serif` | Everything else |

---

## Critical Rules (Frequent Mistakes)

| Bug | Correct |
|-----|---------|
| User messages right-aligned (`flex justify-end`) | LEFT-aligned — `flex items-start gap-3` |
| Sidebar has Anthropic logo / settings gear | NO logo, NO gear — only [≡][+][💬][📁][⊞][ST] |
| "New chat" is a full-width button | It's a **nav item row** (coral dot + text) |
| Projects badge is blue | Teal — `bg-[#E8F4F8] text-[#3B82A0]` |
| Response toolbar shows on hover | ALWAYS visible (no hover-only) |
| StyleIcon is a bolt/lightning bolt | 3 sliders SVG: `d="M8 6h13M8 12h9m-9 6h5"` |
| `window.location.href` for navigation | Use `<Link href>` or `router.push()` |
| `border-t border-gray-50` (invisible) | Use `border-[#E0E0E0]` |
| AnthropicMark duplicated in files | Extract to `src/components/icons.tsx` |
| `bg-black/8` IDE warning | Valid in Tailwind v4 — compiles correctly |

---

## App Shell Structure

```tsx
<div className="flex h-screen bg-[#F9F6F0]">
  <Sidebar />          {/* w-12 collapsed / w-64 expanded */}
  <main className="flex-1 flex flex-col overflow-hidden">
    {/* page content */}
  </main>
</div>
```

## Project Structure

```
src/app/
  page.tsx                  # Login (split layout)
  layout.tsx                # Root layout
  (chat)/
    layout.tsx              # App shell (sidebar + main)
    new/page.tsx            # Home / chat
    recents/page.tsx        # Chat history
    settings/page.tsx       # Settings tabs
    artifacts/page.tsx      # Artifacts list + split view
    upgrade/page.tsx        # Billing / plan cards
  (onboarding)/             # 5-screen onboarding flow
src/components/
  sidebar.tsx               # Collapsible sidebar + account menu
  chat-input.tsx            # Textarea + toolbar + dropdowns
```

---

## Reference Directory

### Design System
- `references/design-tokens.md` — Full token table, Tailwind v4 @theme, sizing conventions
- `references/flows.md` — All 19 flows table, navigation rules, route map

### Components
- `references/components/sidebar.md` — Collapsed/expanded states, account menu popup
- `references/components/chat-input.md` — Toolbar buttons, StyleIcon SVG, dropdowns, props
- `references/components/messages.md` — UserMessage (LEFT), AssistantMessage, ResponseToolbar, AnthropicMark
- `references/components/modals.md` — Rename, Share, Feedback, Delete, DeleteAccount

### Pages
- `references/pages/home.md` — Empty state hero, conversation view, topbar, upgrade banner
- `references/pages/recents.md` — Chat card (no preview text), select mode toolbar
- `references/pages/settings.md` — 6 tabs, Profile fields, Appearance picker, ToggleSwitch
- `references/pages/login.md` — Split layout, 5-screen onboarding flow
- `references/pages/billing.md` — Plan cards (Free/Pro/Max), tab toggle, billing toggle
- `references/pages/artifacts.md` — List page, category pills, card grid, split view

---

## Accessibility Checklist

- [ ] Icon buttons → `aria-label`
- [ ] SVG icons → `aria-hidden="true"`
- [ ] Toggle switches → `role="switch"` + `aria-checked`
- [ ] Form inputs → `<label htmlFor>` or `aria-label`
- [ ] Focus ring → `outline: 2px solid #C96A4A` in globals.css
- [ ] Min touch target → 44×44px

## Tailwind v4 Notes

- `@import "tailwindcss"` replaces old `@tailwind base/components/utilities`
- `@theme inline` in globals.css defines custom utility classes
- `bg-black/8` = valid arbitrary opacity — IDE warns but compiles correctly
- Custom tokens: `bg-cream`, `bg-brand`, `text-text-muted`, `border-border`
