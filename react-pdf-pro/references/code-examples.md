# Code Examples -- Core Patterns

---

## 12.1 Complete Font Registration for CViet

```ts
// src/lib/pdf/fonts.ts
import { Font } from "@react-pdf/renderer"

let registered = false

export function registerFonts() {
  if (registered) return
  registered = true

  // Disable hyphenation -- Vietnamese words must not be split
  Font.registerHyphenationCallback((word: string) => [word])

  // Be Vietnam Pro -- native Vietnamese font with full diacritic support
  Font.register({
    family: "BeVietnamPro",
    fonts: [
      {
        src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVPSTAyLFyeg_IDWvOJmVES_Hw4BX8.ttf",
        fontWeight: 400,
      },
      {
        src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HTEJm86Rbg.ttf",
        fontWeight: 500,
      },
      {
        src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HToIW86Rbg.ttf",
        fontWeight: 600,
      },
      {
        src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HSMIG86Rbg.ttf",
        fontWeight: 700,
      },
      {
        src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVNSTAyLFyeg_IDWvOJmVES_HwyNXcSZQ.ttf",
        fontWeight: 400,
        fontStyle: "italic" as const,
      },
      {
        src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVKSTAyLFyeg_IDWvOJmVES_HwyPcM3dbADcg.ttf",
        fontWeight: 700,
        fontStyle: "italic" as const,
      },
    ],
  })

  // Optional: Emoji support (requires internet at render time)
  Font.registerEmojiSource({
    format: "png",
    url: "https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/",
  })
}
```

## 12.2 Complete Export API Route

```ts
// src/app/api/export/[id]/route.ts
import { NextRequest, NextResponse } from "next/server"
import { auth } from "@/lib/auth"
import { db } from "@/lib/db"
import { headers } from "next/headers"
import { renderToBuffer } from "@react-pdf/renderer"
import { createElement } from "react"
import { CVData, CVTemplate } from "@/types/cv"
import { ClassicTemplate } from "@/lib/pdf/templates/classic"
import { ModernTemplate } from "@/lib/pdf/templates/modern"
import { CreativeTemplate } from "@/lib/pdf/templates/creative"
import { registerFonts } from "@/lib/pdf/fonts"

export const dynamic = "force-dynamic"

const TEMPLATES: Record<CVTemplate, React.ComponentType<{ data: CVData }>> = {
  classic: ClassicTemplate,
  modern: ModernTemplate,
  creative: CreativeTemplate,
}

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  // 1. Authenticate
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }

  // 2. Fetch CV
  const { id } = await params
  const cv = await db.cV.findUnique({ where: { id } })
  if (!cv) {
    return NextResponse.json({ error: "Khong tim thay CV" }, { status: 404 })
  }
  if (cv.userId !== session.user.id) {
    return NextResponse.json({ error: "Khong co quyen" }, { status: 403 })
  }

  // 3. Plan gating
  const user = await db.user.findUnique({ where: { id: session.user.id } })
  if (user?.plan === "FREE" && cv.template !== "classic") {
    return NextResponse.json(
      { error: "Nang cap Pro de su dung mau nay" },
      { status: 403 }
    )
  }

  // 4. Register fonts (idempotent)
  registerFonts()

  // 5. Render PDF
  const cvData = cv.data as unknown as CVData
  const template = (cv.template as CVTemplate) || "classic"
  const Template = TEMPLATES[template] || ClassicTemplate

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const component: any = createElement(Template, { data: cvData })
  const buffer = await renderToBuffer(component)

  // 6. Response
  const safeTitle = cv.title.replace(/[^a-zA-Z0-9\s]/g, "").replace(/\s+/g, "-")
  const filename = `${safeTitle || "cv"}.pdf`

  return new NextResponse(new Uint8Array(buffer), {
    headers: {
      "Content-Type": "application/pdf",
      "Content-Disposition": `attachment; filename="${filename}"`,
      "Content-Length": buffer.length.toString(),
    },
  })
}
```

## 12.3 CV Template with Vietnamese Font

```tsx
// src/lib/pdf/templates/classic.tsx
import { Document, Page, Text, View, StyleSheet, Link } from "@react-pdf/renderer"
import { CVData } from "@/types/cv"

const BRAND = "#1B4FD8"
const TEXT_PRIMARY = "#0F172A"
const TEXT_MUTED = "#64748B"
const BORDER = "#E2E8F0"

const styles = StyleSheet.create({
  page: {
    fontFamily: "BeVietnamPro",    // Vietnamese font
    fontSize: 9,
    color: TEXT_PRIMARY,
    padding: 40,
    lineHeight: 1.4,
  },
  header: {
    borderBottom: `2 solid ${BRAND}`,
    paddingBottom: 12,
    marginBottom: 16,
  },
  name: {
    fontSize: 22,
    fontWeight: 700,               // Uses BeVietnamPro-Bold.ttf
    color: TEXT_PRIMARY,
  },
  sectionTitle: {
    fontSize: 8,
    fontWeight: 700,
    color: BRAND,
    textTransform: "uppercase",
    letterSpacing: 1,
    borderBottom: `1 solid ${BORDER}`,
    paddingBottom: 3,
    marginBottom: 8,
    marginTop: 14,
  },
  // ... more styles
})

export function ClassicTemplate({ data }: { data: CVData }) {
  const { personalInfo, experience = [], education = [] } = data

  return (
    <Document title={`CV - ${personalInfo.fullName}`} language="vi">
      <Page size="A4" style={styles.page}>
        {/* Header with Vietnamese text */}
        <View style={styles.header}>
          <Text style={styles.name}>
            {personalInfo.fullName || "Ho va Ten"}
          </Text>
        </View>

        {/* Section with Vietnamese title */}
        {experience.length > 0 && (
          <View>
            <Text style={styles.sectionTitle}>KINH NGHIEM LAM VIEC</Text>
            {/* ... experience items */}
          </View>
        )}

        {/* Page numbers */}
        <Text
          fixed
          style={{ position: "absolute", bottom: 20, right: 40, fontSize: 7, color: TEXT_MUTED }}
          render={({ pageNumber, totalPages }) =>
            `Trang ${pageNumber} / ${totalPages}`
          }
        />
      </Page>
    </Document>
  )
}
```
