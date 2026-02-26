# Measurement — Optional Real Metrics

Supplement code-based scoring with Lighthouse and contrast checks when a dev server is available.

## Lighthouse Quick Scores

```bash
# Requires: npm install -g lighthouse
lighthouse http://localhost:3000 --output=json --quiet | node -e "
  const r = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
  const c = r.categories;
  console.log('Performance:', Math.round(c.performance.score*100));
  console.log('Accessibility:', Math.round(c.accessibility.score*100));
  console.log('Best Practices:', Math.round(c['best-practices'].score*100));
  console.log('SEO:', Math.round(c.seo.score*100));
"
```

### Map to ui-scoring categories
| Lighthouse | ui-scoring Category | Calibration Cap |
|------------|--------------------|-----------------|
| Performance | Performance (cat 10) | Cap at Lighthouse ÷ 10 |
| Accessibility | Accessibility (cat 7) | Cap at Lighthouse ÷ 10 |
| Best Practices | Interactions (cat 6) | Advisory only |
| SEO | Content (cat 8) | Advisory only |

## Contrast Check

```bash
# Requires: npm install -g @axe-core/cli
axe http://localhost:3000 --tags wcag2a,wcag2aa
```

### Key pairs to verify
| Element | Foreground | Background | Min Ratio |
|---------|-----------|------------|-----------|
| Body text | `--foreground` | `--background` | 4.5:1 |
| Muted text | `--muted-foreground` | `--background` | 4.5:1 |
| Primary button | white | `--primary` | 4.5:1 |
| Card text | `--card-foreground` | `--card` | 4.5:1 |

## When to Use

- **Available dev server**: Run Lighthouse, cap scores accordingly
- **No dev server**: Skip, score code-based only, flag "measurement pending"
- **Anti-Bias rule 3**: If Lighthouse available, Performance/Accessibility scores must not exceed Lighthouse ÷ 10
