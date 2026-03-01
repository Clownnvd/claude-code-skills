# TypeScript Patterns

## Basic Typed Store

```typescript
import { create } from 'zustand'

interface BearState {
  bears: number
  increase: (by: number) => void
  reset: () => void
}

// The extra () is REQUIRED for TypeScript type inference with middleware
const useBearStore = create<BearState>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  reset: () => set({ bears: 0 }),
}))
```

## Typed Store with Middleware

```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

interface EditorState {
  content: string
  wordCount: number
  setContent: (content: string) => void
}

const useEditorStore = create<EditorState>()(
  devtools(
    persist(
      immer((set) => ({
        content: '',
        wordCount: 0,
        setContent: (content) =>
          set((state) => {
            state.content = content
            state.wordCount = content.split(/\s+/).filter(Boolean).length
          }),
      })),
      { name: 'editor-storage' }
    ),
    { name: 'EditorStore' }
  )
)
```

## Slices Pattern (Large Stores)

```typescript
import { create, type StateCreator } from 'zustand'

// ---- Slice 1: Personal Info ----
interface PersonalSlice {
  fullName: string
  email: string
  setFullName: (name: string) => void
  setEmail: (email: string) => void
}

const createPersonalSlice: StateCreator<
  PersonalSlice & ExperienceSlice,  // Full combined state
  [],                                // Middleware mutators
  [],                                // Additional mutators
  PersonalSlice                      // This slice's interface
> = (set) => ({
  fullName: '',
  email: '',
  setFullName: (name) => set({ fullName: name }),
  setEmail: (email) => set({ email }),
})

// ---- Slice 2: Experience ----
interface ExperienceSlice {
  experiences: Array<{ company: string; role: string }>
  addExperience: (exp: { company: string; role: string }) => void
  removeExperience: (index: number) => void
}

const createExperienceSlice: StateCreator<
  PersonalSlice & ExperienceSlice,
  [],
  [],
  ExperienceSlice
> = (set) => ({
  experiences: [],
  addExperience: (exp) =>
    set((state) => ({ experiences: [...state.experiences, exp] })),
  removeExperience: (index) =>
    set((state) => ({
      experiences: state.experiences.filter((_, i) => i !== index),
    })),
})

// ---- Combined Store ----
const useCVEditorStore = create<PersonalSlice & ExperienceSlice>()((...a) => ({
  ...createPersonalSlice(...a),
  ...createExperienceSlice(...a),
}))
```

## Typed Selectors

```typescript
// Standalone typed selector (reusable)
const selectBearCount = (state: BearState) => state.bears
const selectIncrease = (state: BearState) => state.increase

function Component() {
  const bears = useBearStore(selectBearCount)
  const increase = useBearStore(selectIncrease)
}
```
