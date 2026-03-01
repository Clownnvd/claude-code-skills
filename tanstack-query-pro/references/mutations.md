# Mutation Patterns

---

## 5.1 useMutation -- Basic

```tsx
"use client"
import { useMutation, useQueryClient } from "@tanstack/react-query"

function CreateCVButton() {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (data: { title: string; template: string }) =>
      fetch("/api/cv", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      }).then(r => {
        if (!r.ok) throw new Error("Failed to create CV")
        return r.json() as Promise<CV>
      }),

    onMutate: (variables) => {
      // Called BEFORE mutationFn fires
      // `variables` is what was passed to mutate()
      console.log("Creating CV:", variables.title)
    },

    onSuccess: (data, variables, context) => {
      // Called on successful mutation
      // `data` is the return value of mutationFn
      queryClient.invalidateQueries({ queryKey: ["cvs"] })
    },

    onError: (error, variables, context) => {
      // Called on error
      console.error("Failed:", error.message)
    },

    onSettled: (data, error, variables, context) => {
      // Called on BOTH success and error (like finally)
      // Good place for cleanup
    },

    retry: 1,  // Retry failed mutations
  })

  return (
    <button
      onClick={() => mutation.mutate({ title: "My CV", template: "classic" })}
      disabled={mutation.isPending}
    >
      {mutation.isPending ? "Creating..." : "Create CV"}
    </button>
  )
}
```

## 5.2 mutate vs mutateAsync

```tsx
const mutation = useMutation({ mutationFn: createCV })

// mutate: fire-and-forget, handles errors via onError callback
mutation.mutate(data)

// mutateAsync: returns Promise, allows try/catch
try {
  const cv = await mutation.mutateAsync(data)
  router.push(`/cv/${cv.id}`)
} catch (error) {
  // Handle error
}
```

**Rule of thumb**: Use `mutate` for simple side effects; use `mutateAsync` when you need the result for navigation or chaining.

## 5.3 Optimistic Updates -- Via UI (Simple)

Leverage `variables` from the mutation result to update the UI optimistically without touching the cache.

```tsx
function CVList() {
  const queryClient = useQueryClient()

  const deleteMutation = useMutation({
    mutationFn: (id: string) => fetch(`/api/cv/${id}`, { method: "DELETE" }),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["cvs"] })
    },
  })

  const { data: cvs = [] } = useQuery({ queryKey: ["cvs"], queryFn: fetchCVs })

  // Filter out the "optimistically deleted" CV
  const visibleCVs = cvs.filter(cv => !deleteMutation.variables || cv.id !== deleteMutation.variables)

  return visibleCVs.map(cv => (
    <CVCard
      key={cv.id}
      cv={cv}
      onDelete={() => deleteMutation.mutate(cv.id)}
    />
  ))
}
```

## 5.4 Optimistic Updates -- Via Cache (Full Control)

```tsx
function useUpdateCVTitle() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, title }: { id: string; title: string }) =>
      fetch(`/api/cv/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
      }).then(r => r.json()),

    onMutate: async ({ id, title }) => {
      // 1. Cancel outgoing refetches (so they don't overwrite our optimistic update)
      await queryClient.cancelQueries({ queryKey: ["cvs"] })

      // 2. Snapshot the previous value (for rollback)
      const previousCVs = queryClient.getQueryData<CV[]>(["cvs"])

      // 3. Optimistically update the cache
      queryClient.setQueryData<CV[]>(["cvs"], (old) =>
        old?.map(cv => cv.id === id ? { ...cv, title } : cv)
      )

      // 4. Return context with snapshot
      return { previousCVs }
    },

    onError: (err, variables, context) => {
      // Rollback to previous value on error
      if (context?.previousCVs) {
        queryClient.setQueryData(["cvs"], context.previousCVs)
      }
    },

    onSettled: () => {
      // Always refetch after error or success to sync with server
      queryClient.invalidateQueries({ queryKey: ["cvs"] })
    },
  })
}
```

## 5.5 Invalidation Strategies

```tsx
const queryClient = useQueryClient()

// Invalidate everything matching the prefix
queryClient.invalidateQueries({ queryKey: ["cvs"] })

// Invalidate exact key only
queryClient.invalidateQueries({ queryKey: ["cvs"], exact: true })

// Invalidate with predicate
queryClient.invalidateQueries({
  predicate: (query) => query.queryKey[0] === "cvs" && query.queryKey[1] !== "drafts",
})

// Remove from cache entirely (doesn't refetch)
queryClient.removeQueries({ queryKey: ["cvs", oldId] })

// Reset to initial state
queryClient.resetQueries({ queryKey: ["cvs"] })

// Set data directly (no refetch)
queryClient.setQueryData(["cvs", id], updatedCV)
```
