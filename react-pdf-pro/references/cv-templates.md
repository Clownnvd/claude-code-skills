# PDF Templates for CVs

---

## 6.1 Classic Layout (Single Column)

Current implementation: `src/lib/pdf/templates/classic.tsx`

```
+----------------------------------+
| NAME                             |
| Headline       email | phone     |
|----------------------------------|
| GIOI THIEU                       |
| Summary text...                  |
|                                  |
| KINH NGHIEM LAM VIEC             |
| Job Title              Date     |
| Company                          |
| * Bullet point 1                 |
| * Bullet point 2                 |
|                                  |
| HOC VAN                          |
| Institution            Date     |
| Degree - Field                   |
|                                  |
| KY NANG                          |
| Category: skill1 * skill2        |
|                                  |
| NGON NGU                         |
| Vietnamese: Native  English: B2  |
+----------------------------------+
```

Key styles: `fontFamily: "Helvetica"`, blue section titles, bordered header.

## 6.2 Modern Layout (Single Column with Accent Bar)

Current implementation: `src/lib/pdf/templates/modern.tsx`

```
+==================================+ <- 4px blue accent bar
| NAME (26pt)                      |
| Headline (sky blue)              |
| email  |  phone  |  location     |
|                                  |
| PROFILE                          |
| --- divider ---                  |
| | Summary with left border      |
|                                  |
| KINH NGHIEM                      |
| --- divider ---                  |
| Job Title              Date     |
| Company * Location               |
| > Achievement 1                  |
| > Achievement 2                  |
+----------------------------------+
```

Key styles: Sky blue accent (`#0EA5E9`), left-bordered summary, `>` bullets.

## 6.3 Creative Layout (Two-Column with Sidebar)

Current implementation: `src/lib/pdf/templates/creative.tsx`

```
+----------+------------------------+
|  SIDEBAR |  MAIN CONTENT          |
| (33%)    |  (67%)                 |
| Blue BG  |                        |
|          |  GIOI THIEU            |
| Name     |  Summary text          |
| Headline |                        |
|          |  KINH NGHIEM           |
| LIEN HE  |  Job Title     Date   |
| email    |  Company               |
| phone    |  > Bullet 1            |
| location |  > Bullet 2            |
|          |                        |
| KY NANG  |  HOC VAN               |
| [chip]   |  Institution           |
| [chip]   |  Degree                |
|          |                        |
| NGON NGU |  CHUNG CHI             |
| VN: Nat  |  Cert name             |
| EN: Flu  |  Issuer * Date         |
+----------+------------------------+
```

Key styles: Two-column flexbox (`flexDirection: "row"`), blue sidebar with white text, skill chips.

## 6.4 Template Switching Pattern (used in export route)

```ts
import { createElement } from "react"
import { ClassicTemplate } from "@/lib/pdf/templates/classic"
import { ModernTemplate } from "@/lib/pdf/templates/modern"
import { CreativeTemplate } from "@/lib/pdf/templates/creative"

const TEMPLATES = {
  classic: ClassicTemplate,
  modern: ModernTemplate,
  creative: CreativeTemplate,
} as const

// In API route:
const Template = TEMPLATES[template] || ClassicTemplate
const component = createElement(Template, { data: cvData })
const buffer = await renderToBuffer(component)
```
