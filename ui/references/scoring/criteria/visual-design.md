# Visual Design Criteria

Covers categories 1-4: Visual Hierarchy (15%), Color & Theme (10%), Typography (10%), Spacing & Layout (12%).

## 1. Visual Hierarchy (15%)

**Quick checklist:**
- [ ] Clear primary → secondary → tertiary content flow
- [ ] Eye drawn to most important element first (CTA, heading)
- [ ] Size, color, weight used to establish importance
- [ ] Z-pattern or F-pattern scanning supported
- [ ] Visual grouping via proximity (Gestalt)

**What to check:** Size contrast (H1 >> body), color weight (accent draws eye to CTA), spatial prominence (top-left F-pattern or center Z-pattern), grouping (Gestalt proximity), depth (shadows separate interactive from static).

**Scoring:** 9-10: Eye flows headline→value prop→CTA, no ambiguity | 7-8: Mostly clear, 1-2 competing elements | 5-6: Multiple same-weight elements | 3-4: Flat hierarchy | 0-2: Random placement

**Common issues:** Hero heading same size as section headings, multiple CTAs with same weight, important info buried below fold, no whitespace between sections.

## 2. Color & Theme (10%)

**Quick checklist:**
- [ ] Consistent palette (60-30-10 rule)
- [ ] Primary/accent colors used purposefully for CTAs + emphasis
- [ ] Dark mode support (if applicable)
- [ ] No clashing or random colors
- [ ] Design tokens used (not hardcoded hex values)

**What to check:** 60-30-10 rule (bg/secondary/accent), semantic colors (green=success, red=error), contrast ratios (WCAG AA: 4.5:1 text, 3:1 large), dark mode both modes tested, token usage (CSS vars not inline hex).

**Scoring:** 9-10: Harmonious, purposeful accent, both modes polished | 7-8: Good, 1-2 inconsistencies | 5-6: Functional but bland | 3-4: Inconsistent, poor contrast | 0-2: No system

**Common issues:** `zinc-*` hardcoded instead of `bg-background`, accent on non-interactive elements, dark mode contrast fail, too many colors.

## 3. Typography (10%)

**Quick checklist:**
- [ ] Max 2-3 font families
- [ ] Clear heading hierarchy (h1 > h2 > h3)
- [ ] Body text >= 16px, line-height >= 1.5
- [ ] Line length 50-75 characters
- [ ] Sentence case for headings (not ALL CAPS unless brand)

**What to check:** Font count (heading + body + optional mono), scale (14→16→20→24→32→48), weight (bold headings, regular body), line height (body >=1.5, headings 1.1-1.3), line length (50-75ch).

**Scoring:** 9-10: Professional rhythm, every text intentional | 7-8: Good, minor issues | 5-6: Readable but generic | 3-4: Poor readability | 0-2: No typographic system

## 4. Spacing & Layout (12%)

**Quick checklist:**
- [ ] Consistent spacing system (4px/8px grid)
- [ ] Adequate breathing room between sections
- [ ] Aligned to grid system
- [ ] Related items grouped, unrelated items separated
- [ ] No cramped or overly sparse areas

**What to check:** Grid system (12-col, auto-grid), spacing scale (4px/8px multiples), section rhythm (consistent vertical spacing), card/component padding consistency, alignment (left edges, centers).

**Scoring:** 9-10: Mathematical precision, luxurious whitespace | 7-8: Mostly consistent, 1-2 anomalies | 5-6: Some cramped areas | 3-4: Random paddings/margins | 0-2: Overlapping/chaotic

**Common issues:** Section padding varies (py-12 then py-20 then py-8), card padding inconsistent, no gap between icon and label, heading too close to preceding section.
