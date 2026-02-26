# Fix Patterns: Performance

## Server Components (Next.js)

### Convert client → server where possible
```tsx
// Before: "use client" on a static section
"use client";
export function LogosSection() { return <section>...</section>; }

// After: remove "use client" if no hooks, event handlers, or browser APIs
export function LogosSection() { return <section>...</section>; }
```

### When "use client" IS required
- `useState`, `useEffect`, `useRef`, `useContext`
- Event handlers (`onClick`, `onChange`)
- Browser APIs (`window`, `document`, `IntersectionObserver`)
- Third-party client-only libraries

### Minimize client boundary
```tsx
// Before: entire section is client
"use client";
export function FeaturesSection() {
  return (
    <section>
      <h2>Features</h2>         {/* Static — doesn't need client */}
      <AnimatedGrid>...</AnimatedGrid>  {/* Needs client for animation */}
    </section>
  );
}

// After: split into server wrapper + client island
// features-section.tsx (server)
import { AnimatedFeatureGrid } from "./animated-feature-grid";
export function FeaturesSection() {
  return (
    <section>
      <h2>Features</h2>
      <AnimatedFeatureGrid />
    </section>
  );
}

// animated-feature-grid.tsx (client)
"use client";
export function AnimatedFeatureGrid() { /* animation logic */ }
```

## Image Optimization

### Use next/image instead of <img>
```tsx
// Before: raw img tag
<img src="https://picsum.photos/id/0/800/600" />

// After: next/image with optimization
import Image from "next/image";
<Image
  src="https://picsum.photos/id/0/800/600"
  alt="Product screenshot"
  width={800}
  height={600}
  className="rounded-lg"
  loading="lazy"
/>
```

### External domains in next.config
```ts
// next.config.ts
images: {
  remotePatterns: [
    { protocol: "https", hostname: "picsum.photos" },
  ],
}
```

### Prevent CLS with explicit dimensions
```tsx
// Always set width + height OR use fill with aspect-ratio container
<div className="relative aspect-video">
  <Image src="..." alt="..." fill className="object-cover" />
</div>
```

## Bundle Optimization

### Dynamic imports for heavy components
```tsx
import dynamic from "next/dynamic";

const HeroParallax = dynamic(
  () => import("@/components/ui/hero-parallax").then(m => ({ default: m.HeroParallax })),
  { loading: () => <div className="h-[600px] animate-pulse bg-muted" /> }
);
```

### Tree-shaking icon imports
```tsx
// Already correct: named imports from lucide-react
import { Shield, CreditCard } from "lucide-react";
// NOT: import * as Icons from "lucide-react"; // kills tree-shaking
```

## Animation Performance

### GPU-accelerated properties only
```css
/* Good: transform + opacity (composited) */
transform: translateY(-2px);
opacity: 0.8;

/* Bad: layout-triggering properties */
width: 100px;   /* triggers layout */
top: 10px;      /* triggers layout */
margin: 8px;    /* triggers layout */
```

### Avoid transition-all
```tsx
// Before
className="transition-all duration-200"

// After: specific properties
className="transition-[transform,box-shadow,border-color] duration-200"
```

### IntersectionObserver for scroll triggers
```tsx
// Already used in ScrollReveal ✓
// Never use scroll event listeners for reveal animations
```

## Font & Script Loading

- Next.js `next/font` handles preloading automatically
- Third-party scripts: use `<Script strategy="lazyOnload" />` (not raw `<script>`)
- Always set `font-display: swap` on custom `@font-face`
