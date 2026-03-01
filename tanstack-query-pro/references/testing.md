# Testing Patterns

---

## 10.1 Test Wrapper

```tsx
// src/test/test-utils.tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { render, type RenderOptions } from "@testing-library/react"

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,          // No retries in tests
        gcTime: Infinity,      // Don't garbage collect during test
        staleTime: Infinity,   // Don't trigger background refetches
      },
      mutations: {
        retry: false,
      },
    },
  })
}

export function createWrapper() {
  const queryClient = createTestQueryClient()
  return function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    )
  }
}

export function renderWithQuery(ui: React.ReactElement, options?: RenderOptions) {
  const queryClient = createTestQueryClient()
  return render(ui, {
    wrapper: ({ children }) => (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    ),
    ...options,
  })
}
```

## 10.2 Testing Hooks with renderHook

```tsx
import { renderHook, waitFor } from "@testing-library/react"
import { createWrapper } from "@/test/test-utils"
import { useCVs } from "@/hooks/use-cvs"

// Mock fetch
globalThis.fetch = vi.fn()

describe("useCVs", () => {
  it("fetches CVs successfully", async () => {
    const mockCVs = [{ id: "1", title: "Test CV" }]

    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockCVs),
    } as Response)

    const { result } = renderHook(() => useCVs(), {
      wrapper: createWrapper(),
    })

    // Initially pending
    expect(result.current.isPending).toBe(true)

    // Wait for success
    await waitFor(() => expect(result.current.isSuccess).toBe(true))

    expect(result.current.data).toEqual(mockCVs)
  })

  it("handles fetch error", async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: false,
      status: 500,
    } as Response)

    const { result } = renderHook(() => useCVs(), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isError).toBe(true))
    expect(result.current.error?.message).toBe("Failed to fetch CVs")
  })
})
```

## 10.3 Testing Mutations

```tsx
import { renderHook, waitFor, act } from "@testing-library/react"
import { createWrapper } from "@/test/test-utils"
import { useCreateCV } from "@/hooks/use-cvs"

describe("useCreateCV", () => {
  it("creates a CV and invalidates list", async () => {
    const newCV = { id: "2", title: "New CV" }

    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(newCV),
    } as Response)

    const { result } = renderHook(() => useCreateCV(), {
      wrapper: createWrapper(),
    })

    act(() => {
      result.current.mutate({ title: "New CV", template: "classic", language: "vi" })
    })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toEqual(newCV)
  })
})
```

## 10.4 Testing Components

```tsx
import { screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { renderWithQuery } from "@/test/test-utils"
import DashboardPage from "@/app/(app)/dashboard/page"

describe("DashboardPage", () => {
  it("renders CV list", async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve([
        { id: "1", title: "My CV", template: "classic", updatedAt: new Date().toISOString() },
      ]),
    } as Response)

    renderWithQuery(<DashboardPage />)

    // Loading state
    expect(screen.getByText("Dang tai...")).toBeInTheDocument()

    // Success state
    await waitFor(() => {
      expect(screen.getByText("My CV")).toBeInTheDocument()
    })
  })
})
```
