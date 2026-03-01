# Styling Reference

---

## 5.1 StyleSheet API

```ts
import { StyleSheet } from "@react-pdf/renderer"

const styles = StyleSheet.create({
  page: { padding: 40, fontFamily: "BeVietnamPro" },
  section: { marginBottom: 10 },
})

// Usage: <View style={styles.section}>
// Array: <View style={[styles.section, { color: "red" }]}>
// Inline: <View style={{ padding: 10 }}>
```

## 5.2 Valid Units

| Unit | Description | Example |
|------|-------------|---------|
| `pt` | Points (default, 72 per inch) | `fontSize: 12` |
| `in` | Inches | `margin: "0.5in"` |
| `mm` | Millimeters | `padding: "10mm"` |
| `cm` | Centimeters | `margin: "1cm"` |
| `%` | Percentage of parent | `width: "50%"` |
| `vw` | Page width percentage | `width: "100vw"` |
| `vh` | Page height percentage | `height: "100vh"` |

## 5.3 All Supported CSS Properties

### Layout & Flexbox

```ts
{
  display: "flex",             // Only "flex" and "none" supported
  flexDirection: "row",        // "row" | "column" | "row-reverse" | "column-reverse"
  flexWrap: "wrap",            // "wrap" | "nowrap" | "wrap-reverse"
  flexFlow: "row wrap",        // Shorthand
  flex: 1,                     // Flex grow/shrink/basis shorthand
  flexGrow: 1,
  flexShrink: 0,
  flexBasis: "auto",
  justifyContent: "center",    // "flex-start" | "center" | "flex-end" | "space-between" | "space-around" | "space-evenly"
  alignItems: "center",        // "flex-start" | "center" | "flex-end" | "stretch" | "baseline"
  alignContent: "stretch",
  alignSelf: "auto",
  gap: 10,
  rowGap: 10,
  columnGap: 10,
  position: "relative",        // "relative" | "absolute"
  top: 0,
  right: 0,
  bottom: 0,
  left: 0,
  zIndex: 1,
  overflow: "hidden",          // "hidden" | "visible"
}
```

### Dimensions

```ts
{
  width: 200,
  height: 100,
  minWidth: 50,
  minHeight: 50,
  maxWidth: "100%",
  maxHeight: 300,
}
```

### Spacing (Margin & Padding)

```ts
{
  margin: 10,
  marginTop: 10,
  marginRight: 10,
  marginBottom: 10,
  marginLeft: 10,
  marginHorizontal: 10,       // left + right
  marginVertical: 10,         // top + bottom
  padding: 10,
  paddingTop: 10,
  paddingRight: 10,
  paddingBottom: 10,
  paddingLeft: 10,
  paddingHorizontal: 10,
  paddingVertical: 10,
}
```

### Colors

```ts
{
  color: "#0F172A",            // Text color
  backgroundColor: "#FAFAF8",  // Background
  opacity: 0.8,
}
```

### Text

```ts
{
  fontFamily: "BeVietnamPro",
  fontSize: 12,
  fontStyle: "normal",          // "normal" | "italic" | "oblique"
  fontWeight: 400,              // 100-900, or "thin" | "light" | "normal" | "medium" | "semibold" | "bold" | "ultrabold" | "heavy"
  letterSpacing: 1,
  lineHeight: 1.5,
  maxLines: 3,                  // Truncate after N lines
  textAlign: "left",            // "left" | "center" | "right" | "justify"
  textDecoration: "underline",  // "none" | "underline" | "line-through" | "underline line-through"
  textDecorationColor: "#000",
  textDecorationStyle: "solid", // "solid" | "dashed" | "dotted"
  textIndent: 20,
  textOverflow: "ellipsis",     // Works with maxLines
  textTransform: "uppercase",   // "uppercase" | "lowercase" | "capitalize" | "none"
}
```

### Borders

```ts
{
  // Shorthand
  border: "1 solid #E2E8F0",
  // Per-side
  borderTop: "2 solid #1B4FD8",
  borderRight: "1 solid #E2E8F0",
  borderBottom: "1 solid #E2E8F0",
  borderLeft: "3 solid #0EA5E9",
  // Individual properties
  borderColor: "#E2E8F0",
  borderStyle: "solid",         // "solid" | "dashed" | "dotted"
  borderWidth: 1,
  borderTopWidth: 2,
  borderTopColor: "#1B4FD8",
  borderTopStyle: "solid",
  // ... same for Right, Bottom, Left
  // Border radius
  borderTopLeftRadius: 4,
  borderTopRightRadius: 4,
  borderBottomRightRadius: 4,
  borderBottomLeftRadius: 4,
}
```

### Transforms

```ts
{
  transform: "rotate(45deg)",
  // OR as array:
  transform: [
    { rotate: "45deg" },
    { scale: 1.2 },
    { translateX: 10 },
    { translateY: 20 },
    { skewX: "5deg" },
  ],
  transformOrigin: "center center",  // "top left", "50% 50%", etc.
}
```

### Object Fit (Image)

```ts
{
  objectFit: "cover",            // "contain" | "cover" | "fill" | "none" | "scale-down"
  objectPosition: "center",
}
```

## 5.4 Media Queries

```ts
const styles = StyleSheet.create({
  section: {
    width: "100%",
    "@media min-width: 500": {
      width: "50%",
    },
    "@media orientation: landscape": {
      flexDirection: "row",
    },
  },
})
```

Supported: `width`, `height`, `min-width`, `max-width`, `min-height`, `max-height`, `orientation`.
