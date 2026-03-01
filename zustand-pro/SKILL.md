---
name: zustand-pro
description: "Zustand v5 state management for Next.js 16. Store patterns, middleware (persist/immer/devtools), SSR hydration, CV editor multi-step wizard, 20 documented errors. Triggers: zustand, store, state management, useState replacement, global state, persist, immer."
---

# Zustand Pro -- State Management for Next.js 16

## When to Use

Trigger on any mention of: zustand, global state, store, state management, persist middleware, immer, devtools, CV editor state, multi-step form state, undo/redo.

## Reference Files

Load the relevant reference file(s) based on the task:

| File | Lines | Content |
|------|-------|---------|
| `references/setup.md` | ~65 | Version compatibility matrix (v4/v5), breaking changes, React 19 notes, install, project structure |
| `references/core-api.md` | ~100 | `create`, `createStore`, `useStore`, `setState`, `subscribe`, selectors |
| `references/nextjs-patterns.md` | ~190 | 3 patterns: global store, per-request context provider (SSR), hydration-safe persist, server component rules |
| `references/typescript.md` | ~115 | Basic typed store, middleware typing, slices pattern (large stores), typed selectors |
| `references/middleware.md` | ~195 | persist, devtools, immer, subscribeWithSelector, combine, composition order |
| `references/errors-001-010.md` | ~200 | ZST-001 to ZST-010: hydration, infinite re-render, server component, state sync, TS middleware, SSR storage, useShallow, devtools, persist schema, async actions |
| `references/errors-011-020.md` | ~175 | ZST-011 to ZST-020: missing provider, immer import, fast refresh, slices+middleware TS, persist+immer merge, React Compiler naming, subscribeWithSelector, setState replace, window undefined, stale closure |
| `references/cviet-patterns.md` | ~190 | Full multi-step CV editor store with devtools+subscribeWithSelector+immer, navigation, CRUD for all CV sections, AI patch, saving |
| `references/cviet-hooks.md` | ~170 | Auto-save with debounce, undo/redo (zundo), AI panel integration, unsaved changes warning |
| `references/performance.md` | ~130 | Atomic selectors, useShallow, stable action refs, transient updates, computed/derived state, selector extraction |
| `references/testing.md` | ~155 | Jest auto-reset mock, Vitest auto-reset mock, store direct testing, component testing, pre-set state testing |
| `references/anti-patterns.md` | ~170 | 6 anti-patterns (server component store, full store select, store in component, direct mutation, server state, missing useShallow) + 3 gotchas (middleware order, Set/Map persist, getState reactivity) |
| `references/ecosystem.md` | ~85 | Zustand vs Redux vs Jotai comparison, why Zustand for CViet, third-party middleware (zundo, zustand-computed, zukeeper), key links, quick reference card |

## Error Quick Lookup

| ID | Error | Fix |
|----|-------|-----|
| ZST-001 | Hydration mismatch with persist | `skipHydration` + `useHydratedStore` hook |
| ZST-002 | Infinite re-render (v5) | Use `useShallow` or stable selector |
| ZST-003 | Hook in Server Component | Move to Client Component with `'use client'` |
| ZST-004 | State not updating across components | Immutable update or check import path |
| ZST-005 | TypeScript error with middleware | Use curried `create<Type>()(...)` form |
| ZST-006 | Persist storage unavailable (SSR) | Guard with `typeof window` check |
| ZST-007 | `useShallow` import not found | Import from `zustand/shallow` (v5) |
| ZST-008 | DevTools not showing store | Add `devtools` middleware with `name` |
| ZST-009 | Persist overwrites new fields | Add `version` + `migrate` to persist config |
| ZST-010 | Async action not updating | Use `set()` after await, not direct mutation |
| ZST-011 | Cannot read getState (undefined) | Wrap component tree in Provider |
| ZST-012 | Immer not working | Import from `zustand/middleware/immer` |
| ZST-013 | Multiple store instances (dev) | Expected in dev; use persist for preservation |
| ZST-014 | TS error with slices + middleware | Declare middleware mutators in StateCreator |
| ZST-015 | Persist + immer deep merge conflict | Custom `merge` function with structuredClone |
| ZST-016 | React Compiler `use` prefix warning | Name stores `useXxxStore` |
| ZST-017 | subscribeWithSelector fires always | Provide `equalityFn` or stable selector |
| ZST-018 | setState replace missing fields (v5) | Provide ALL fields or use partial update |
| ZST-019 | "window is not defined" | Guard persist storage with `typeof window` |
| ZST-020 | Stale closure in useEffect | Use `subscribe` or `getState()` in effect |

## Key Patterns

### Store Creation (Next.js 16)
```tsx
// src/stores/cv-editor-store.ts
'use client'  // Not needed for store file, but consumers must be client

import { create } from 'zustand'
import { persist, devtools, immer } from 'zustand/middleware'

// Middleware order matters: devtools(persist(immer(...)))
```

### Hydration-Safe Persist
```tsx
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useStore = create(persist((...) => ({...}), {
  name: 'cv-draft',
  skipHydration: true,  // Critical for Next.js SSR
}))

// In client component:
useEffect(() => { useStore.persist.rehydrate() }, [])
```

### useShallow for Multi-Value Selectors
```tsx
import { useShallow } from 'zustand/shallow'

const { name, email } = useStore(
  useShallow((s) => ({ name: s.name, email: s.email }))
)
```

### Middleware Composition Order
```
devtools -> subscribeWithSelector -> persist -> immer -> stateCreator
```
