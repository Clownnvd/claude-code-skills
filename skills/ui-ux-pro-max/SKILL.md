---
name: ui-ux-pro-max
description: "UI/UX design intelligence with 67 styles, 96 palettes, 57 font pairings. Generate design systems, search domains, get stack-specific guidelines."
---

# UI/UX Pro Max - Design Intelligence

Comprehensive design guide for web and mobile applications. Contains 67 styles, 96 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 13 technology stacks.

## When to Apply

Reference these guidelines when:
- Designing new UI components or pages
- Choosing color palettes and typography
- Reviewing code for UX issues
- Building landing pages or dashboards
- Implementing accessibility requirements

## Rule Categories by Priority

| Priority | Category | Impact | Domain |
|----------|----------|--------|--------|
| 1 | Accessibility | CRITICAL | `ux` |
| 2 | Touch & Interaction | CRITICAL | `ux` |
| 3 | Performance | HIGH | `ux` |
| 4 | Layout & Responsive | HIGH | `ux` |
| 5 | Typography & Color | MEDIUM | `typography`, `color` |
| 6 | Animation | MEDIUM | `ux` |
| 7 | Style Selection | MEDIUM | `style`, `product` |
| 8 | Charts & Data | LOW | `chart` |

## Quick Reference

### Accessibility (CRITICAL)
- `color-contrast` — Minimum 4.5:1 ratio for normal text
- `focus-states` — Visible focus rings on interactive elements
- `alt-text` — Descriptive alt text for meaningful images
- `aria-labels` — aria-label for icon-only buttons
- `keyboard-nav` — Tab order matches visual order

### Touch & Interaction (CRITICAL)
- `touch-target-size` — Minimum 44x44px touch targets
- `hover-vs-tap` — Use click/tap for primary interactions
- `loading-buttons` — Disable button during async operations
- `error-feedback` — Clear error messages near problem

### Performance (HIGH)
- `image-optimization` — Use WebP, srcset, lazy loading
- `reduced-motion` — Check prefers-reduced-motion
- `content-jumping` — Reserve space for async content

### Layout & Responsive (HIGH)
- `viewport-meta` — width=device-width initial-scale=1
- `readable-font-size` — Minimum 16px body text on mobile
- `z-index-management` — Define z-index scale (10, 20, 30, 50)

### Typography & Color (MEDIUM)
- `line-height` — Use 1.5-1.75 for body text
- `line-length` — Limit to 65-75 characters per line
- `font-pairing` — Match heading/body font personalities

## How to Use

### Generate Design System (REQUIRED first step)

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

### Search by Domain

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

### Get Stack Guidelines

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack <stack_name>
```

### Persist Design System

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

## Detailed References

- `references/workflow-guide.md` — Full 4-step workflow, design system persistence, example
- `references/search-reference.md` — All domains, stacks, output formats, prerequisites, tips
- `references/professional-ui-rules.md` — Common UI mistakes, contrast rules, pre-delivery checklist
