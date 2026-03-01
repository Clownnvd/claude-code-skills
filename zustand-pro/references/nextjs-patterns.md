# Next.js 16 App Router Patterns

## Pattern 1: Simple Global Store (Most Common)

For client-side-only state that does not need SSR data:

```typescript
// src/stores/ui-store.ts
'use client' // Not needed in the store file itself, but consumers must be client components

import { create } from 'zustand'

interface UIState {
  sidebarOpen: boolean
  toggleSidebar: () => void
  activeModal: string | null
  openModal: (id: string) => void
  closeModal: () => void
}

export const useUIStore = create<UIState>()((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  activeModal: null,
  openModal: (id) => set({ activeModal: id }),
  closeModal: () => set({ activeModal: null }),
}))
```

```tsx
// src/components/sidebar-toggle.tsx
'use client'

import { useUIStore } from '@/stores/ui-store'

export function SidebarToggle() {
  const toggleSidebar = useUIStore((s) => s.toggleSidebar)
  return <button onClick={toggleSidebar}>Toggle</button>
}
```

**When to use**: UI state, form state, client-side filters, theme preferences.

## Pattern 2: Per-Request Store with Context Provider (SSR-Safe)

For state that needs server-side initialization or must be isolated per request:

```typescript
// src/stores/cv-store.ts
import { createStore } from 'zustand/vanilla'
import type { CVData } from '@/types/cv'

export interface CVStoreState {
  cvData: CVData
  isDirty: boolean
  updateSection: <K extends keyof CVData>(key: K, value: CVData[K]) => void
  reset: (data: CVData) => void
}

export type CVStore = ReturnType<typeof createCVStore>

export function createCVStore(initialData: CVData) {
  return createStore<CVStoreState>()((set) => ({
    cvData: initialData,
    isDirty: false,
    updateSection: (key, value) =>
      set((state) => ({
        cvData: { ...state.cvData, [key]: value },
        isDirty: true,
      })),
    reset: (data) => set({ cvData: data, isDirty: false }),
  }))
}
```

```tsx
// src/providers/cv-store-provider.tsx
'use client'

import { createContext, useContext, useRef, type ReactNode } from 'react'
import { useStore, type StoreApi } from 'zustand'
import { createCVStore, type CVStoreState } from '@/stores/cv-store'
import type { CVData } from '@/types/cv'

const CVStoreContext = createContext<StoreApi<CVStoreState> | null>(null)

interface CVStoreProviderProps {
  children: ReactNode
  initialData: CVData
}

export function CVStoreProvider({ children, initialData }: CVStoreProviderProps) {
  const storeRef = useRef<StoreApi<CVStoreState> | null>(null)

  if (storeRef.current === null) {
    storeRef.current = createCVStore(initialData)
  }

  return (
    <CVStoreContext.Provider value={storeRef.current}>
      {children}
    </CVStoreContext.Provider>
  )
}

export function useCVStore<T>(selector: (state: CVStoreState) => T): T {
  const store = useContext(CVStoreContext)
  if (!store) {
    throw new Error('useCVStore must be used within a CVStoreProvider')
  }
  return useStore(store, selector)
}
```

```tsx
// src/app/(app)/cv/[id]/page.tsx -- Server Component
import { CVStoreProvider } from '@/providers/cv-store-provider'
import { CVEditor } from '@/components/cv/editor'
import { db } from '@/lib/db'

export default async function CVEditPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const cv = await db.cv.findUnique({ where: { id } })

  if (!cv) return <div>CV not found</div>

  return (
    <CVStoreProvider initialData={cv.data as CVData}>
      <CVEditor />
    </CVStoreProvider>
  )
}
```

**When to use**: CV editor state initialized from DB, per-page stores, SSR-hydrated state.

## Pattern 3: Hydration-Safe Persist Store

For persisted state that must work with SSR without hydration errors:

```typescript
// src/stores/preferences-store.ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

interface PreferencesState {
  theme: 'light' | 'dark'
  language: 'vi' | 'en'
  setTheme: (theme: 'light' | 'dark') => void
  setLanguage: (language: 'vi' | 'en') => void
}

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    (set) => ({
      theme: 'light',
      language: 'vi',
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'cviet-preferences',
      storage: createJSONStorage(() => localStorage),
    }
  )
)
```

```tsx
// src/hooks/use-hydrated-store.ts
'use client'

import { useState, useEffect } from 'react'

/**
 * Prevents hydration mismatch by returning default value on server
 * and actual store value only after client hydration.
 */
export function useHydratedStore<T>(
  useStoreFn: (selector: (state: any) => T) => T,
  selector: (state: any) => T,
  defaultValue: T
): T {
  const [hydrated, setHydrated] = useState(false)
  const storeValue = useStoreFn(selector)

  useEffect(() => {
    setHydrated(true)
  }, [])

  return hydrated ? storeValue : defaultValue
}
```

**Alternative: skipHydration approach**:

```typescript
export const usePreferencesStore = create<PreferencesState>()(
  persist(
    (set) => ({ /* ... */ }),
    {
      name: 'cviet-preferences',
      skipHydration: true,  // Do NOT auto-hydrate
    }
  )
)

// In a client component (e.g., root layout):
'use client'
import { useEffect } from 'react'
import { usePreferencesStore } from '@/stores/preferences-store'

export function HydrationSync() {
  useEffect(() => {
    usePreferencesStore.persist.rehydrate()
  }, [])
  return null
}
```

## Server Components: What You CANNOT Do

```tsx
// WRONG: Server Components cannot use hooks
export default async function Page() {
  // ERROR: Cannot use useStore in a Server Component
  const count = useCounterStore((s) => s.count)
}

// WRONG: Server Components cannot write to stores
export default async function Page() {
  useCounterStore.setState({ count: 5 }) // No effect on client
}

// LIMITED: getState() returns initial state only (no reactivity)
export default async function Page() {
  const state = useCounterStore.getState() // Only default values
  return <p>{state.count}</p> // Always 0
}
```

**Rule**: Zustand stores live on the client. Server Components fetch data and pass it to Client Components, which initialize or hydrate stores.
