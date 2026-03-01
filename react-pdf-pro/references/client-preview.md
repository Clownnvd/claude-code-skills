# Client-Side Preview

---

## 8.1 PDFViewer with Dynamic Import

```tsx
"use client"

import dynamic from "next/dynamic"
import { ClassicTemplate } from "@/lib/pdf/templates/classic"
import type { CVData } from "@/types/cv"

const PDFViewer = dynamic(
  () => import("@react-pdf/renderer").then((mod) => mod.PDFViewer),
  {
    ssr: false,
    loading: () => (
      <div className="flex items-center justify-center h-[600px] bg-gray-50 rounded-lg">
        <p className="text-gray-500">Dang tai ban xem truoc...</p>
      </div>
    ),
  }
)

interface Props {
  data: CVData
}

export function CVPreview({ data }: Props) {
  return (
    <PDFViewer width="100%" height={700} showToolbar={false}>
      <ClassicTemplate data={data} />
    </PDFViewer>
  )
}
```

## 8.2 usePDF Hook for Download Button

```tsx
"use client"

import { usePDF } from "@react-pdf/renderer"
import { ClassicTemplate } from "@/lib/pdf/templates/classic"
import type { CVData } from "@/types/cv"

export function DownloadButton({ data }: { data: CVData }) {
  const [instance, updateInstance] = usePDF({
    document: <ClassicTemplate data={data} />,
  })

  if (instance.loading) return <button disabled>Dang tao...</button>
  if (instance.error) return <p>Loi: {instance.error}</p>

  return (
    <a
      href={instance.url!}
      download="cv.pdf"
      className="bg-[#1B4FD8] text-white px-4 py-2 rounded-lg"
    >
      Tai xuong PDF
    </a>
  )
}
```

**Note:** `usePDF` does NOT auto-update when `data` changes. Call `updateInstance(<ClassicTemplate data={newData} />)` to regenerate.

## 8.3 PDFDownloadLink (Simpler Alternative)

```tsx
"use client"

import dynamic from "next/dynamic"

const PDFDownloadLink = dynamic(
  () => import("@react-pdf/renderer").then((mod) => mod.PDFDownloadLink),
  { ssr: false }
)

export function SimpleDownload({ data }: { data: CVData }) {
  return (
    <PDFDownloadLink
      document={<ClassicTemplate data={data} />}
      fileName="cv.pdf"
    >
      {({ loading }) => (loading ? "Dang tao..." : "Tai xuong")}
    </PDFDownloadLink>
  )
}
```
