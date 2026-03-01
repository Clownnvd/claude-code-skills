# Code Examples -- Advanced Patterns

---

## 12.4 Client-Side Live Preview with Template Switching

```tsx
"use client"

import dynamic from "next/dynamic"
import { useState } from "react"
import type { CVData, CVTemplate } from "@/types/cv"

// Dynamic import -- SSR disabled
const PDFViewer = dynamic(
  () => import("@react-pdf/renderer").then((mod) => mod.PDFViewer),
  { ssr: false, loading: () => <PreviewSkeleton /> }
)

// Template components can be imported normally (they are just React components)
import { ClassicTemplate } from "@/lib/pdf/templates/classic"
import { ModernTemplate } from "@/lib/pdf/templates/modern"
import { CreativeTemplate } from "@/lib/pdf/templates/creative"

const TEMPLATES = {
  classic: ClassicTemplate,
  modern: ModernTemplate,
  creative: CreativeTemplate,
} as const

function PreviewSkeleton() {
  return (
    <div className="w-full h-[700px] bg-gray-50 rounded-lg animate-pulse flex items-center justify-center">
      <p className="text-gray-400">Dang tai ban xem truoc...</p>
    </div>
  )
}

interface Props {
  data: CVData
  template: CVTemplate
}

export function LivePreview({ data, template }: Props) {
  const Template = TEMPLATES[template] || ClassicTemplate

  return (
    <div className="border border-[#E2E8F0] rounded-lg overflow-hidden">
      <PDFViewer
        width="100%"
        height={700}
        showToolbar={false}
      >
        <Template data={data} />
      </PDFViewer>
    </div>
  )
}
```

## 12.5 Inline Download via API Route

```tsx
"use client"

import { useState } from "react"
import { Download } from "lucide-react"

export function ExportButton({ cvId }: { cvId: string }) {
  const [loading, setLoading] = useState(false)

  const handleExport = async () => {
    setLoading(true)
    try {
      const res = await fetch(`/api/export/${cvId}`)
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error || "Export that bai")
      }

      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `cv.pdf`
      a.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error("Export error:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <button
      onClick={handleExport}
      disabled={loading}
      className="flex items-center gap-2 bg-[#1B4FD8] text-white px-4 py-2 rounded-lg
                 hover:bg-[#1543b5] transition-colors duration-200 cursor-pointer
                 disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px]"
    >
      <Download size={16} />
      {loading ? "Dang xuat..." : "Xuat PDF"}
    </button>
  )
}
```

## 12.6 Advanced: Two-Column CV with Sidebar

```tsx
import { Document, Page, Text, View, StyleSheet, Image, Svg, Path } from "@react-pdf/renderer"

const styles = StyleSheet.create({
  page: {
    fontFamily: "BeVietnamPro",
    fontSize: 9,
    flexDirection: "row",     // Two columns
  },
  sidebar: {
    width: "33%",
    backgroundColor: "#1B4FD8",
    padding: 24,
    color: "#FFFFFF",
  },
  main: {
    flex: 1,
    padding: 28,
    color: "#0F172A",
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginBottom: 12,
    objectFit: "cover",
  },
  sidebarName: {
    fontSize: 16,
    fontWeight: 700,
    color: "#FFFFFF",
    marginBottom: 4,
  },
  skillChip: {
    backgroundColor: "#1e3a8a",
    borderRadius: 4,
    paddingHorizontal: 6,
    paddingVertical: 2,
    marginBottom: 3,
    marginRight: 3,
  },
  // Decorative divider using Canvas-like element
  accentLine: {
    width: 40,
    height: 3,
    backgroundColor: "#0EA5E9",
    marginBottom: 12,
  },
})

export function TwoColumnTemplate({ data }: { data: CVData }) {
  return (
    <Document>
      <Page size="A4" style={styles.page}>
        {/* Left Sidebar */}
        <View style={styles.sidebar}>
          {data.personalInfo.avatarUrl && (
            <Image src={data.personalInfo.avatarUrl} style={styles.avatar} />
          )}
          <Text style={styles.sidebarName}>
            {data.personalInfo.fullName}
          </Text>
          <View style={styles.accentLine} />

          {/* Contact Info */}
          <View style={{ marginBottom: 16 }}>
            <Text style={{ fontSize: 7, textTransform: "uppercase", letterSpacing: 1, marginBottom: 6, color: "#DBEAFE" }}>
              THONG TIN LIEN HE
            </Text>
            {data.personalInfo.email && (
              <Text style={{ fontSize: 8, marginBottom: 3 }}>
                {data.personalInfo.email}
              </Text>
            )}
            {data.personalInfo.phone && (
              <Text style={{ fontSize: 8, marginBottom: 3 }}>
                {data.personalInfo.phone}
              </Text>
            )}
          </View>

          {/* Skills as chips */}
          {data.skillGroups?.map((group) => (
            <View key={group.id} style={{ marginBottom: 12 }}>
              <Text style={{ fontSize: 7, textTransform: "uppercase", letterSpacing: 1, marginBottom: 4, color: "#DBEAFE" }}>
                {group.category}
              </Text>
              <View style={{ flexDirection: "row", flexWrap: "wrap" }}>
                {group.skills.map((skill) => (
                  <View key={skill.id} style={styles.skillChip}>
                    <Text style={{ fontSize: 7.5 }}>{skill.name}</Text>
                  </View>
                ))}
              </View>
            </View>
          ))}
        </View>

        {/* Right Main Content */}
        <View style={styles.main}>
          {/* Experience, Education, etc. */}
        </View>
      </Page>
    </Document>
  )
}
```

---

## Quick Reference: react-pdf vs Puppeteer

| Aspect | @react-pdf/renderer | Puppeteer |
|--------|---------------------|-----------|
| **Approach** | React components to PDF | HTML/CSS to PDF via headless Chrome |
| **Bundle size** | ~2MB | ~300MB+ (includes Chromium) |
| **Speed** | Fast (sub-second for CVs) | Slower (3-4s cold start) |
| **Vietnamese** | Requires font registration | Uses system/web fonts natively |
| **Styling** | Subset of CSS (flexbox only) | Full CSS support |
| **Layout** | Flexbox only, no Grid | Full CSS Grid, Flexbox, etc. |
| **Serverless** | Works (Node.js runtime) | Difficult (Chromium too large) |
| **File size** | Compact (font subsetting) | Larger (full fonts embedded) |
| **Text quality** | Vector text (searchable) | Vector text (searchable) |
| **Best for** | CVs, invoices, reports | Complex layouts, web page screenshots |

**Verdict for CViet:** `@react-pdf/renderer` is the right choice. CVs are structured documents with predictable layouts that work well with flexbox. The font subsetting keeps file sizes small, and it runs well in serverless environments (Vercel, Railway).

---

## Sources

- [react-pdf.org](https://react-pdf.org/) -- Official documentation
- [react-pdf.org/fonts](https://react-pdf.org/fonts) -- Font registration
- [react-pdf.org/components](https://react-pdf.org/components) -- Component reference
- [react-pdf.org/styling](https://react-pdf.org/styling) -- Styling reference
- [react-pdf.org/advanced](https://react-pdf.org/advanced) -- Advanced features
- [react-pdf.org/node](https://react-pdf.org/node) -- Node.js API
- [react-pdf.org/hooks](https://react-pdf.org/hooks) -- usePDF hook
- [react-pdf.org/compatibility](https://react-pdf.org/compatibility) -- Version compatibility
- [GitHub: diegomura/react-pdf](https://github.com/diegomura/react-pdf) -- Source & issues
- [GitHub: react-pdf-dev/starter-rp-nextjs-app-router-js](https://github.com/react-pdf-dev/starter-rp-nextjs-app-router-js) -- Official Next.js starter
- [GitHub Issue #2460](https://github.com/diegomura/react-pdf/issues/2460) -- renderToBuffer in App Router
- [GitHub Issue #2756](https://github.com/diegomura/react-pdf/issues/2756) -- React 19 compatibility
- [GitHub Issue #933](https://github.com/diegomura/react-pdf/issues/933) -- Multilanguage font support
- [Be Vietnam Pro on Google Fonts](https://fonts.google.com/specimen/Be+Vietnam+Pro) -- Vietnamese font
- [google-webfonts-helper](https://gwfh.mranftl.com/fonts/be-vietnam-pro?subsets=vietnamese,latin) -- Self-hosted font URLs
- [npm: @react-pdf/renderer](https://www.npmjs.com/package/@react-pdf/renderer) -- Package info
- [npm-compare: PDF libraries](https://npm-compare.com/html-pdf,pdfkit,pdfmake,puppeteer,react-pdf,wkhtmltopdf) -- Library comparison
