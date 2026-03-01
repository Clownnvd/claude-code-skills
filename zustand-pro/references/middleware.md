# Middleware Reference

## 6.1 `persist` -- localStorage / sessionStorage

```typescript
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

interface SettingsState {
  theme: 'light' | 'dark'
  fontSize: number
  setTheme: (t: 'light' | 'dark') => void
  setFontSize: (s: number) => void
}

const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      theme: 'light',
      fontSize: 14,
      setTheme: (theme) => set({ theme }),
      setFontSize: (fontSize) => set({ fontSize }),
    }),
    {
      name: 'cviet-settings', // localStorage key

      // Optional: choose storage engine
      storage: createJSONStorage(() => localStorage), // default
      // storage: createJSONStorage(() => sessionStorage),

      // Optional: persist only specific fields
      partialize: (state) => ({
        theme: state.theme,
        fontSize: state.fontSize,
        // Exclude action functions from persistence
      }),

      // Optional: version for migrations
      version: 1,

      // Optional: migrate between versions
      migrate: (persistedState: unknown, version: number) => {
        if (version === 0) {
          // Migration logic from v0 to v1
          return { ...(persistedState as any), fontSize: 14 }
        }
        return persistedState as SettingsState
      },

      // Optional: deep merge for nested objects
      merge: (persistedState, currentState) => ({
        ...currentState,
        ...(persistedState as Partial<SettingsState>),
      }),

      // Optional: hydration callbacks
      onRehydrateStorage: (state) => {
        console.log('Hydration starts')
        return (state, error) => {
          if (error) console.error('Hydration failed:', error)
          else console.log('Hydration finished')
        }
      },

      // Optional: skip automatic hydration (for SSR control)
      skipHydration: false,
    }
  )
)
```

## 6.2 `devtools` -- Redux DevTools Integration

```typescript
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

const useBearStore = create<BearState>()(
  devtools(
    (set) => ({
      bears: 0,
      increase: (by) =>
        set(
          (state) => ({ bears: state.bears + by }),
          false,           // replace = false (default)
          'bears/increase' // action name in DevTools
        ),
    }),
    {
      name: 'BearStore',  // Store name in DevTools
      enabled: process.env.NODE_ENV === 'development',
    }
  )
)
```

**Multiple stores**: Use unique `name` values to distinguish stores in DevTools.

## 6.3 `immer` -- Mutable-Style Updates

```typescript
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

interface CVEditorState {
  personalInfo: {
    fullName: string
    email: string
    phone: string
  }
  experiences: Array<{
    id: string
    company: string
    bullets: string[]
  }>
  updatePersonalField: (field: string, value: string) => void
  addBullet: (expId: string, bullet: string) => void
  removeBullet: (expId: string, bulletIndex: number) => void
}

const useCVEditorStore = create<CVEditorState>()(
  immer((set) => ({
    personalInfo: { fullName: '', email: '', phone: '' },
    experiences: [],

    // Direct mutation syntax (Immer handles immutability)
    updatePersonalField: (field, value) =>
      set((state) => {
        (state.personalInfo as any)[field] = value
      }),

    addBullet: (expId, bullet) =>
      set((state) => {
        const exp = state.experiences.find((e) => e.id === expId)
        if (exp) exp.bullets.push(bullet)
      }),

    removeBullet: (expId, bulletIndex) =>
      set((state) => {
        const exp = state.experiences.find((e) => e.id === expId)
        if (exp) exp.bullets.splice(bulletIndex, 1)
      }),
  }))
)
```

## 6.4 `subscribeWithSelector` -- Fine-Grained Subscriptions

```typescript
import { create } from 'zustand'
import { subscribeWithSelector } from 'zustand/middleware'

const useDogStore = create<DogState>()(
  subscribeWithSelector((set) => ({
    ppiaw: true,
    treats: 0,
    addTreat: () => set((state) => ({ treats: state.treats + 1 })),
  }))
)

// Subscribe to specific field changes (outside React)
const unsubPaw = useDogStore.subscribe(
  (state) => state.ppiaw,          // Selector
  (paw, prevPaw) => {              // Callback with previous value
    console.log('Paw changed:', prevPaw, '->', paw)
  },
  {
    equalityFn: Object.is,         // Custom equality (optional)
    fireImmediately: true,         // Fire on subscribe (optional)
  }
)
```

## 6.5 `combine` -- Auto-Infer Types

```typescript
import { create } from 'zustand'
import { combine } from 'zustand/middleware'

// Types are inferred from initial state + actions
const useStore = create(
  combine(
    { count: 0, text: 'hello' },  // Initial state (types inferred)
    (set) => ({
      increment: () => set((s) => ({ count: s.count + 1 })),
      setText: (text: string) => set({ text }),
    })
  )
)
```

## 6.6 Middleware Composition Order

```typescript
// Correct nesting order (outermost to innermost):
// devtools -> subscribeWithSelector -> persist -> immer -> stateCreator

const useStore = create<MyState>()(
  devtools(                          // Outermost
    subscribeWithSelector(
      persist(
        immer(                       // Innermost
          (set) => ({
            // state and actions
          })
        ),
        { name: 'my-storage' }       // persist options
      )
    ),
    { name: 'MyStore' }             // devtools options
  )
)
```
