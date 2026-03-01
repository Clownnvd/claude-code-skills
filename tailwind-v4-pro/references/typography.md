# Typography Patterns

> Font registration, Vietnamese text support, and responsive sizing in Tailwind CSS v4

---

## Font Registration

```css
/* Step 1: Load the font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import "tailwindcss";

/* Step 2: Register in @theme */
@theme inline {
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-display: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;
}
```

Usage: `<p class="font-sans">`, `<h1 class="font-display">`, `<code class="font-mono">`

## Vietnamese Text Support

Vietnamese uses Latin script with extensive diacritical marks (e.g., a, a, a, o, u). Key considerations:

```css
@theme inline {
  /* Inter has excellent Vietnamese support */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
}

/* Ensure proper rendering of Vietnamese diacritical marks */
body {
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-rendering improves diacritical mark positioning */
  text-rendering: optimizeLegibility;
}
```

When loading Google Fonts with Vietnamese subset:
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&subset=vietnamese&display=swap');
```

## Text Size Customization

```css
@theme {
  --text-xs: 0.75rem;
  --text-xs--line-height: 1rem;
  --text-sm: 0.875rem;
  --text-sm--line-height: 1.25rem;
  --text-base: 1rem;
  --text-base--line-height: 1.5rem;
  --text-lg: 1.125rem;
  --text-lg--line-height: 1.75rem;
}
```

The `--text-*--line-height` convention pairs a line-height with each text size automatically.

## Responsive Typography

```html
<h1 class="text-2xl md:text-3xl lg:text-4xl font-bold tracking-tight">
  Tao CV chuyen nghiep
</h1>
<p class="text-base md:text-lg text-muted leading-relaxed">
  Xay dung CV an tuong voi AI
</p>
```
