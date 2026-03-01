# Testing Patterns

---

## 11.1 Mocking @react-pdf/renderer in Vitest

```ts
// __mocks__/@react-pdf/renderer.ts
import { vi } from "vitest"

export const Document = ({ children }: any) => children
export const Page = ({ children }: any) => children
export const View = ({ children }: any) => children
export const Text = ({ children }: any) => children
export const Image = () => null
export const Link = ({ children }: any) => children
export const StyleSheet = { create: (s: any) => s }
export const Font = {
  register: vi.fn(),
  registerHyphenationCallback: vi.fn(),
  registerEmojiSource: vi.fn(),
  getRegisteredFontFamilies: vi.fn(() => []),
}
export const renderToBuffer = vi.fn(() => Promise.resolve(Buffer.from("mock-pdf")))
export const renderToStream = vi.fn()
export const renderToFile = vi.fn()
export const renderToString = vi.fn()
export const usePDF = vi.fn(() => [
  { url: "blob:mock", blob: new Blob(), loading: false, error: null },
  vi.fn(),
])

// Dynamic exports
export const PDFViewer = ({ children }: any) => children
export const PDFDownloadLink = ({ children }: any) =>
  typeof children === "function" ? children({ loading: false }) : children
export const BlobProvider = ({ children }: any) =>
  children({ blob: new Blob(), url: "blob:mock", loading: false, error: null })
```

## 11.2 Testing Template Output

```ts
// tests/pdf/classic-template.test.ts
import { describe, it, expect, vi } from "vitest"
import { renderToBuffer } from "@react-pdf/renderer"
import { createElement } from "react"
import { ClassicTemplate } from "@/lib/pdf/templates/classic"

// Use real renderer for integration tests
describe("ClassicTemplate", () => {
  it("renders without crashing", async () => {
    const data = {
      personalInfo: {
        fullName: "Nguyen Van A",
        email: "test@example.com",
      },
    }

    const component = createElement(ClassicTemplate, { data } as any)
    const buffer = await renderToBuffer(component as any)

    expect(buffer).toBeDefined()
    expect(buffer.length).toBeGreaterThan(0)
    // PDF magic bytes
    expect(buffer.toString("utf-8", 0, 5)).toBe("%PDF-")
  })
})
```

## 11.3 Testing Font Registration

```ts
import { describe, it, expect, vi } from "vitest"

vi.mock("@react-pdf/renderer", () => ({
  Font: {
    register: vi.fn(),
    registerHyphenationCallback: vi.fn(),
  },
}))

import { Font } from "@react-pdf/renderer"
import { registerFonts } from "@/lib/pdf/fonts"

describe("registerFonts", () => {
  it("registers Be Vietnam Pro font family", () => {
    registerFonts()

    expect(Font.register).toHaveBeenCalledWith(
      expect.objectContaining({
        family: "BeVietnamPro",
      })
    )
  })

  it("disables hyphenation for Vietnamese", () => {
    registerFonts()

    expect(Font.registerHyphenationCallback).toHaveBeenCalled()
  })

  it("is idempotent (only registers once)", () => {
    registerFonts()
    registerFonts()
    registerFonts()

    // Called only once due to singleton guard
    expect(Font.register).toHaveBeenCalledTimes(1)
  })
})
```

## 11.4 Testing Export API Route

```ts
// tests/api/export.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest"

// Mock dependencies
vi.mock("@/lib/auth")
vi.mock("@/lib/db")
vi.mock("@/lib/pdf/fonts")
vi.mock("@react-pdf/renderer", () => ({
  renderToBuffer: vi.fn(() => Promise.resolve(Buffer.from("%PDF-1.4 mock content"))),
  Document: ({ children }: any) => children,
  Page: ({ children }: any) => children,
  View: ({ children }: any) => children,
  Text: ({ children }: any) => children,
  StyleSheet: { create: (s: any) => s },
  Font: { register: vi.fn(), registerHyphenationCallback: vi.fn() },
}))

describe("GET /api/export/[id]", () => {
  it("returns PDF with correct headers", async () => {
    // ... setup mocks, call route handler, assert response
  })

  it("returns 401 for unauthenticated requests", async () => {
    // ...
  })

  it("returns 403 for non-owner access", async () => {
    // ...
  })
})
```

## 11.5 Visual Regression Testing

Use `react-pdf-testing-library` for snapshot testing:

```bash
pnpm add -D react-pdf-testing-library jest-image-snapshot
```

```ts
import { renderDocument } from "react-pdf-testing-library"

it("matches visual snapshot", async () => {
  const { pages } = await renderDocument(<ClassicTemplate data={mockData} />)

  expect(pages).toHaveLength(1)
  expect(pages[0]).toMatchImageSnapshot()
})
```
