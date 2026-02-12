# Fix Patterns: Bundle Size & Code Splitting + Image Optimization

## Bundle Size Fixes

### Dynamic Import Heavy Libraries
```typescript
// BEFORE: Top-level import
import { Chart } from 'chart.js';

// AFTER: Dynamic import
import dynamic from 'next/dynamic';
const Chart = dynamic(() => import('chart.js').then(m => m.Chart), { ssr: false });
```

### Remove Barrel Re-exports
```typescript
// BEFORE: src/components/index.ts
export * from './button';
export * from './modal';
export * from './chart'; // pulls in chart.js even if unused

// AFTER: Direct imports
import { Button } from '@/components/button';
import { Modal } from '@/components/modal';
```

### Lazy Below-Fold Components
```typescript
// BEFORE: Eager load
import { TestimonialsSection } from './testimonials-section';

// AFTER: Lazy load
import dynamic from 'next/dynamic';
const TestimonialsSection = dynamic(() => import('./testimonials-section'));
```

### Remove Unused Dependencies
```bash
# Find unused deps
npx depcheck
# Remove them
pnpm remove <unused-package>
```

### Tree-Shakeable Imports
```typescript
// BEFORE: Import entire library
import _ from 'lodash';
_.debounce(fn, 300);

// AFTER: Named import (tree-shakeable)
import { debounce } from 'lodash-es';
debounce(fn, 300);
```

---

## Image Optimization Fixes

### Replace Raw img Tags
```tsx
// BEFORE
<img src="/hero.png" alt="Hero" />

// AFTER
import Image from 'next/image';
<Image src="/hero.png" alt="Hero" width={1200} height={630} priority />
```

### Add Sizes for Responsive
```tsx
// BEFORE
<Image src="/feature.png" width={600} height={400} alt="Feature" />

// AFTER
<Image
  src="/feature.png"
  width={600}
  height={400}
  alt="Feature"
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
/>
```

### Use next/font
```typescript
// BEFORE: CSS @import or <link>
// @import url('https://fonts.googleapis.com/css2?family=Inter');

// AFTER: next/font
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });
```

### Optimize Public Assets
```bash
# Find large images
find public -name "*.png" -size +500k
find public -name "*.jpg" -size +500k
# Convert to WebP
npx sharp-cli -i public/image.png -o public/image.webp --format webp --quality 80
```
