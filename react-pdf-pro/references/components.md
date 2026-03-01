# Component Reference

---

## Core Components

### Document

Root element representing the PDF document. Only accepts `<Page>` children.

```tsx
<Document
  title="CV - Nguyen Van A"
  author="CViet"
  subject="Curriculum Vitae"
  keywords="CV, Resume, Vietnam"
  creator="CViet App"
  producer="@react-pdf/renderer"
  pdfVersion="1.3"
  language="vi"
  pageMode="useNone"     // useNone | useOutlines | useThumbs | fullScreen
  pageLayout="singlePage" // singlePage | oneColumn | twoColumnLeft
  onRender={({ blob }) => console.log("PDF rendered", blob)}
>
  <Page>...</Page>
</Document>
```

### Page

Represents a single page. Supports wrapping (automatic page breaks).

```tsx
<Page
  size="A4"              // "A4" | "LETTER" | [width, height] | { width, height }
  orientation="portrait"  // "portrait" | "landscape"
  wrap={true}             // Enable auto page breaks
  dpi={72}                // Default DPI
  style={styles.page}
  debug={false}           // Show layout bounding boxes
  id="page-1"             // For internal linking
  bookmark="Section 1"    // PDF bookmarks
>
  <View>...</View>
</Page>
```

**Common Page Sizes:**

| Name | Dimensions (pt) | Use Case |
|------|-----------------|----------|
| A4 | 595.28 x 841.89 | Standard worldwide, Vietnamese CVs |
| LETTER | 612 x 792 | US standard |
| LEGAL | 612 x 1008 | US legal documents |

### View

The fundamental layout component (like `<div>`).

```tsx
<View
  wrap={true}
  fixed={false}        // If true, renders on ALL wrapped pages (headers/footers)
  style={styles.section}
  debug={false}
  render={({ pageNumber }) => (/* dynamic content */)}
>
  {children}
</View>
```

### Text

Displays text. Supports nesting for inline styling.

```tsx
<Text
  wrap={true}
  fixed={false}
  style={styles.text}
  hyphenationCallback={(word) => [word]}  // Per-element hyphenation
  orphans={2}    // Min lines at bottom of page
  widows={2}     // Min lines at top of page
  render={({ pageNumber, totalPages }) =>
    `Trang ${pageNumber} / ${totalPages}`
  }
>
  <Text style={{ fontWeight: 700 }}>Bold</Text> Normal text
</Text>
```

### Image

Renders JPG or PNG images.

```tsx
<Image
  src="https://example.com/photo.jpg"
  // OR:
  src={{ uri: "https://example.com/photo.jpg", method: "GET", headers: {}, body: "" }}
  // OR:
  src={buffer}  // Buffer or base64 string
  style={{ width: 80, height: 80, borderRadius: 40 }}
  cache={true}
  fixed={false}
/>
```

### Link

Hyperlinks -- both external URLs and internal document anchors.

```tsx
<Link src="https://linkedin.com/in/username" style={styles.link}>
  LinkedIn Profile
</Link>

{/* Internal link */}
<Link src="#skills-section">Jump to Skills</Link>
<Text id="skills-section">Skills...</Text>
```

### Note

Annotation notes in the PDF.

```tsx
<Note style={{ color: "yellow" }}>
  Review this section
</Note>
```

### Canvas

Freeform drawing (for decorative elements, charts, etc.).

```tsx
<Canvas
  style={{ width: "100%", height: 4 }}
  paint={(painter, width, height) => {
    painter
      .rect(0, 0, width, height)
      .fill("#1B4FD8")
  }}
/>
```

---

## Web-Only Components

### PDFViewer

Iframe-based live preview. **Web only -- must use dynamic import with `ssr: false`.**

```tsx
<PDFViewer
  width="100%"
  height={600}
  showToolbar={true}
  style={{ border: "1px solid #E2E8F0" }}
>
  <MyDocument data={cvData} />
</PDFViewer>
```

### PDFDownloadLink

Download button. **Web only.**

```tsx
<PDFDownloadLink
  document={<MyDocument data={cvData} />}
  fileName="cv-nguyen-van-a.pdf"
  style={{ textDecoration: "none", color: "#1B4FD8" }}
>
  {({ loading, error }) =>
    loading ? "Dang tao PDF..." : "Tai xuong PDF"
  }
</PDFDownloadLink>
```

### BlobProvider

Access blob data without rendering.

```tsx
<BlobProvider document={<MyDocument data={cvData} />}>
  {({ blob, url, loading, error }) => (
    loading ? <p>Loading...</p> : <a href={url}>Download</a>
  )}
</BlobProvider>
```

---

## SVG Components

For decorative icons and graphics in PDFs:

```tsx
import { Svg, Path, Circle, Rect, Line, G, Defs, ClipPath } from "@react-pdf/renderer"

<Svg viewBox="0 0 24 24" width={16} height={16}>
  <Path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10..." fill="#1B4FD8" />
</Svg>
```

Available SVG primitives: `Svg`, `Line`, `Polyline`, `Polygon`, `Path`, `Rect`, `Circle`, `Ellipse`, `Text` (SVG text), `Tspan`, `G`, `Stop`, `Defs`, `ClipPath`, `LinearGradient`, `RadialGradient`.
