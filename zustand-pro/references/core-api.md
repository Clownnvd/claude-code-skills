# Core API Reference

## `create` -- Create a React Hook Store

```typescript
import { create } from 'zustand'

// Basic store with TypeScript
interface CounterState {
  count: number
  increment: () => void
  decrement: () => void
  reset: () => void
}

const useCounterStore = create<CounterState>()((set, get) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}))
```

**Important**: For TypeScript, always use the curried form `create<Type>()(...)` with the extra `()`.

## `createStore` -- Create a Vanilla Store (no React)

```typescript
import { createStore } from 'zustand/vanilla'

// Used for: per-request stores, non-React contexts, testing
const store = createStore<CounterState>()((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}))

// Access without React
store.getState()         // { count: 0, increment: fn, ... }
store.setState({ count: 5 })
store.subscribe((state) => console.log(state))
```

## `useStore` -- Use a Vanilla Store in React

```typescript
import { useStore } from 'zustand'

function Counter({ store }: { store: StoreApi<CounterState> }) {
  const count = useStore(store, (s) => s.count)
  const increment = useStore(store, (s) => s.increment)
  return <button onClick={increment}>{count}</button>
}
```

## `setState` API

```typescript
// Partial update (merged with current state)
store.setState({ count: 5 })

// Functional update
store.setState((state) => ({ count: state.count + 1 }))

// Replace entire state (v5: must provide ALL fields)
store.setState({ count: 0, increment: fn, decrement: fn, reset: fn }, true)
```

## `subscribe` API

```typescript
// Subscribe to all state changes
const unsub = store.subscribe((state, prevState) => {
  console.log('State changed:', state)
})

// Cleanup
unsub()
```

## Selectors

```typescript
function Component() {
  // Select single value (only re-renders when count changes)
  const count = useCounterStore((state) => state.count)

  // Select action (stable reference, never causes re-render)
  const increment = useCounterStore((state) => state.increment)

  // BAD: selecting multiple values as new object -- causes re-render every time in v5
  // const { count, name } = useCounterStore((state) => ({ count: state.count, name: state.name }))

  // GOOD: use useShallow for multiple values
  const { count, name } = useCounterStore(
    useShallow((state) => ({ count: state.count, name: state.name }))
  )
}
```
