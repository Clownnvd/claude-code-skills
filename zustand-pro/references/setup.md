# Setup & Version Compatibility

> Zustand version: 5.0.11 (latest as of Feb 2026) | React 19 | Next.js 16 | TypeScript 5.x

---

## 1. Version Compatibility Matrix

| Zustand | React | Next.js | TypeScript | Node.js | Notes |
|---------|-------|---------|------------|---------|-------|
| 5.0.11 (latest) | 18+ / 19 | 13+ / 14 / 15 / 16 | 4.5+ | 16+ | Recommended for CViet |
| 5.0.0 | 18+ | 13+ | 4.5+ | 16+ | Initial v5 release |
| 4.5.x | 16.8+ / 17 / 18 / 19 | 12+ | 3.5+ | 12+ | Legacy, still maintained |

### Zustand v5 Breaking Changes Summary

| Change | v4 Behavior | v5 Behavior | Migration |
|--------|------------|------------|-----------|
| Default export removed | `import create from 'zustand'` | Named export only | `import { create } from 'zustand'` |
| React 18 minimum | React 16.8+ | React 18+ | Upgrade React |
| `use-sync-external-store` | Bundled shim | Native `useSyncExternalStore` | Peer dep: `react >= 18` |
| Selector equality | Custom equality in `create()` | Use `createWithEqualityFn` | See ZST-003 |
| New reference behavior | Selector could return new refs safely | New refs may cause infinite loops | Use `useShallow` |
| `setState` replace flag | `setState({}, true)` allowed empty | Must provide complete state | Provide full state object |
| Persist middleware | Shallow merge default | Behavioral changes in merge | Test persist stores |
| UMD/SystemJS dropped | Supported | Removed | Use ESM or CJS |
| ES5 support dropped | Supported | ES2018+ target | Update tsconfig |

### React 19 Compatibility Notes

- Zustand 5.x is **fully compatible** with React 19
- **Hook naming convention**: Stores MUST use the `use` prefix (e.g., `useEditorStore`, `useCVStore`) -- React Compiler enforces this
- React 19's improved TypeScript support makes Zustand's type-safe approach more natural
- Zustand's subscription-based model complements React 19's concurrent features
- Peer dependency warnings may appear but functionality works correctly

---

## 2. Installation & Setup

### Install (pnpm)

```bash
# Core
pnpm add zustand

# Optional middleware dependencies
pnpm add immer          # For immer middleware
pnpm add zundo          # For undo/redo (temporal middleware)

# DevTools (browser extension, not an npm package)
# Install "Redux DevTools" Chrome/Firefox extension
```

### Project Structure (CViet)

```
src/
  stores/
    cv-editor-store.ts     # CV editor form state
    ui-store.ts            # UI state (sidebar, modals, etc.)
    auth-store.ts          # Auth session state (if needed beyond Better Auth)
  providers/
    store-provider.tsx     # Optional: per-request store provider for SSR
```
