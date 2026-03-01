# Server-Side Rendering (API Routes)

---

## 7.1 renderToBuffer (Primary for CViet)

Returns a `Buffer` containing the PDF bytes.

```ts
// src/app/api/export/[id]/route.ts
import { NextRequest, NextResponse } from "next/server"
import { renderToBuffer } from "@react-pdf/renderer"
import { createElement } from "react"

export const dynamic = "force-dynamic"

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params

  // ... auth & data fetching ...

  registerFonts()  // Idempotent singleton

  // IMPORTANT: Use createElement, not JSX in .ts files
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const component: any = createElement(ClassicTemplate, { data: cvData })
  const buffer = await renderToBuffer(component)

  return new NextResponse(new Uint8Array(buffer), {
    headers: {
      "Content-Type": "application/pdf",
      "Content-Disposition": `attachment; filename="${filename}"`,
      "Content-Length": buffer.length.toString(),
    },
  })
}
```

## 7.2 renderToStream

Returns a Node.js readable stream. Better for large PDFs.

```ts
import { renderToStream } from "@react-pdf/renderer"

const stream = await renderToStream(component)

return new Response(stream as unknown as ReadableStream, {
  headers: { "Content-Type": "application/pdf" },
})
```

## 7.3 renderToFile

Saves PDF directly to disk (useful for batch generation).

```ts
import { renderToFile } from "@react-pdf/renderer"

await renderToFile(component, `/tmp/cv-${id}.pdf`)
```

## 7.4 renderToString

Returns base64-encoded string of the PDF.

```ts
import { renderToString } from "@react-pdf/renderer"

const base64String = await renderToString(component)
```

## 7.5 Key Patterns for API Routes

1. Always set `export const dynamic = "force-dynamic"` -- PDF generation cannot be statically cached.
2. Use `createElement()` instead of JSX in `.ts` files (non-TSX).
3. Cast component as `any` to bypass React 19 type mismatch with renderToBuffer.
4. Convert `Buffer` to `Uint8Array` for `NextResponse` body.
5. Register fonts BEFORE rendering (idempotent singleton pattern).
