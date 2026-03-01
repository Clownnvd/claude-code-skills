# CViet Editor Hooks & Integrations

## 8.2 Auto-Save with Debounce

```typescript
// src/hooks/use-auto-save.ts
'use client'

import { useEffect, useRef, useCallback } from 'react'
import { useCVEditorStore } from '@/stores/cv-editor-store'

const DEBOUNCE_MS = 2000

export function useAutoSave() {
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const isSaving = useCVEditorStore((s) => s.isSaving)

  const save = useCallback(async () => {
    const { cvId, cvData, isDirty, setSaving, markSaved } =
      useCVEditorStore.getState()

    if (!cvId || !isDirty || isSaving) return

    setSaving(true)
    try {
      await fetch(`/api/cv/${cvId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: cvData }),
      })
      markSaved()
    } catch (error) {
      console.error('Auto-save failed:', error)
      setSaving(false)
    }
  }, [isSaving])

  useEffect(() => {
    // Subscribe to isDirty changes
    const unsub = useCVEditorStore.subscribe(
      (state) => state.isDirty,
      (isDirty) => {
        if (!isDirty) return

        // Clear existing timer
        if (timerRef.current) clearTimeout(timerRef.current)

        // Set new debounced save
        timerRef.current = setTimeout(save, DEBOUNCE_MS)
      }
    )

    return () => {
      unsub()
      if (timerRef.current) clearTimeout(timerRef.current)
    }
  }, [save])

  // Return manual save trigger
  return { save, isSaving }
}
```

## 8.3 Undo/Redo for CV Editor (with Zundo)

```typescript
// src/stores/cv-editor-store-with-undo.ts
import { create } from 'zustand'
import { temporal } from 'zundo'
import { immer } from 'zustand/middleware/immer'
import type { CVData, EditorStep } from '@/types/cv'

interface CVEditorState {
  cvData: CVData
  currentStep: EditorStep
  updatePersonalInfo: (info: Partial<CVData['personalInfo']>) => void
  // ... other actions
}

export const useCVEditorStore = create<CVEditorState>()(
  temporal(
    immer((set) => ({
      cvData: { personalInfo: { fullName: '', email: '' } },
      currentStep: 'personal' as EditorStep,

      updatePersonalInfo: (info) =>
        set((s) => { Object.assign(s.cvData.personalInfo, info) }),
    })),
    {
      // Only track cvData changes (not UI state like currentStep)
      partialize: (state) => ({ cvData: state.cvData }),

      // Limit history to 50 entries
      limit: 50,

      // Prevent recording duplicate states
      equality: (a, b) => JSON.stringify(a) === JSON.stringify(b),
    }
  )
)

// Usage in component:
function UndoRedoButtons() {
  const { undo, redo, pastStates, futureStates } =
    useCVEditorStore.temporal.getState()

  return (
    <div className="flex gap-2">
      <button
        onClick={() => undo()}
        disabled={pastStates.length === 0}
        className="px-3 py-1 rounded border disabled:opacity-50"
      >
        Undo
      </button>
      <button
        onClick={() => redo()}
        disabled={futureStates.length === 0}
        className="px-3 py-1 rounded border disabled:opacity-50"
      >
        Redo
      </button>
    </div>
  )
}
```

## 8.4 AI Panel Integration with Store

```typescript
// Integrating AIPanel with the centralized store instead of local state:

'use client'
import { useCVEditorStore } from '@/stores/cv-editor-store'
import { useShallow } from 'zustand/shallow'

export function AIPanel({ plan, aiUsageRemaining }: { plan: 'FREE' | 'PRO'; aiUsageRemaining: number }) {
  // Select only what's needed (stable reference via useShallow)
  const { cvData, applyAIPatch } = useCVEditorStore(
    useShallow((s) => ({
      cvData: s.cvData,
      applyAIPatch: s.applyAIPatch,
    }))
  )

  async function handleEnhance() {
    const allBullets = (cvData.experience || []).flatMap(e => e.bullets).filter(Boolean)
    const res = await fetch('/api/ai/enhance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bullets: allBullets }),
    })
    const data = await res.json()

    // Apply AI results through the store
    let bulletIdx = 0
    const updatedExperience = (cvData.experience || []).map(exp => {
      const count = exp.bullets.filter(Boolean).length
      const improved = data.bullets.slice(bulletIdx, bulletIdx + count)
      bulletIdx += count
      return { ...exp, bullets: improved.length ? improved : exp.bullets }
    })
    applyAIPatch({ experience: updatedExperience })
  }

  return (
    // ... UI
  )
}
```

## 8.5 Unsaved Changes Warning

```typescript
// src/hooks/use-unsaved-warning.ts
'use client'

import { useEffect } from 'react'
import { useCVEditorStore } from '@/stores/cv-editor-store'

export function useUnsavedWarning() {
  useEffect(() => {
    const handler = (e: BeforeUnloadEvent) => {
      const isDirty = useCVEditorStore.getState().isDirty
      if (isDirty) {
        e.preventDefault()
        // Modern browsers ignore custom messages, but this still triggers the prompt
      }
    }

    window.addEventListener('beforeunload', handler)
    return () => window.removeEventListener('beforeunload', handler)
  }, [])
}
```
