# Dark Mode Patterns

> System preference, class-based toggle, and CSS variable strategies for Tailwind CSS v4

---

## Default: System Preference

By default, `dark:` uses `prefers-color-scheme: dark`:

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Follows OS dark mode setting
</div>
```

## Selector Strategy (Class-Based Toggle)

Override with `@custom-variant`:

```css
@import "tailwindcss";

/* Use .dark class on <html> to toggle */
@custom-variant dark (&:where(.dark, .dark *));
```

## Data Attribute Strategy

```css
@import "tailwindcss";

/* Use data-theme="dark" attribute */
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
```

## Three-Way Toggle (Light/Dark/System)

```html
<html>
<head>
  <!-- Inline in <head> to prevent FOUC (Flash of Unstyled Content) -->
  <script>
    (function() {
      var theme = localStorage.getItem('theme');
      if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
      }
    })();
  </script>
</head>
```

Toggle function:
```ts
function setTheme(mode: 'light' | 'dark' | 'system') {
  if (mode === 'system') {
    localStorage.removeItem('theme');
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.classList.toggle('dark', isDark);
  } else {
    localStorage.setItem('theme', mode);
    document.documentElement.classList.toggle('dark', mode === 'dark');
  }
}
```

## Using CSS Variables for Dark Mode Colors

```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));

@theme inline {
  --color-bg: #FAFAF8;
  --color-surface: #FFFFFF;
  --color-text: #0F172A;
  --color-muted: #64748B;
  --color-border: #E2E8F0;
}

.dark {
  --color-bg: #0F172A;
  --color-surface: #1E293B;
  --color-text: #F8FAFC;
  --color-muted: #94A3B8;
  --color-border: #334155;
}
```

Usage:
```html
<div class="bg-bg text-text border-border">
  Automatically switches with dark mode
</div>
```

## @variant Directive (Apply Variants in CSS)

```css
.my-card {
  background: white;
  color: var(--color-text);

  @variant dark {
    background: var(--color-surface);
    color: var(--color-text);
  }
}
```
