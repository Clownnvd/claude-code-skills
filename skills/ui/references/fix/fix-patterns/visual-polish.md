# Fix Patterns: Visual Polish

## Typography Variation

### Section heading monotony
```tsx
// Before: all sections identical
<h2 className="text-3xl font-bold sm:text-4xl">

// After: primary vs secondary sections
// Primary (Features, Pricing, Hero): larger
<h2 className="text-3xl font-bold sm:text-4xl lg:text-5xl">

// Secondary (FAQ, How It Works): slightly smaller
<h2 className="text-2xl font-bold sm:text-3xl">
```

### Fluid typography with clamp()
```css
/* Hero heading: 30px → 72px */
font-size: clamp(1.875rem, 4vw + 1rem, 4.5rem);

/* Section heading primary: 24px → 48px */
font-size: clamp(1.5rem, 3vw + 0.5rem, 3rem);

/* Section heading secondary: 20px → 36px */
font-size: clamp(1.25rem, 2.5vw + 0.5rem, 2.25rem);
```

## Visual Hierarchy Fixes

### Competing elements
- Ensure single dominant element per viewport
- Use size + color weight + position to establish rank
- Rule: largest + brightest + top = most important

### Z-pattern / F-pattern scanning
```
Hero:     [Badge]
          [Headline]                    [Image/Visual]
          [Subheadline]
          [CTA Primary] [CTA Secondary]
          [Social proof]
```

### Whitespace as hierarchy signal
```tsx
// Primary sections: generous spacing
className="py-24 sm:py-32"

// Secondary sections: standard spacing
className="py-16 sm:py-24"

// Tight grouping within sections (related items)
className="mt-4"  // close = related
className="mt-12" // far = separate group
```

## Spacing Consistency

### Common spacing scale (Tailwind defaults)
| Token | px | Use |
|-------|-----|-----|
| `gap-1` | 4px | Icon + label |
| `gap-2` | 8px | Related items |
| `gap-4` | 16px | Card padding, list items |
| `gap-6` | 24px | Grid gaps |
| `gap-8` | 32px | Section sub-groups |
| `gap-12` | 48px | Between content blocks |
| `py-24` | 96px | Section padding |

### Inconsistent padding fix
```tsx
// Audit: check all section py values
// All primary sections should use same py
// Exception: hero (can be larger) and CTA (can be smaller)

// Standard: py-24 for all content sections
// Hero: py-16 sm:py-24 (or custom)
// Final CTA: py-24 (matches others)
```

## Color System Fixes

### Hardcoded colors → tokens
```tsx
// Before
className="text-zinc-500"
className="bg-red-600"

// After: use design tokens
className="text-muted-foreground"
className="bg-primary"
```

### Dark mode misses
```tsx
// Check: does element look correct in both modes?
// Common miss: hardcoded opacity that doesn't work in dark
className="bg-black/5"   // invisible in dark mode!
className="bg-foreground/5" // works in both modes ✓
```

### Accent usage discipline
- Primary/accent color ONLY on: CTAs, active states, key highlights
- Never on: body text, backgrounds (except subtle tints), decorative elements
- Secondary actions: `text-muted-foreground` not `text-primary`

## Social Proof Polish

### Vague numbers → specific
```tsx
// Before
"Trusted by 100+ developers"

// After: specific or growing
"Trusted by 127 developers"
"Join 2,400+ developers"
```

### Generic avatars → real
```tsx
// Before: initials
<div className="bg-primary/10 text-primary">MT</div>

// After: real photo or Gravatar
<Image src="/testimonials/minh.jpg" alt="Minh T." width={40} height={40} className="rounded-full" />
```

### Testimonial credibility
```tsx
// Minimum: name + role + company
// Better: name + photo + role + company + specific result
{
  name: "Sarah Chen",
  role: "CTO",
  company: "Acme Inc",
  photo: "/testimonials/sarah.jpg",
  quote: "Saved our team 3 weeks of setup. Paid for itself on day 1.",
}
```

## Shadow & Depth

Use existing shadow scale from `globals.css`: `shadow-subtle` → `shadow-card` → `shadow-elevated` → `shadow-floating` → `shadow-dramatic`. Never invent new shadow values.
