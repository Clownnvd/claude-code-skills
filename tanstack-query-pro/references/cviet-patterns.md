# CViet-Specific Patterns

---

## 12.1 Current Project Setup (As-Is)

The CViet project already has TanStack Query set up:

**Dependencies** (`package.json`):
```json
{
  "@tanstack/react-query": "^5.90.21",
  "@tanstack/react-query-devtools": "^5.91.3"
}
```

**Provider** (`src/providers/query-provider.tsx`):
```tsx
"use client"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { ReactQueryDevtools } from "@tanstack/react-query-devtools"
import { useState } from "react"

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            retry: 1,
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

**Hooks** (`src/hooks/use-cvs.ts`):
```tsx
"use client"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"

export const cvKeys = {
  all: ["cvs"] as const,
  detail: (id: string) => ["cvs", id] as const,
}

export function useCVs() {
  return useQuery({ queryKey: cvKeys.all, queryFn: fetchCVs })
}

export function useCV(id: string) {
  return useQuery({ queryKey: cvKeys.detail(id), queryFn: () => fetchCV(id), enabled: !!id })
}

export function useCreateCV() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: createCV,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: cvKeys.all }),
  })
}

export function useUpdateCV() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: updateCV,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: cvKeys.detail(data.id) })
      queryClient.invalidateQueries({ queryKey: cvKeys.all })
    },
  })
}

export function useDeleteCV() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: deleteCV,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: cvKeys.all }),
  })
}
```

## 12.2 Recommended Enhancements

### A. Expand Query Key Factory

```tsx
// src/lib/query-keys.ts
export const cvKeys = {
  all:        ["cvs"] as const,
  lists:      () => [...cvKeys.all, "list"] as const,
  list:       (filters?: { template?: string; language?: string }) =>
                [...cvKeys.lists(), filters] as const,
  details:    () => [...cvKeys.all, "detail"] as const,
  detail:     (id: string) => [...cvKeys.details(), id] as const,
}

export const aiKeys = {
  all:        ["ai"] as const,
  enhance:    (cvId: string, section: string) =>
                [...aiKeys.all, "enhance", cvId, section] as const,
  usage:      () => [...aiKeys.all, "usage"] as const,
}

export const planKeys = {
  all:        ["plan"] as const,
  current:    () => [...planKeys.all, "current"] as const,
}
```

### B. AI Enhancement Caching

```tsx
// src/hooks/use-ai-enhance.ts
"use client"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { aiKeys, cvKeys } from "@/lib/query-keys"

interface EnhanceInput {
  cvId: string
  section: string   // "summary" | "experience" | "skills"
  content: string
  language: "vi" | "en"
}

interface EnhanceResult {
  enhanced: string
  suggestions: string[]
}

export function useAIEnhance() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (input: EnhanceInput): Promise<EnhanceResult> => {
      const res = await fetch("/api/ai/enhance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
      })
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.error || "AI enhancement failed")
      }
      return res.json()
    },

    // Cache the AI result so same section re-enhance is instant
    onSuccess: (data, variables) => {
      queryClient.setQueryData(
        aiKeys.enhance(variables.cvId, variables.section),
        data
      )
    },

    // Optimistic: show "enhancing..." state
    // No cache rollback needed since we're adding data, not modifying
  })
}

// Hook to read cached AI suggestions
export function useAISuggestions(cvId: string, section: string) {
  return useQuery({
    queryKey: aiKeys.enhance(cvId, section),
    queryFn: () => null, // No auto-fetch -- populated by mutation
    enabled: false,       // Manual only
    staleTime: Infinity,  // Keep until explicitly cleared
  })
}
```

### C. Dashboard SSR Prefetch

```tsx
// src/app/(app)/dashboard/page.tsx -- Enhanced with SSR prefetch
import { dehydrate, HydrationBoundary, QueryClient } from "@tanstack/react-query"
import { auth } from "@/lib/auth"
import { prisma } from "@/lib/db"
import { cvKeys, planKeys } from "@/lib/query-keys"
import { DashboardContent } from "./dashboard-content"

async function getCVs(userId: string) {
  return prisma.cv.findMany({
    where: { userId },
    orderBy: { updatedAt: "desc" },
    select: { id: true, title: true, template: true, language: true, updatedAt: true },
  })
}

export default async function DashboardPage() {
  const session = await auth()
  if (!session?.user?.id) redirect("/login")

  const queryClient = new QueryClient()

  // Prefetch CV list and user plan in parallel
  await Promise.all([
    queryClient.prefetchQuery({
      queryKey: cvKeys.all,
      queryFn: () => getCVs(session.user.id),
    }),
    queryClient.prefetchQuery({
      queryKey: planKeys.current(),
      queryFn: () => getUserPlan(session.user.id),
    }),
  ])

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <DashboardContent />
    </HydrationBoundary>
  )
}
```

### D. CV Auto-Save with Debounced Mutation

```tsx
// src/hooks/use-cv-autosave.ts
"use client"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useRef, useCallback } from "react"
import { cvKeys } from "@/lib/query-keys"
import type { CVData } from "@/types/cv"

export function useCVAutoSave(cvId: string) {
  const queryClient = useQueryClient()
  const timeoutRef = useRef<ReturnType<typeof setTimeout>>()

  const mutation = useMutation({
    mutationFn: async (data: Partial<CVData>) => {
      const res = await fetch(`/api/cv/${cvId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data }),
      })
      if (!res.ok) throw new Error("Auto-save failed")
      return res.json()
    },
    onSuccess: (data) => {
      // Update detail cache without refetching
      queryClient.setQueryData(cvKeys.detail(cvId), data)
    },
    // Don't invalidate list on every auto-save -- too expensive
  })

  const debouncedSave = useCallback(
    (data: Partial<CVData>) => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current)
      timeoutRef.current = setTimeout(() => {
        mutation.mutate(data)
      }, 1500) // 1.5 second debounce
    },
    [mutation]
  )

  return {
    save: debouncedSave,
    isSaving: mutation.isPending,
    lastSaved: mutation.data?.updatedAt,
    error: mutation.error,
  }
}
```

### E. Billing / Plan Status

```tsx
// src/hooks/use-plan.ts
"use client"
import { useQuery } from "@tanstack/react-query"
import { planKeys } from "@/lib/query-keys"

interface UserPlan {
  plan: "free" | "pro"
  cvLimit: number
  cvCount: number
  aiUsageRemaining: number
  aiUsageLimit: number
}

export function useUserPlan() {
  return useQuery({
    queryKey: planKeys.current(),
    queryFn: async (): Promise<UserPlan> => {
      const res = await fetch("/api/user/plan")
      if (!res.ok) throw new Error("Failed to fetch plan")
      return res.json()
    },
    staleTime: 5 * 60 * 1000,  // Plan doesn't change frequently
    refetchOnWindowFocus: true,  // But check when user returns
  })
}
```
