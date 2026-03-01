# Performance Patterns

## 9.1 Atomic Selectors (Single Value)

```typescript
// BEST: Each component subscribes to exactly what it needs
function NameField() {
  const fullName = useCVEditorStore((s) => s.cvData.personalInfo.fullName)
  const updatePersonalInfo = useCVEditorStore((s) => s.updatePersonalInfo)

  return (
    <input
      value={fullName}
      onChange={(e) => updatePersonalInfo({ fullName: e.target.value })}
    />
  )
}
```

## 9.2 `useShallow` for Multiple Values

```typescript
import { useShallow } from 'zustand/shallow'

function PersonalInfoForm() {
  // Shallow comparison prevents re-render when unrelated state changes
  const { fullName, email, phone } = useCVEditorStore(
    useShallow((s) => ({
      fullName: s.cvData.personalInfo.fullName,
      email: s.cvData.personalInfo.email,
      phone: s.cvData.personalInfo.phone,
    }))
  )
  const updatePersonalInfo = useCVEditorStore((s) => s.updatePersonalInfo)

  return (
    <form>
      <input value={fullName} onChange={(e) => updatePersonalInfo({ fullName: e.target.value })} />
      <input value={email} onChange={(e) => updatePersonalInfo({ email: e.target.value })} />
      <input value={phone ?? ''} onChange={(e) => updatePersonalInfo({ phone: e.target.value })} />
    </form>
  )
}
```

## 9.3 Stable Action References

```typescript
// Actions are ALWAYS stable references -- no need for useShallow or useCallback
function SaveButton() {
  // This selector returns a function, which is a stable reference
  const save = useCVEditorStore((s) => s.markSaved)  // Never causes re-render
  return <button onClick={save}>Save</button>
}
```

## 9.4 Transient Updates (No Re-render)

For high-frequency updates that shouldn't trigger React re-renders (e.g., mouse position, scroll, animation):

```typescript
import { useRef, useEffect } from 'react'

function CursorTracker() {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Subscribe directly -- bypasses React entirely
    const unsub = usePositionStore.subscribe((state) => {
      if (ref.current) {
        ref.current.style.transform = `translate(${state.x}px, ${state.y}px)`
      }
    })
    return unsub
  }, [])

  return <div ref={ref} className="cursor-dot" />
}
```

## 9.5 Computed / Derived State

```typescript
const useCVEditorStore = create<State>()((set, get) => ({
  cvData: { /* ... */ },

  // Computed getter (recalculated on each access)
  get completionPercentage() {
    const data = get().cvData
    let filled = 0
    let total = 6
    if (data.personalInfo.fullName && data.personalInfo.email) filled++
    if (data.experience?.length) filled++
    if (data.education?.length) filled++
    if (data.skillGroups?.length) filled++
    if (data.languages?.length) filled++
    if (data.certifications?.length) filled++
    return Math.round((filled / total) * 100)
  },
}))

// Alternative: External selector (memoized per component)
const selectCompletionPct = (state: State) => {
  const data = state.cvData
  let filled = 0
  if (data.personalInfo.fullName && data.personalInfo.email) filled++
  if (data.experience?.length) filled++
  if (data.education?.length) filled++
  if (data.skillGroups?.length) filled++
  if (data.languages?.length) filled++
  if (data.certifications?.length) filled++
  return Math.round((filled / 6) * 100)
}

function ProgressBar() {
  const pct = useCVEditorStore(selectCompletionPct)
  return <div style={{ width: `${pct}%` }} className="h-2 bg-brand rounded" />
}
```

## 9.6 Avoid Selector in Render (Extract Outside)

```typescript
// BAD: Creates new function on every render
function Component() {
  const name = useStore((state) => state.name) // Fine -- simple
  const items = useStore((state) => state.items.filter(i => i.active)) // BAD -- new array every time
}

// GOOD: Define selector outside component
const selectActiveItems = (state: State) => state.items.filter(i => i.active)

function Component() {
  const items = useStore(useShallow(selectActiveItems)) // Stable with useShallow
}
```
