# Responsiveness & Performance Criteria

Covers categories 5, 10: Responsiveness (12%), Performance (5%).

## 5. Responsiveness (12%)

**Quick checklist:**
- [ ] Works at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll at any breakpoint
- [ ] Touch targets >= 44px on mobile
- [ ] Text readable without zooming on mobile
- [ ] Images scale proportionally

### Breakpoint Testing
- **375px** (iPhone SE): All content visible, no overflow
- **390px** (iPhone 14): Primary mobile experience
- **768px** (iPad): 2-col instead of 1
- **1024px** (Laptop): Desktop layout
- **1440px** (Desktop): Content constrained (max-width)
- **1920px+** (Large): No stretched layouts, centered

### Mobile-Specific
- Touch targets >= 44x44px (Apple HIG) or 48x48px (Material)
- No horizontal scrollbar at any width
- Text >= 16px body, readable without zoom
- Images scale proportionally, no overflow
- Sticky elements don't obscure content

### Layout Behavior
- Grid collapses: 3-col → 2-col → 1-col
- Nav → hamburger/drawer on mobile
- Tables → scrollable or cards on mobile
- Hero text no overflow/truncate
- Forms stack vertically on mobile

### Advanced
- Container queries for component-level responsiveness
- Fluid typography: `clamp()` for font sizes
- Image `srcset`/`sizes` for resolution-appropriate images
- Aspect ratios preserved across breakpoints

**Scoring:** 9-10: Pixel-perfect all breakpoints, touch targets sized, fluid | 7-8: Works, minor issues (tight spacing, one overflow) | 5-6: Functional but desktop-first | 3-4: Broken at mobile, horizontal scroll | 0-2: Not responsive

**Common issues:** Text overflow on mobile (long URLs), grid not collapsing, buttons too small to tap, fixed-width breaking layout, missing viewport meta.

## 10. Performance (5%)

**Quick checklist:**
- [ ] No layout shift during load (CLS)
- [ ] Images optimized (WebP/AVIF, lazy loaded)
- [ ] No render-blocking resources
- [ ] Minimal JS bundle for initial paint
- [ ] Smooth scrolling and animations (60fps)

### Core Web Vitals
- **LCP** (Largest Contentful Paint): < 2.5s good, < 4s needs improvement
- **CLS** (Cumulative Layout Shift): < 0.1 good, < 0.25 needs improvement
- **INP** (Interaction to Next Paint): < 200ms good, < 500ms needs improvement

### Image Optimization
- Modern formats (WebP, AVIF) with fallbacks
- Lazy loading below-fold (`loading="lazy"`)
- Explicit width/height (prevent layout shift)
- Responsive via `srcset`, no oversized images

### Code Performance
- JS bundle minimized, tree-shaken, code-split
- No render-blocking CSS/JS in `<head>`
- Fonts preloaded or `font-display: swap`
- Third-party scripts async/deferred

### Animation Performance
- Use `transform`/`opacity` only (GPU-accelerated)
- No layout thrashing
- 60fps scrolling (no scroll event handlers without throttle)
- IntersectionObserver for scroll-triggered (not scroll listeners)

**Scoring:** 9-10: Lighthouse 95+, sub-2s LCP, no CLS, 60fps | 7-8: Good vitals, minor opportunities | 5-6: Slow on mobile, LCP > 3s | 3-4: Jank, large unoptimized images | 0-2: 5s+ load, significant shifts

### Measurement Tools
Lighthouse (DevTools/CLI), PageSpeed Insights, WebPageTest, Bundle analyzer
