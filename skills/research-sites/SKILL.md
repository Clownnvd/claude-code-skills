---
name: research-sites
description: Research beautiful UI by page type (landing, dashboard, auth, billing). For each page, find best components with direct links. Present per-page tables for user to pick and implement.
---

# Research Sites

Research beautiful UI components organized by page type. For each page, find the best components from real sites with direct links. Present findings and wait for user selection.

## When to Use

Activate when user asks to research sites, find beautiful components, or explore UI patterns for specific pages.

## Workflow

### 1. Determine Pages

Ask or infer which pages to research. Common pages:
- **Landing**: hero, navbar, features, pricing, testimonials, FAQ, CTA, footer
- **Dashboard**: sidebar, stats cards, charts, tables, activity feed, header
- **Auth**: sign-in, sign-up, forgot password, OTP, social login
- **Billing**: pricing table, checkout, invoices, payment history, plans

If user says "all" or doesn't specify, research all 4 pages.

### 2. Search Per Page (3+ queries each)

For each page, use `WebSearch`:

```
"best [page] [section] component 2026" site:21st.dev
"[page] [section] UI" site:ui.aceternity.com
"[page] [section]" site:magicui.design
"[page] design inspiration" site:godly.website
"[page] section examples" site:originui.com
```

### 3. Fetch & Extract

Use `WebFetch` on promising URLs. For each component extract:
- Component name
- What section of the page it belongs to (hero, sidebar, etc.)
- Visual style
- **Direct link** to the component page
- Complexity (Simple / Medium / Advanced)

### 4. Present Per-Page Tables

For EACH page, output a table with direct links. See `references/output-format.md`.

Example:

```markdown
## Landing Page

| # | Section | Component | Style | Link | Complexity |
|---|---------|-----------|-------|------|------------|
| 1 | Hero | Aurora Background | Animated gradient | [Aceternity](https://ui.aceternity.com/components/aurora-background) | Medium |
| 2 | Hero | Hero Video Dialog | Click-to-expand | [Magic UI](https://magicui.design/docs/components/hero-video-dialog) | Medium |
| 3 | Nav | Floating Dock | macOS dock | [Aceternity](https://ui.aceternity.com/components/floating-dock) | Medium |
```

### 5. Wait for User

After ALL page tables, **STOP and wait**:
> "Pick numbers to implement (e.g. Landing #1, #3 + Dashboard #2), or ask me to search deeper for a specific page."

Do NOT implement until user picks.

### 6. Implement Selected

Fetch source URL → adapt to project stack → build component.

## Key Sources

| Source | URL | Best For |
|--------|-----|----------|
| 21st.dev | 21st.dev | Full page sections, community components |
| Aceternity UI | ui.aceternity.com | Animated effects, backgrounds, cards |
| Magic UI | magicui.design | 150+ animated components |
| Origin UI | originui.com | Clean copy-paste blocks |
| shadcn/ui | ui.shadcn.com | Accessible primitives |
| Godly | godly.website | Landing page layouts |

## Page Breakdown Reference

See `references/page-sections.md` for full section lists per page type.
See `references/trending-2026.md` for current trending components.
See `references/output-format.md` for presentation templates.

## References

- `references/page-sections.md` — Sections per page type with search queries
- `references/site-sources.md` — Full source list with URLs and search patterns
- `references/trending-2026.md` — Current trending components with descriptions
- `references/output-format.md` — Per-page table templates and follow-up prompts
