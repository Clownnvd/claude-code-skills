# UI Scoring — Edge Cases Eval

Verify correct behavior for UI-specific edge cases.

## Test 1: No Responsive Breakpoints

- Provide components with fixed pixel widths and no media queries
- Verify Responsiveness scores <= 3 (CRITICAL)
- Verify Spacing & Layout also penalized for non-fluid layout
- Verify issue identifies specific components lacking breakpoints

## Test 2: Missing ARIA Labels and Alt Text

- Provide interactive elements without ARIA attributes and images without alt text
- Verify Accessibility scores <= 2 (CRITICAL)
- Verify issue lists each failing element and its location
- Verify fix recommends specific ARIA roles and alt text patterns

## Test 3: No Visual Hierarchy (Flat Design)

- Provide page where all text is same size, weight, and color
- Verify Visual Hierarchy scores <= 3
- Verify Typography also penalized for missing type scale
- Verify fix recommends heading hierarchy and emphasis patterns

## Test 4: Hardcoded Colors Instead of Design Tokens

- Provide components using hex values instead of CSS variables from globals.css
- Verify Color & Theme scores <= 4
- Verify issue identifies hardcoded color values
- Verify fix recommends using existing CSS custom properties

## Test 5: No Loading or Feedback States

- Provide interactive components (buttons, forms) with no loading indicators
- Verify Interactions scores <= 3
- Verify Content & Copy penalized for missing feedback messaging
- Verify Nielsen heuristic "Visibility of system status" fails

## Test 6: CTA Below the Fold With No Visual Weight

- Provide landing page with primary CTA buried or styled like secondary elements
- Verify Conversion & CTA scores <= 4
- Verify Visual Hierarchy also penalized
- Verify fix recommends above-fold placement and contrasting CTA styling

## Test 7: Anti-Bias Baseline Enforcement

- Run scoring and verify no category starts above 7 without evidence
- Verify scores of 9-10 cite specific positive evidence in Notes column
- Verify scores below 5 cite specific failing checklist items
- Verify output does not inflate scores for "looking nice" without criteria
