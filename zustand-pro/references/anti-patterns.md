# Anti-Patterns & Gotchas

## Anti-Pattern 1: Using Store Inside Server Components

```tsx
// WRONG:
export default async function Page() {
  const data = useCVEditorStore.getState()  // Returns defaults, not reactive
  return <div>{data.cvData.personalInfo.fullName}</div>
}

// CORRECT: Fetch on server, pass to client
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const cv = await db.cv.findUnique({ where: { id } })
  return <CVEditor initialData={cv.data} />
}
```

## Anti-Pattern 2: Selecting the Entire Store

```tsx
// WRONG: Re-renders on ANY state change
function Component() {
  const state = useCVEditorStore() // No selector = entire state
  return <div>{state.cvData.personalInfo.fullName}</div>
}

// CORRECT: Select only what you need
function Component() {
  const fullName = useCVEditorStore((s) => s.cvData.personalInfo.fullName)
  return <div>{fullName}</div>
}
```

## Anti-Pattern 3: Creating Stores Inside Components

```tsx
// WRONG: New store on every render
function Component() {
  const useStore = create((set) => ({ count: 0 }))  // BAD!
  const count = useStore((s) => s.count)
}

// CORRECT: Create store outside component at module level
const useStore = create((set) => ({ count: 0 }))

function Component() {
  const count = useStore((s) => s.count)
}
```

## Anti-Pattern 4: Mutating State Directly Without Immer

```typescript
// WRONG (without immer):
set((state) => {
  state.items.push(newItem)  // Direct mutation -- React won't see this
  return state
})

// CORRECT (without immer):
set((state) => ({
  items: [...state.items, newItem]
}))

// CORRECT (with immer):
set((state) => {
  state.items.push(newItem)  // OK with immer middleware
})
```

## Anti-Pattern 5: Using Zustand for Server State

```typescript
// WRONG: Using Zustand to cache API responses
const useDataStore = create((set) => ({
  users: [],
  fetchUsers: async () => {
    const res = await fetch('/api/users')
    const users = await res.json()
    set({ users })
  },
}))

// CORRECT: Use React Query / TanStack Query for server state
// Zustand is for CLIENT state (UI state, form state, etc.)
// The CViet project already uses @tanstack/react-query in use-cvs.ts
```

## Anti-Pattern 6: Forgetting `useShallow` When Returning Objects/Arrays

```tsx
// WRONG in v5 (creates new object reference every render):
const { a, b } = useStore((s) => ({ a: s.a, b: s.b }))

// CORRECT:
const { a, b } = useStore(useShallow((s) => ({ a: s.a, b: s.b })))

// ALSO CORRECT: Multiple individual selectors
const a = useStore((s) => s.a)
const b = useStore((s) => s.b)
```

## Gotcha: Middleware Order Matters

```typescript
// Middleware wraps from innermost to outermost.
// devtools should be outermost to see final state shape.
// immer should be innermost to transform set() behavior first.

// CORRECT ORDER:
create(devtools(persist(immer(fn))))

// WRONG ORDER (devtools won't see immer mutations correctly):
create(immer(devtools(persist(fn))))
```

## Gotcha: `Set` and `Map` Don't Persist

```typescript
// localStorage serialization loses Set and Map
// The persist middleware uses JSON.stringify/parse by default

// WRONG:
completedSteps: new Set(['personal', 'experience'])  // Serializes to {}

// FIX: Use custom serialization or arrays
persist(
  (set) => ({ completedSteps: ['personal', 'experience'] }),  // Use array
  {
    name: 'cv-editor',
    // Or: custom storage with Set handling
    storage: {
      getItem: (name) => {
        const str = localStorage.getItem(name)
        if (!str) return null
        const parsed = JSON.parse(str)
        if (parsed.state.completedSteps) {
          parsed.state.completedSteps = new Set(parsed.state.completedSteps)
        }
        return parsed
      },
      setItem: (name, value) => {
        const toStore = {
          ...value,
          state: {
            ...value.state,
            completedSteps: [...value.state.completedSteps],
          },
        }
        localStorage.setItem(name, JSON.stringify(toStore))
      },
      removeItem: (name) => localStorage.removeItem(name),
    },
  }
)
```

## Gotcha: `getState()` Is Not Reactive

```typescript
// WRONG: In a React component, getState() won't trigger re-renders
function Component() {
  const count = useCVEditorStore.getState().count  // Static, never updates
  return <div>{count}</div>
}

// CORRECT: Use the hook with a selector
function Component() {
  const count = useCVEditorStore((s) => s.count)  // Reactive
  return <div>{count}</div>
}

// OK: getState() is fine outside React or in event handlers
function handleClick() {
  const current = useCVEditorStore.getState().count  // One-time read
}
```
