# Component Patterns (CViet Design System)

> Button, Card, Input, Badge, and Sidebar patterns using Tailwind CSS v4 utilities

---

## Button

```html
<!-- Primary CTA -->
<button class="
  bg-brand text-white px-6 py-3 rounded-lg
  font-medium text-sm
  hover:bg-brand-dark active:scale-[0.98]
  transition-colors duration-200
  cursor-pointer
  min-h-11 min-w-11
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand
">
  Tao CV ngay
</button>

<!-- Secondary -->
<button class="
  bg-surface text-text px-6 py-3 rounded-lg
  font-medium text-sm border border-border
  hover:bg-gray-50 active:scale-[0.98]
  transition-colors duration-200
  cursor-pointer
">
  Xem truoc
</button>

<!-- Ghost -->
<button class="
  text-muted px-4 py-2 rounded-lg
  font-medium text-sm
  hover:bg-gray-100 hover:text-text
  transition-colors duration-200
  cursor-pointer
">
  Huy
</button>
```

**Note**: v4 changed button cursor to `default`. CViet requires `cursor-pointer` explicitly.

## Card

```html
<div class="
  bg-surface rounded-xl border border-border
  p-6 shadow-xs
  hover:shadow-sm hover:border-brand/20
  transition-all duration-200
">
  <h3 class="text-lg font-semibold text-text">CV Template</h3>
  <p class="text-sm text-muted mt-2">Mau CV chuyen nghiep</p>
</div>
```

**Note**: v4 renamed `shadow-sm` -> `shadow-xs`, `shadow` -> `shadow-sm`.

## Input

```html
<div class="flex flex-col gap-1.5">
  <label class="text-sm font-medium text-text">
    Ho va ten
  </label>
  <input
    type="text"
    placeholder="Nguyen Van A"
    class="
      w-full px-4 py-3 rounded-lg
      border border-border bg-surface text-text
      text-sm placeholder:text-muted/50
      focus:border-brand focus:outline-hidden focus:ring-1 focus:ring-brand
      transition-colors duration-200
    "
  />
  <p class="text-xs text-muted">Nhap ho ten day du cua ban</p>
</div>
```

**Note**: v4 changed `outline-none` -> `outline-hidden`, `ring` -> `ring-1`.

## Badge

```html
<!-- Pro badge -->
<span class="
  inline-flex items-center gap-1
  px-2.5 py-0.5 rounded-full
  text-xs font-medium
  bg-success/10 text-success
">
  Pro
</span>

<!-- Free badge -->
<span class="
  inline-flex items-center gap-1
  px-2.5 py-0.5 rounded-full
  text-xs font-medium
  bg-muted/10 text-muted
">
  Free
</span>

<!-- Status badge -->
<span class="
  inline-flex items-center gap-1
  px-2.5 py-0.5 rounded-full
  text-xs font-medium
  bg-brand/10 text-brand
">
  AI Enhanced
</span>
```

## Sidebar Navigation

```html
<nav class="flex flex-col gap-1 p-3">
  <!-- Active item -->
  <a href="/dashboard" class="
    flex items-center gap-3 px-3 py-2.5 rounded-lg
    bg-brand/10 text-brand font-medium text-sm
    cursor-pointer
  ">
    <LayoutDashboard class="w-5 h-5" />
    Dashboard
  </a>

  <!-- Inactive item -->
  <a href="/cv/new" class="
    flex items-center gap-3 px-3 py-2.5 rounded-lg
    text-muted hover:bg-gray-100 hover:text-text
    font-medium text-sm
    transition-colors duration-200 cursor-pointer
  ">
    <Plus class="w-5 h-5" />
    Tao CV moi
  </a>
</nav>
```
