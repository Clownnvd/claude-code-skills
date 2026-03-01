# TypeScript Best Practices

---

## 9.1 Type Inference -- Let It Flow

```tsx
// GOOD: queryFn return type infers data type
const { data } = useQuery({
  queryKey: ["cvs"],
  queryFn: async (): Promise<CV[]> => {
    const res = await fetch("/api/cv")
    return res.json()
  },
})
// data is CV[] | undefined

// BAD: Don't add generics when inference works
const { data } = useQuery<CV[], Error>({  // Unnecessary
  queryKey: ["cvs"],
  queryFn: async () => { ... },
})
```

## 9.2 Error Types

```tsx
// Default error type is Error in v5
const { error } = useQuery({
  queryKey: ["cvs"],
  queryFn: fetchCVs,
})
// error is Error | null

// For custom error types:
class APIError extends Error {
  status: number
  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

const { error } = useQuery<CV[], APIError>({
  queryKey: ["cvs"],
  queryFn: async () => {
    const res = await fetch("/api/cv")
    if (!res.ok) throw new APIError("Failed", res.status)
    return res.json()
  },
})
// error is APIError | null
```

## 9.3 queryOptions for Type-Safe Sharing

```tsx
import { queryOptions } from "@tanstack/react-query"

// Define query factory with full type safety
export const cvQueries = {
  all: () => queryOptions({
    queryKey: ["cvs"] as const,
    queryFn: fetchCVs,
    staleTime: 60_000,
  }),
  detail: (id: string) => queryOptions({
    queryKey: ["cvs", id] as const,
    queryFn: () => fetchCV(id),
    staleTime: 5 * 60_000,
  }),
}

// In component:
const { data } = useQuery(cvQueries.detail(id))

// In server prefetch:
await queryClient.prefetchQuery(cvQueries.all())

// Type-safe cache read:
const cvs = queryClient.getQueryData(cvQueries.all().queryKey)
// cvs is CV[] | undefined
```

## 9.4 skipToken for Conditional Queries

```tsx
import { useQuery, skipToken } from "@tanstack/react-query"

function CVEditor({ id }: { id: string | undefined }) {
  const { data } = useQuery({
    queryKey: ["cvs", id ?? ""],
    queryFn: id
      ? () => fetch(`/api/cv/${id}`).then(r => r.json()) as Promise<CV>
      : skipToken,
  })
  // data is CV | undefined
  // Query is disabled when id is undefined -- type-safe!
}
```

## 9.5 Mutation Type Safety

```tsx
interface CreateCVInput {
  title: string
  template: string
  language: string
}

const mutation = useMutation({
  mutationFn: async (input: CreateCVInput): Promise<CV> => {
    const res = await fetch("/api/cv", {
      method: "POST",
      body: JSON.stringify(input),
    })
    return res.json()
  },
  onSuccess: (data) => {
    // data is CV
  },
  onError: (error) => {
    // error is Error
  },
})

// mutation.mutate() requires CreateCVInput
mutation.mutate({ title: "My CV", template: "classic", language: "vi" })
```
