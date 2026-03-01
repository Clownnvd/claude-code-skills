# Version Compatibility & Installation Setup

> TanStack Query: v5.90+ | React: 19.x | Next.js: 16.x | Date: 2026-02-27

---

## 1. Version Compatibility

### Verified Stack

| Package | Version | Notes |
|---------|---------|-------|
| `@tanstack/react-query` | `^5.90.21` | Core library |
| `@tanstack/react-query-devtools` | `^5.91.3` | Dev-only debugging UI |
| `@tanstack/react-query-next-experimental` | `^5.x` | Optional: streaming SSR without manual prefetch |
| `react` | `19.2.3` | Full React 19 support in TQ v5 |
| `next` | `16.1.6` | App Router with `proxy.ts` (replaces `middleware.ts`) |
| `typescript` | `^5` | Required for v5 type inference |

### v5 Breaking Changes from v4

| Change | v4 | v5 |
|--------|----|----|
| Hook API | Multiple overloads | Single object argument only |
| Loading status | `status: 'loading'` / `isLoading` | `status: 'pending'` / `isPending` |
| Cache time | `cacheTime` | `gcTime` (garbage collection time) |
| Keep previous data | `keepPreviousData: true` | `placeholderData: keepPreviousData` (import from TQ) |
| Error type | `unknown` | `Error` (default type for errors) |
| Server retry | Default 3 retries | Default 0 retries on server |
| Suspense hooks | `useQuery({ suspense: true })` | Dedicated `useSuspenseQuery` hook |
| Infinite query pages | No limit | `maxPages` option available |
| Dehydration options | `dehydrateMutations` / `dehydrateQueries` booleans | `shouldDehydrateQuery` / `shouldDehydrateMutation` functions |
| Bundle size | Baseline | ~20% smaller than v4 |
| Query Options | Inline only | `queryOptions()` helper for type-safe sharing |
| Conditional queries | `enabled: false` | `skipToken` (type-safe alternative) |
| Mutation state | Per-component | `useMutationState()` -- shared across components |

### Migration Codemod

```bash
# Automated migration from v4 to v5
npx jscodeshift@latest ./src/ \
  --extensions=ts,tsx \
  --parser=tsx \
  --transform=./node_modules/@tanstack/react-query/build/codemods/v5/remove-overloads/remove-overloads.cjs
```

---

## 2. Installation & Setup

### 2.1 Install Packages

```bash
pnpm add @tanstack/react-query
pnpm add -D @tanstack/react-query-devtools
# Optional: for streaming SSR without manual prefetch
pnpm add @tanstack/react-query-next-experimental
```

### 2.2 QueryClient Provider (Client Component)

**File: `src/providers/query-provider.tsx`**

```tsx
"use client"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { ReactQueryDevtools } from "@tanstack/react-query-devtools"
import { useState } from "react"

export function QueryProvider({ children }: { children: React.ReactNode }) {
  // Create QueryClient inside useState to ensure:
  // 1. Only one instance per component lifecycle
  // 2. No data shared between users/requests on server
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,     // 1 minute -- data stays "fresh"
            gcTime: 5 * 60 * 1000,    // 5 minutes -- inactive data kept in cache
            retry: 1,                  // 1 retry on failure (0 on server by default)
            refetchOnWindowFocus: true, // Refetch stale data on tab focus
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

**IMPORTANT**: Always create `QueryClient` inside `useState` or `useRef`, never as a module-level variable. Module-level clients share state across requests in SSR and between users.

### 2.3 Root Layout Integration

**File: `src/app/layout.tsx`**

```tsx
import { QueryProvider } from "@/providers/query-provider"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body>
        <QueryProvider>
          {children}
        </QueryProvider>
      </body>
    </html>
  )
}
```

### 2.4 DevTools

DevTools are automatically excluded from production bundles (they check `process.env.NODE_ENV === 'development'`).

```tsx
import { ReactQueryDevtools } from "@tanstack/react-query-devtools"

// Inside QueryClientProvider:
<ReactQueryDevtools
  initialIsOpen={false}    // Start collapsed
  buttonPosition="bottom-left"  // Toggle button position
/>
```

**Features**:
- View all active queries, their status, and cached data
- Trigger refetches manually
- Invalidate specific queries
- View query timelines and lifecycle
- State persisted in localStorage across reloads
