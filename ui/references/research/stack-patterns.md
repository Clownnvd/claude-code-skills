# Stack Patterns — Next.js / React / Tailwind

## Next.js App Router

### Layout patterns
- `layout.tsx` for shared chrome (header, sidebar, footer)
- `loading.tsx` for Suspense fallbacks
- `error.tsx` for error boundaries
- Parallel routes `@modal` for overlays without navigation
- Route groups `(marketing)` for layout segmentation

### Server vs Client components
- **Server default**: data fetching, heavy imports, SEO content
- **Client (`"use client"`)**: interactivity, hooks, browser APIs
- Push `"use client"` boundary down — keep pages as server components

### Image optimization
- `next/image` with `priority` on above-fold images
- `sizes` prop for responsive: `"(max-width: 768px) 100vw, 50vw"`
- Blur placeholder: `placeholder="blur"` with `blurDataURL`

## React Patterns

### Component structure
```
src/components/
  ui/          → reusable primitives (button, input, card)
  landing/     → page-specific sections
  dashboard/   → authenticated UI
  auth/        → sign-in/up flows
```

### Animation approaches
1. **CSS only**: `transition-all`, `animate-*` (Tailwind)
2. **Intersection Observer**: scroll-triggered reveals
3. **Framer Motion**: complex orchestrated animations
4. **View Transitions API**: page-level transitions (experimental)

### Performance
- `React.lazy()` + `Suspense` for code splitting
- `useMemo` / `useCallback` only when measured
- Virtualize lists > 50 items (`@tanstack/react-virtual`)

## Tailwind CSS 4

### Key differences from v3
- `bg-linear-to-r` NOT `bg-gradient-to-r`
- CSS-first config (no `tailwind.config.js` needed)
- `@theme` directive for design tokens
- Native container queries with `@container`

### Spacing system
- Section padding: `py-24 lg:py-32`
- Container: `mx-auto max-w-7xl px-4 sm:px-6 lg:px-8`
- Card padding: `p-6 sm:p-8`
- Stack gap: `space-y-4` or `gap-4`

### Responsive breakpoints
```
sm: 640px   → mobile landscape
md: 768px   → tablet
lg: 1024px  → desktop
xl: 1280px  → wide desktop
2xl: 1536px → ultrawide
```

### Dark mode
- Use semantic tokens: `bg-background`, `text-foreground`
- Avoid hardcoded colors: `bg-white` → `bg-card`
- Class strategy: `dark:` prefix with CSS variables
- Test both modes during development

### Common compositions
```
/* Card with hover */
rounded-2xl border border-border bg-card p-6 shadow-sm
transition-all hover:shadow-lg hover:border-primary/20

/* Gradient text */
bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent

/* Glass effect */
backdrop-blur-xl bg-background/80 border border-border/50

/* Responsive grid */
grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3
```
