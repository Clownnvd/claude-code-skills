# UX & Interactions Criteria

Covers categories 6-7: Interactions & States (8%), Accessibility (10%).

## 6. Interactions & States (8%)

**Quick checklist:**
- [ ] Hover, focus, active, disabled states for all interactive elements
- [ ] Smooth transitions (150-300ms)
- [ ] Loading states (skeleton/spinner)
- [ ] Animations respect prefers-reduced-motion
- [ ] Keyboard navigation works

**What to check:** Hover states (buttons, links, cards), focus states (keyboard focus ring), active/pressed states, disabled states (opacity, cursor), transitions (150-300ms ease), loading states (skeletons/spinners), animations (entrance fade-in/slide-up, respects reduced-motion).

**Scoring:** 9-10: Every element has all states, polished animations | 7-8: Most states present, 1-2 gaps | 5-6: Basic hover but inconsistent, no loading states | 3-4: Many elements no feedback | 0-2: No states at all

**Common issues:** Links styled like text (no hover), `outline: none` without replacement, no skeleton on data components, animations too fast (<100ms) or too slow (>500ms), `transition-all` instead of specific properties.

## 7. Accessibility (10%)

**Quick checklist:**
- [ ] Color contrast >= 4.5:1 (text), >= 3:1 (large text)
- [ ] All images have alt text
- [ ] Form labels present and associated
- [ ] Focus indicators visible
- [ ] Screen reader compatible (semantic HTML, ARIA)

### Color & Contrast
- Text: >= 4.5:1 (WCAG AA), large text (>=18pt or 14pt bold): >= 3:1
- Non-text (buttons, inputs, icons): >= 3:1
- Info never conveyed by color alone — add icon/text/pattern

### Semantic HTML
- Heading order: h1 → h2 → h3 (no skipping)
- Landmarks: `<nav>`, `<main>`, `<section>`, `<article>`
- `<button>` for actions, `<a>` for navigation (not divs)
- Lists use `<ul>`/`<ol>`, not styled divs

### Forms
- Every input has `<label>` (not just placeholder)
- Errors linked via `aria-describedby`
- Required fields indicated (not just color)
- Groups use `<fieldset>` + `<legend>`

### Keyboard
- All interactive elements reachable via Tab
- Tab order matches visual order
- Focus trap in modals
- Escape closes modals/dropdowns

### Screen Readers
- Images: descriptive `alt` or `alt=""` for decorative
- Icons with meaning: `aria-label`
- Dynamic content: `aria-live`
- Decorative: `aria-hidden="true"`

**Scoring:** 9-10: WCAG AA compliant, keyboard+screen reader tested | 7-8: Good contrast/semantics, minor ARIA gaps | 5-6: Basic semantics, missing labels, poor keyboard | 3-4: Contrast failures, non-semantic | 0-2: Divs everywhere, no alt text, no focus

### Nielsen Heuristic Alignment
- H1: Loading/state indicators | H3: Undo, escape, back | H5: Confirmation, validation | H9: Clear error messages | H10: Tooltips, help
- See `references/nielsen-heuristics.md` for full checklist
