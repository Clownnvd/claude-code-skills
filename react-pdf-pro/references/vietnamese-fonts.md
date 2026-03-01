# Vietnamese Font Registration

---

## The Problem

Vietnamese uses Latin script with extensive diacritics (a, a, a, o, o, u, d) and tone marks (acute, grave, hook, tilde, dot below). The 12 built-in PDF fonts (Helvetica, Courier, Times-Roman) do **NOT** support Vietnamese characters. Text will render as `?` or gibberish.

## Solution: Register a Font with Vietnamese Support

Three recommended fonts for Vietnamese CVs:

| Font | Style | Vietnamese | License | Best For |
|------|-------|-----------|---------|----------|
| **Be Vietnam Pro** | Neo Grotesk | Full | OFL | Modern CVs, tech industry |
| **Noto Sans** | Humanist | Full | OFL | Maximum language coverage |
| **Roboto** | Neo Grotesk | Full | Apache 2.0 | Clean, Google-style |

## 3.1 Be Vietnam Pro (Recommended for CViet)

Purpose-built for Vietnamese text. 7 weights (100-900) + italics.

```ts
import { Font } from "@react-pdf/renderer"

Font.register({
  family: "BeVietnamPro",
  fonts: [
    // Thin (100)
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVNSTAyLFyeg_IDWvOJmVES_HRUNXcSZQ.ttf", fontWeight: 100 },
    // ExtraLight (200)
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HT4JG86Rbg.ttf", fontWeight: 200 },
    // Light (300)
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HScJ286Rbg.ttf", fontWeight: 300 },
    // Regular (400)
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVPSTAyLFyeg_IDWvOJmVES_Hw4BX8.ttf", fontWeight: 400 },
    // Medium (500)
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HTEJm86Rbg.ttf", fontWeight: 500 },
    // SemiBold (600)
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HToIW86Rbg.ttf", fontWeight: 600 },
    // Bold (700)
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HSMIG86Rbg.ttf", fontWeight: 700 },
    // ExtraBold (800)
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HSQI286Rbg.ttf", fontWeight: 800 },
    // Black (900)
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HS0Im86Rbg.ttf", fontWeight: 900 },
    // Italic variants
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVNSTAyLFyeg_IDWvOJmVES_HwyNXcSZQ.ttf", fontWeight: 400, fontStyle: "italic" },
    { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVKSTAyLFyeg_IDWvOJmVES_HwyPcM3dbADcg.ttf", fontWeight: 700, fontStyle: "italic" },
  ],
})
```

## 3.2 Practical Font Registration for CViet

For a CV builder, you typically need only 4 weights:

```ts
// src/lib/pdf/fonts.ts
import { Font } from "@react-pdf/renderer"

let registered = false

export function registerFonts() {
  if (registered) return
  registered = true

  // CRITICAL: Disable hyphenation for Vietnamese
  // Vietnamese words should not be broken across lines
  Font.registerHyphenationCallback((word: string) => [word])

  // Be Vietnam Pro -- purpose-built for Vietnamese text
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
        fontStyle: "italic",
      },
    ],
  })
}
```

## 3.3 Using the Font in Templates

```tsx
const styles = StyleSheet.create({
  page: {
    fontFamily: "BeVietnamPro",  // <-- Use the registered family name
    fontSize: 9,
    color: "#0F172A",
    padding: 40,
    lineHeight: 1.4,
  },
  bold: {
    fontFamily: "BeVietnamPro",
    fontWeight: 700,  // react-pdf picks the Bold TTF automatically
  },
})
```

## 3.4 Hyphenation Callback (Critical for Vietnamese)

Vietnamese words should NEVER be hyphenated. The default hyphenation algorithm does not understand Vietnamese and will break words at wrong positions.

```ts
// Return the word as-is (no hyphenation)
Font.registerHyphenationCallback((word: string) => [word])
```

## 3.5 Self-Hosting Fonts (Alternative)

For faster loading or offline support, download TTF files to `public/fonts/`:

```ts
Font.register({
  family: "BeVietnamPro",
  fonts: [
    { src: "/fonts/BeVietnamPro-Regular.ttf", fontWeight: 400 },
    { src: "/fonts/BeVietnamPro-Bold.ttf", fontWeight: 700 },
  ],
})
```

**Note:** In API routes (server-side), use absolute file system paths:

```ts
import path from "path"

const fontDir = path.join(process.cwd(), "public", "fonts")
Font.register({
  family: "BeVietnamPro",
  fonts: [
    { src: path.join(fontDir, "BeVietnamPro-Regular.ttf"), fontWeight: 400 },
    { src: path.join(fontDir, "BeVietnamPro-Bold.ttf"), fontWeight: 700 },
  ],
})
```
