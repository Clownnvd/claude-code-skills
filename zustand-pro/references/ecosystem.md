# Comparison & Ecosystem

## 12. Comparison: Zustand vs Redux vs Jotai

| Feature | Zustand | Redux Toolkit | Jotai |
|---------|---------|--------------|-------|
| **Bundle size** | ~3 KB | ~35 KB | ~8 KB |
| **Boilerplate** | Minimal | Moderate (slices, reducers) | Minimal |
| **Learning curve** | Low | Moderate-High | Low |
| **State model** | Single store (top-down) | Single store (top-down) | Atoms (bottom-up) |
| **TypeScript** | Excellent (v5) | Excellent | Excellent |
| **DevTools** | Via middleware | Built-in | Via plugin |
| **Middleware** | persist, devtools, immer, etc. | Built-in (createSlice) | Custom |
| **SSR/Next.js** | Good (with patterns) | Good | Good |
| **React 19** | Compatible | Compatible | Compatible |
| **Time travel** | Via zundo | Built-in | Via plugin |
| **Provider needed** | No (opt-in for SSR) | Yes (always) | Yes (always) |
| **Outside React** | Yes (vanilla store) | Yes (store.getState) | Limited |

### When to Use Which

- **Zustand**: 90% of cases. Client state, UI state, form state, when you want minimal boilerplate. Best for CViet.
- **Redux Toolkit**: Large teams with strict conventions, complex action flows, time-travel debugging as a hard requirement.
- **Jotai**: Atomic/bottom-up state, spreadsheet-like apps, form builders with deeply interdependent fields.

### Why Zustand for CViet

1. **Minimal boilerplate**: CViet is a small-to-medium SaaS, not a large enterprise app
2. **No Provider required**: Simpler than Redux (unless using per-request SSR pattern)
3. **Immer middleware**: Perfect for deeply nested CVData updates
4. **Works alongside React Query**: CViet already uses @tanstack/react-query for server state; Zustand handles client state
5. **Small bundle**: 3 KB matters for a user-facing SaaS product
6. **Undo/redo via zundo**: Critical for CV editor UX

---

## 13. Ecosystem & Third-Party Middleware

| Package | Size | Purpose | Zustand Compat |
|---------|------|---------|----------------|
| `zundo` | <700B | Undo/redo temporal middleware | v4.2+ / v5 |
| `zustand-computed` | ~1KB | Computed/derived state | v4+ / v5 |
| `zustand-debounce` | ~1KB | Debounced persist storage | v4+ / v5 |
| `zukeeper` | ~5KB | Enhanced devtools UI | v4+ / v5 |

### Key Links

- Official docs: https://zustand.docs.pmnd.rs/
- GitHub: https://github.com/pmndrs/zustand
- v5 migration: https://zustand.docs.pmnd.rs/migrations/migrating-to-v5
- Next.js guide: https://zustand.docs.pmnd.rs/guides/nextjs
- Zundo (undo/redo): https://github.com/charkour/zundo
- npm: https://www.npmjs.com/package/zustand

---

## Quick Reference Card

```bash
# Install
pnpm add zustand

# Install with all optional middleware deps
pnpm add zustand immer zundo
```

```typescript
// Minimal store
import { create } from 'zustand'
const useStore = create<State>()((set) => ({ /* state + actions */ }))

// With all middleware
import { devtools, persist, subscribeWithSelector } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

const useStore = create<State>()(
  devtools(subscribeWithSelector(persist(immer((set, get) => ({
    // state + actions (can mutate with immer)
  })), { name: 'key' })), { name: 'StoreName' })
)

// Use in component
const value = useStore((s) => s.value)
const { a, b } = useStore(useShallow((s) => ({ a: s.a, b: s.b })))

// Use outside React
useStore.getState()
useStore.setState({ value: 42 })
useStore.subscribe((state) => console.log(state))
```
