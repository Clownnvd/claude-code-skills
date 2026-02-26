# Fix Patterns: Responsiveness

## Table → Mobile Cards

### 3-col grid table cramped at 375px
```tsx
// Before: always 3-col
<div className="grid grid-cols-3">

// After: stack on mobile, 3-col on sm+
<div className="grid grid-cols-1 sm:grid-cols-3">
```

### Alternative: horizontal scroll wrapper
```tsx
<div className="overflow-x-auto -mx-4 px-4 sm:mx-0 sm:px-0">
  <div className="min-w-[600px]">
    {/* Table content */}
  </div>
</div>
```

### Card-based mobile alternative
```tsx
// Show cards on mobile, table on desktop
<div className="block sm:hidden space-y-4">
  {rows.map(row => (
    <div key={row.id} className="rounded-lg border p-4">
      <div className="font-medium">{row.feature}</div>
      <div className="mt-2 flex justify-between text-sm text-muted-foreground">
        <span>DIY: {row.diyHours}</span>
        <Check className="size-5 text-primary" />
      </div>
    </div>
  ))}
</div>
<div className="hidden sm:block">
  {/* Original table */}
</div>
```

## Grid Collapse Patterns

### Standard collapse
```tsx
// 3-col → 2-col → 1-col
className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"

// 4-col → 2-col → 1-col
className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6"
```

### Bento grid collapse
```tsx
// BentoGrid already handles via its own responsive classes
// Ensure col-span classes reset on mobile:
className={i === 0 ? "sm:col-span-2" : ""} // NOT col-span-2 (breaks mobile)
```

## Touch Targets

### Minimum 44x44px (Apple HIG)
```tsx
// Before: too small
<button className="px-2 py-1 text-xs">

// After: adequate target
<button className="min-h-[44px] min-w-[44px] px-4 py-2 text-sm">
```

### Icon buttons need padding
```tsx
// Before
<button><ChevronDown className="size-4" /></button>

// After
<button className="flex items-center justify-center size-10">
  <ChevronDown className="size-4" />
</button>
```

## Text Overflow

### Long words / URLs
```tsx
className="break-words" // or overflow-wrap: break-word
// For URLs specifically:
className="break-all"   // breaks at any character
```

### Truncation with ellipsis
```tsx
className="truncate"           // single line
className="line-clamp-2"       // multi-line (2 lines)
```

## Mobile-First Patterns

### Hero text sizing
```tsx
// Responsive type scale
className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl"
```

### Fluid typography with clamp()
```css
.hero-heading {
  font-size: clamp(1.875rem, 5vw, 4.5rem);
}
```

### Stack on mobile, row on desktop
```tsx
className="flex flex-col sm:flex-row gap-4"
```

## Container Max-Widths

### Prevent stretching on large screens
```tsx
className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8"
// Content never exceeds 1024px, centered with padding
```

### Full-bleed with contained content
```tsx
<section className="w-full bg-accent/30">
  <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
    {/* Content */}
  </div>
</section>
```
