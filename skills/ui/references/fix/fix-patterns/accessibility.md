# Fix Patterns: Accessibility & Interactions

## aria-* Attributes

### Missing `aria-expanded` on toggles (FAQ, dropdowns)
```tsx
// Before
<button onClick={() => toggle()}>

// After
<button onClick={() => toggle()} aria-expanded={isOpen}>
```

### Missing `aria-label` on icon-only elements
```tsx
// Before
<div className="flex gap-1">{stars}</div>

// After
<div className="flex gap-1" role="img" aria-label="5 out of 5 stars">{stars}</div>
```

### Decorative SVGs missing `aria-hidden`
```tsx
// Before
<DotPattern className="..." />

// After — inside the SVG component
<svg aria-hidden="true" ...>
```

### Avatar initials without labels
```tsx
// Before
<div className="rounded-full">MT</div>

// After
<div className="rounded-full" aria-label="User MT">MT</div>
```

## Semantic HTML

### Heading hierarchy gaps
- Audit: h1 → h2 → h3 (no skipping h2 to h4)
- Fix: change heading level, adjust styles via className not tag

### Buttons vs links
```tsx
// Navigation → <a> or <Link>
<Link href="/pricing">View pricing</Link>

// Action → <button>
<button onClick={handleSubmit}>Submit</button>
```

## Focus Styles

### Missing focus on custom buttons
```tsx
// Add focus-visible ring
className="... focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
```

### FAQ accordion focus
```tsx
<button
  onClick={() => toggle(index)}
  aria-expanded={openIndex === index}
  className="... focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
>
```

## Keyboard Navigation

### Enter/Space on custom buttons
```tsx
// Usually handled by <button> natively
// Only needed for divs acting as buttons (anti-pattern — use <button> instead)
onKeyDown={(e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    handleClick();
  }
}}
```

### Focus trap in modals
```tsx
// Use Radix Dialog or @headlessui/react — built-in focus trap
// Never implement manually unless required
```

## Color Contrast

### Check with tools
- DevTools: Elements → Accessibility → Contrast ratio
- Target: 4.5:1 normal text, 3:1 large text (≥18pt or 14pt bold)

### Common fixes
```css
/* Too low: text-muted-foreground on light bg */
/* Fix: darken the muted-foreground CSS var */
--muted-foreground: oklch(0.45 0.02 30); /* was 0.48 */
```

## Reduced Motion

### Already handled pattern
```tsx
// ScrollReveal already checks prefers-reduced-motion ✓
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (prefersReducedMotion) { setIsVisible(true); return; }
```

### Marquee / continuous animations
```css
@media (prefers-reduced-motion: reduce) {
  .animate-marquee { animation: none; }
}
```
