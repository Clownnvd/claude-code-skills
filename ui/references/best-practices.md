# Best Practices for UI Development

## Design Tokens

### Do
- Extract ALL colors from `globals.css` CSS variables — never hardcode hex/rgb
- Use semantic tokens (`bg-primary`, `text-muted-foreground`) over primitive tokens (`bg-red-600`)
- Use Tailwind CSS 4 syntax: `bg-linear-to-r` not `bg-gradient-to-r`
- Define spacing scale in CSS variables, reference via Tailwind classes
- Use `cn()` from `src/utils/cn.ts` for conditional class merging

### Don't
- Don't hardcode colors: `text-[#FF0000]` — use `text-primary`
- Don't mix design systems: pick one token source (globals.css) and commit
- Don't use inline styles for anything achievable with Tailwind classes
- Don't create one-off spacing values: `p-[13px]` — use the scale (`p-3`, `p-4`)

## Visual Hierarchy

### Do
- Use 3 levels of heading size minimum (hero > section > card)
- Create emphasis with font-weight AND size together (not just bold)
- Use color sparingly for emphasis — primary color on CTAs and key elements only
- Maintain consistent card elevation (shadow-sm → shadow-md → shadow-lg)
- Add whitespace between sections (py-16 to py-24 for landing sections)

### Don't
- Don't make everything bold — if everything is emphasized, nothing is
- Don't use more than 3 font sizes per section
- Don't center-align body text longer than 2 lines
- Don't use colored backgrounds on more than 30% of page area

## Typography

### Do
- Limit to 2 fonts maximum (1 heading + 1 body)
- Use relative units for font sizes (`text-sm`, `text-base`, `text-lg`)
- Set line-height: 1.5-1.75 for body text, 1.1-1.3 for headings
- Max line width: 65-75 characters for readability (`max-w-prose` or `max-w-2xl`)

### Don't
- Don't use font-size below 14px for body text (accessibility)
- Don't mix font families within the same hierarchy level
- Don't use ALL CAPS for more than 3 words (except acronyms)

## Color & Theme

### Do
- Support both light and dark modes — test both
- Use sufficient contrast ratios: 4.5:1 for body text, 3:1 for large text (WCAG AA)
- Use primary color for interactive elements (buttons, links, focus rings)
- Use muted/secondary colors for supporting content
- Use success/warning/destructive semantic colors for status

### Don't
- Don't use pure black (#000) on pure white (#FFF) — use zinc-950 on white
- Don't rely on color alone to convey information (add icons/labels)
- Don't use more than 4 distinct colors per page (excluding grays)
- Don't use low-contrast placeholder text (`placeholder:text-muted-foreground/50`)

## Responsiveness

### Do
- Design mobile-first, enhance for larger screens
- Use CSS Grid + Flexbox (not absolute positioning for layout)
- Test at 375px (mobile), 768px (tablet), 1024px (laptop), 1440px (desktop)
- Use `container mx-auto` for max-width content areas
- Hide non-essential elements on mobile with `hidden sm:block`

### Don't
- Don't use fixed widths (`w-[500px]`) — use responsive utilities (`w-full sm:w-1/2`)
- Don't let text overflow containers — use `truncate` or `line-clamp-*`
- Don't use horizontal scroll on mobile for primary content
- Don't make touch targets smaller than 44x44px

## Accessibility

### Do
- Use semantic HTML: `<main>`, `<nav>`, `<section>`, `<article>`, `<button>`
- Add `aria-label` to icon-only buttons and links
- Ensure keyboard navigation works for all interactive elements
- Add `role="status"` or `aria-live="polite"` for dynamic content updates
- Respect `prefers-reduced-motion` — wrap animations in media query

### Don't
- Don't use `<div onClick>` — use `<button>` for clickable elements
- Don't remove focus outlines without providing alternative focus indicators
- Don't auto-play animations without respecting reduced-motion preference
- Don't use `tabindex > 0` — it breaks natural tab order

## Performance

### Do
- Use Next.js `<Image>` component with width/height for all images
- Lazy load below-fold components with `dynamic(() => import(...))`
- Use Server Components by default — add `'use client'` only when needed
- Minimize JavaScript bundle: check with build analyzer
- Use CSS animations (transform, opacity) over JS animations — GPU accelerated

### Don't
- Don't import entire icon libraries — import individual icons
- Don't use `useEffect` for data fetching — use Server Components or `useSuspenseQuery`
- Don't render hidden content (use conditional rendering, not `display: none`)
- Don't add `'use client'` to components that don't need interactivity

## Content & Copy

### Do
- Write action-oriented CTA text: "Get Started" > "Submit", "Buy Now — $99" > "Purchase"
- Use specific social proof: "Trusted by 100+ developers" > "Trusted by many"
- Keep headlines under 10 words
- Use benefit-driven language: "Save 200+ hours" > "Built with modern tools"

### Don't
- Don't use placeholder text ("Lorem ipsum") in production
- Don't write CTAs that don't tell users what happens next
- Don't use jargon that your target audience won't understand
- Don't hide the price — transparency builds trust

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Hardcoded colors | Theme switch looks broken | Replace with CSS variable tokens |
| Missing dark mode | White flash or unreadable text | Test both modes, use `dark:` prefix |
| Text overflow on mobile | Horizontal scroll, cut-off text | `truncate`, `break-words`, responsive text size |
| No focus indicators | Can't navigate with keyboard | `focus-visible:ring-2 focus-visible:ring-primary` |
| Giant images | Slow LCP, layout shift | `next/image` with explicit dimensions |
| Inconsistent spacing | Sections feel random | Systematic scale (8px increments) |
| Too many animations | Feels chaotic/AI-generated | Max 2-3 animation types per page |
| No loading states | Blank screen during fetch | Skeleton loaders, Suspense boundaries |

## Anti-AI Patterns

Signs that UI looks "AI-generated" rather than professionally designed:

| Red Flag | Fix |
|----------|-----|
| Every section has a different visual style | Pick 1-2 card styles, reuse consistently |
| Excessive gradients everywhere | Reserve gradient for 1-2 hero elements |
| Generic stock-photo aesthetics | Use icons, illustrations, or real screenshots |
| Perfect symmetry on everything | Add intentional asymmetry (offset grids, varied sizes) |
| Rainbow of colors | Restrict to primary + 1 accent + neutrals |
| Every element animated | Animate entry only, not hover on everything |

## Pre-Ship Checklist

- [ ] All text uses design tokens from `globals.css` (no hardcoded colors)
- [ ] Dark mode works correctly on all sections
- [ ] Mobile responsive (tested at 375px)
- [ ] Keyboard navigation works (Tab through all interactive elements)
- [ ] Images use `next/image` with proper dimensions
- [ ] No `console.log` in components
- [ ] CTA buttons have clear, action-oriented text
- [ ] Loading/error states exist for async content
- [ ] `prefers-reduced-motion` respected for animations
- [ ] Score >= target (B for production, A- for premium)
