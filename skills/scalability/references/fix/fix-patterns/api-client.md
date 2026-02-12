# Fix Patterns: API Response Performance + Client-Side Performance

## API Performance Fixes

### Return Only Needed Fields
```typescript
// BEFORE: Returns full DB object
const purchase = await prisma.purchase.findUnique({ where: { userId } });
return NextResponse.json(purchase);

// AFTER: Select specific fields
const purchase = await prisma.purchase.findUnique({
  where: { userId },
  select: { id: true, status: true, purchasedAt: true },
});
return NextResponse.json(purchase);
```

### Add Pagination
```typescript
// BEFORE: Unbounded list
const items = await prisma.item.findMany();

// AFTER: Paginated
const page = Number(searchParams.get('page') || '1');
const limit = Math.min(Number(searchParams.get('limit') || '20'), 100);
const items = await prisma.item.findMany({
  take: limit,
  skip: (page - 1) * limit,
  orderBy: { createdAt: 'desc' },
});
return NextResponse.json({ items, page, limit });
```

### Use Consistent Response Format
```typescript
// Shared helper: src/lib/api/response.ts
export function apiSuccess<T>(data: T, status = 200) {
  return NextResponse.json(data, { status });
}
export function apiError(message: string, status = 400) {
  return NextResponse.json({ error: message }, { status });
}
```

### Add AbortController
```typescript
// BEFORE: No timeout
const res = await fetch('https://api.external.com/data');

// AFTER: With timeout
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);
try {
  const res = await fetch('https://api.external.com/data', {
    signal: controller.signal,
  });
  return res.json();
} finally {
  clearTimeout(timeout);
}
```

---

## Client-Side Performance Fixes

### Debounce Frequent Events
```typescript
// BEFORE: API call on every keystroke
function SearchInput() {
  const [query, setQuery] = useState('');
  useEffect(() => { fetchResults(query); }, [query]);
}

// AFTER: Debounced
import { useDebouncedCallback } from 'use-debounce';
function SearchInput() {
  const [query, setQuery] = useState('');
  const debouncedSearch = useDebouncedCallback((value: string) => {
    fetchResults(value);
  }, 300);
  return <input onChange={e => { setQuery(e.target.value); debouncedSearch(e.target.value); }} />;
}
```

### CSS Animations
```css
/* BEFORE: JS animation */
/* element.style.left = `${x}px`; // causes layout */

/* AFTER: CSS transform (GPU-accelerated) */
.slide-in {
  transform: translateX(0);
  transition: transform 0.3s ease-out;
}
.slide-in[data-hidden] {
  transform: translateX(-100%);
}
```

### Proper List Keys
```tsx
// BEFORE: Index as key
{items.map((item, index) => <Item key={index} {...item} />)}

// AFTER: Stable unique key
{items.map(item => <Item key={item.id} {...item} />)}
```

### Avoid Unnecessary State
```typescript
// BEFORE: Derived value in state
const [items, setItems] = useState([]);
const [count, setCount] = useState(0);
useEffect(() => { setCount(items.length); }, [items]);

// AFTER: Compute directly
const [items, setItems] = useState([]);
const count = items.length; // derived, no state needed
```
