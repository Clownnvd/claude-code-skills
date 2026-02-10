# Measurement — Real Metrics

Supplement code-based scoring with actual measurements when available.

## Lighthouse Audit

### Run via CLI (no browser needed)
```bash
# Install globally once
npm install -g lighthouse

# Run audit on dev server (start server first: pnpm dev)
lighthouse http://localhost:3000 --output=json --output-path=./lighthouse-report.json --chrome-flags="--headless --no-sandbox"

# Quick scores only
lighthouse http://localhost:3000 --output=json --quiet | node -e "
  const r = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
  const c = r.categories;
  console.log('Performance:', Math.round(c.performance.score*100));
  console.log('Accessibility:', Math.round(c.accessibility.score*100));
  console.log('Best Practices:', Math.round(c['best-practices'].score*100));
  console.log('SEO:', Math.round(c.seo.score*100));
"
```

### Map Lighthouse → Scoring Categories
| Lighthouse Category | Maps to ui-scoring |
|--------------------|-------------------|
| Performance score | Performance (cat 10) |
| Accessibility score | Accessibility (cat 7) |
| Best Practices | Interactions (cat 6) |
| SEO | Content (cat 8) |

### Score Calibration
| Lighthouse Score | ui-scoring Equivalent |
|------------------|-----------------------|
| 90-100 | 9-10 (Exceptional) |
| 50-89 | 6-8 (Average to Good) |
| 0-49 | 0-5 (Poor to Critical) |

## Contrast Checking

### Using axe-core via CLI
```bash
# Install
npm install -g @axe-core/cli

# Run accessibility audit
axe http://localhost:3000 --tags wcag2a,wcag2aa
```

### Manual contrast check (quick)
For specific color pairs, calculate contrast ratio:
```
Foreground: oklch(L1 C1 H1) → convert to sRGB → relative luminance L1
Background: oklch(L2 C2 H2) → convert to sRGB → relative luminance L2
Ratio = (max(L1,L2) + 0.05) / (min(L1,L2) + 0.05)
Target: >= 4.5:1 normal text, >= 3:1 large text
```

### Common contrast pairs to verify
| Element | Foreground | Background | Min Ratio |
|---------|-----------|------------|-----------|
| Body text | `--foreground` | `--background` | 4.5:1 |
| Muted text | `--muted-foreground` | `--background` | 4.5:1 |
| Primary button text | white | `--primary` | 4.5:1 |
| Link text | `--primary` | `--background` | 4.5:1 |
| Card text | `--card-foreground` | `--card` | 4.5:1 |

## Bundle Size Analysis

```bash
# Next.js built-in analyzer
ANALYZE=true pnpm build

# Or use @next/bundle-analyzer
# In next.config.ts:
# const withBundleAnalyzer = require('@next/bundle-analyzer')({ enabled: process.env.ANALYZE === 'true' })
```

### Targets
| Metric | Good | Warning | Bad |
|--------|------|---------|-----|
| First Load JS | < 80KB | 80-150KB | > 150KB |
| Page JS | < 50KB | 50-100KB | > 100KB |
| Total bundle | < 300KB | 300-500KB | > 500KB |

## When to Use Measurements

| Pipeline Phase | Measurement |
|---------------|-------------|
| After Phase 3 (Score) | Run Lighthouse if dev server available |
| After Phase 4 (Fix) | Run contrast check on changed components |
| Phase 5 (Ship) | Full Lighthouse + bundle analysis |
| Quick audit | Skip measurements, use code-based scoring only |

## Fallback: Code-Based Only

If Lighthouse/axe unavailable (no dev server, CI environment):
- Score based on code analysis only (current behavior)
- Flag "measurement pending" in scorecard
- Add to "verify before deploy" checklist
