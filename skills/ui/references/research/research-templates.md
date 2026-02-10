# Research Templates

## Design Brief Template (Pipeline Handoff Contract)

This is the **exact output format** for ui-research. The next pipeline stage (build or scoring) consumes this contract.

```markdown
## Design Brief: [Page Name]

### Direction
- **Vibe**: [professional / minimal / bold / luxury]
- **Layout**: [described structure — e.g., "full-width hero, 3-col features, centered pricing"]
- **Primary color**: [CSS variable + value, e.g., `var(--primary)` — `oklch(0.637 0.237 25.331)`]
- **Inspiration sources**: [3+ URLs with 1-line notes]

### Component Plan
| Component | Pattern | Source |
|-----------|---------|--------|
| Hero | [e.g., text-left + image-right, dual CTAs] | [URL] |
| Features | [e.g., bento grid, 3-col with icons] | [URL] |
| Pricing | [e.g., single card, gradient border] | [URL] |
| ... | ... | ... |

### Design Tokens (from project theme)
| Token | Variable | Value |
|-------|----------|-------|
| Primary | `var(--primary)` | [oklch/hsl value] |
| Accent | `var(--accent)` | [oklch/hsl value] |
| Font | `var(--font-sans)` | [font stack] |
| Weights | — | [400, 500, 600, 700] |
| Radius | `var(--radius)` | [value] |
| Gradients | `bg-gradient-primary` | [from → to] |
| Utilities | `card-hover`, `shine-effect` | [list available] |

### Anti-Patterns to Avoid
- [Specific item from anti-ai-patterns.md] — [why]
- [Specific item] — [why]

### Technical Plan
- **Components needed**: [list of new/modified files]
- **Animation approach**: [CSS utilities / IntersectionObserver / Framer]
- **Responsive strategy**: [mobile-first, breakpoints used]
- **Dark mode**: [CSS variables / class strategy]
```

### Validation checklist
- [ ] 3+ inspiration URLs included
- [ ] All colors reference CSS variables (no hardcoded hex/oklch)
- [ ] Component plan table has at least 3 rows
- [ ] Design tokens extracted from `globals.css`
- [ ] Anti-patterns section has 2+ items
- [ ] No placeholder/TODO text remaining

## Quick Comparison Template

```markdown
## [Component] — Pattern Comparison

| Aspect | Site A | Site B | Site C | Our Choice |
|--------|--------|--------|--------|------------|
| Layout | | | | |
| Colors | | | | |
| Typography | | | | |
| Animation | | | | |
| Mobile | | | | |
```

## Competitive Audit Template

```markdown
## Competitive Audit: [Product Category]

### Competitors Analyzed
1. **[Name]** ([url]) — [positioning]
2. **[Name]** ([url]) — [positioning]
3. **[Name]** ([url]) — [positioning]

### Visual Positioning Map
- Premium ←→ Budget
- Minimal ←→ Feature-rich
- Technical ←→ Non-technical

### Differentiators
- What they ALL do: [common patterns]
- What NONE do: [opportunity gaps]
- What ONE does uniquely: [standout moves]

### Our Position
- [Where we fit and why]
```
