# Testing Patterns

## 10.1 Jest Setup -- Auto-Reset Stores

```typescript
// src/__mocks__/zustand.ts
import * as zustand from 'zustand'
import { act } from '@testing-library/react'

const { create: actualCreate, createStore: actualCreateStore } =
  jest.requireActual<typeof zustand>('zustand')

// Track all store resets
const storeResetFns = new Set<() => void>()

// Wrap create to capture initial state
const create = (<T>(stateCreator: zustand.StateCreator<T>) => {
  const store = actualCreate(stateCreator)
  const initialState = store.getInitialState()
  storeResetFns.add(() => {
    store.setState(initialState, true)
  })
  return store
}) as typeof zustand.create

// Same for createStore
const createStore = (<T>(stateCreator: zustand.StateCreator<T>) => {
  const store = actualCreateStore(stateCreator)
  const initialState = store.getInitialState()
  storeResetFns.add(() => {
    store.setState(initialState, true)
  })
  return store
}) as typeof zustand.createStore

// Reset all stores after each test
afterEach(() => {
  act(() => {
    storeResetFns.forEach((resetFn) => resetFn())
  })
})

export { create, createStore }
```

## 10.2 Vitest Setup -- Auto-Reset Stores

```typescript
// src/__mocks__/zustand.ts
import * as zustand from 'zustand'
import { act } from '@testing-library/react'

const { create: actualCreate, createStore: actualCreateStore } =
  await vi.importActual<typeof zustand>('zustand')

const storeResetFns = new Set<() => void>()

const create = (<T>(stateCreator: zustand.StateCreator<T>) => {
  const store = actualCreate(stateCreator)
  const initialState = store.getInitialState()
  storeResetFns.add(() => {
    store.setState(initialState, true)
  })
  return store
}) as typeof zustand.create

const createStore = (<T>(stateCreator: zustand.StateCreator<T>) => {
  const store = actualCreateStore(stateCreator)
  const initialState = store.getInitialState()
  storeResetFns.add(() => {
    store.setState(initialState, true)
  })
  return store
}) as typeof zustand.createStore

afterEach(() => {
  act(() => {
    storeResetFns.forEach((resetFn) => resetFn())
  })
})

export { create, createStore }
```

**Important:** The `__mocks__` directory must be a sibling of `node_modules` or inside `src/` (not nested deeper).

## 10.3 Testing a Store Directly

```typescript
import { useCVEditorStore } from '@/stores/cv-editor-store'

describe('CV Editor Store', () => {
  it('should initialize with empty state', () => {
    const state = useCVEditorStore.getState()
    expect(state.cvData.personalInfo.fullName).toBe('')
    expect(state.currentStep).toBe('personal')
    expect(state.isDirty).toBe(false)
  })

  it('should update personal info and mark dirty', () => {
    useCVEditorStore.getState().updatePersonalInfo({ fullName: 'Nguyen Van A' })

    const state = useCVEditorStore.getState()
    expect(state.cvData.personalInfo.fullName).toBe('Nguyen Van A')
    expect(state.isDirty).toBe(true)
  })

  it('should navigate steps correctly', () => {
    const store = useCVEditorStore

    store.getState().nextStep()
    expect(store.getState().currentStep).toBe('experience')
    expect(store.getState().completedSteps.has('personal')).toBe(true)

    store.getState().prevStep()
    expect(store.getState().currentStep).toBe('personal')
  })

  it('should add and remove experience', () => {
    const store = useCVEditorStore

    store.getState().addExperience({
      id: '1',
      jobTitle: 'Software Engineer',
      company: 'FPT',
      startDate: '2024-01',
      bullets: ['Built stuff'],
    })

    expect(store.getState().cvData.experience).toHaveLength(1)

    store.getState().removeExperience('1')
    expect(store.getState().cvData.experience).toHaveLength(0)
  })
})
```

## 10.4 Testing Components with Store

```tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { useCVEditorStore } from '@/stores/cv-editor-store'
import { NameField } from '@/components/cv/name-field'

describe('NameField', () => {
  it('should update store on input change', () => {
    render(<NameField />)

    const input = screen.getByRole('textbox')
    fireEvent.change(input, { target: { value: 'Tran Thi B' } })

    expect(useCVEditorStore.getState().cvData.personalInfo.fullName).toBe('Tran Thi B')
  })
})
```

## 10.5 Testing with Pre-set State

```typescript
it('should show save indicator when dirty', () => {
  // Pre-set store state before rendering
  useCVEditorStore.setState({
    isDirty: true,
    lastSavedAt: new Date('2026-01-01'),
  })

  render(<SaveIndicator />)
  expect(screen.getByText(/unsaved/i)).toBeInTheDocument()
})
```
