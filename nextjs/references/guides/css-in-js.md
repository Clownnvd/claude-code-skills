# CSS-in-JS

> Source: https://nextjs.org/docs/app/guides/css-in-js (v16.1.6)

## Overview

CSS-in-JS requires library support for React concurrent rendering and Server Components. Only works in **Client Components** in the `app` directory.

## Supported Libraries

| Library                       | Status          |
|-------------------------------|-----------------|
| `ant-design`                  | Supported       |
| `chakra-ui`                   | Supported       |
| `@fluentui/react-components`  | Supported       |
| `kuma-ui`                     | Supported       |
| `@mui/material`               | Supported       |
| `@mui/joy`                    | Supported       |
| `pandacss`                    | Supported       |
| `styled-jsx`                  | Supported       |
| `styled-components`           | Supported       |
| `stylex`                      | Supported       |
| `tamagui`                     | Supported       |
| `tss-react`                   | Supported       |
| `vanilla-extract`             | Supported       |
| `emotion`                     | In progress     |

## Setup Pattern (3 Steps)

1. Create a **style registry** to collect CSS rules during render
2. Use `useServerInsertedHTML` hook to inject rules before content
3. Wrap app with registry Client Component during initial SSR

## styled-jsx Setup

```typescript
// app/registry.tsx
'use client'
import React, { useState } from 'react'
import { useServerInsertedHTML } from 'next/navigation'
import { StyleRegistry, createStyleRegistry } from 'styled-jsx'

export default function StyledJsxRegistry({ children }: { children: React.ReactNode }) {
  const [jsxStyleRegistry] = useState(() => createStyleRegistry())

  useServerInsertedHTML(() => {
    const styles = jsxStyleRegistry.styles()
    jsxStyleRegistry.flush()
    return <>{styles}</>
  })

  return <StyleRegistry registry={jsxStyleRegistry}>{children}</StyleRegistry>
}
```

## styled-components Setup

### 1. Enable in config

```javascript
// next.config.js
module.exports = {
  compiler: {
    styledComponents: true,
  },
}
```

### 2. Create registry

```typescript
// lib/registry.tsx
'use client'
import React, { useState } from 'react'
import { useServerInsertedHTML } from 'next/navigation'
import { ServerStyleSheet, StyleSheetManager } from 'styled-components'

export default function StyledComponentsRegistry({ children }: { children: React.ReactNode }) {
  const [styledComponentsStyleSheet] = useState(() => new ServerStyleSheet())

  useServerInsertedHTML(() => {
    const styles = styledComponentsStyleSheet.getStyleElement()
    styledComponentsStyleSheet.instance.clearTag()
    return <>{styles}</>
  })

  if (typeof window !== 'undefined') return <>{children}</>

  return (
    <StyleSheetManager sheet={styledComponentsStyleSheet.instance}>
      {children}
    </StyleSheetManager>
  )
}
```

### 3. Wrap root layout

```typescript
// app/layout.tsx
import StyledComponentsRegistry from './lib/registry'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <StyledComponentsRegistry>{children}</StyledComponentsRegistry>
      </body>
    </html>
  )
}
```

## Key Notes

- Styles extracted during SSR are flushed to `<head>` before content
- During streaming, styles from each chunk are collected and appended
- After hydration, the library takes over for dynamic styles
- Top-level Client Component for registry is most efficient

## Quick Reference

| Task                          | Solution                                         |
|-------------------------------|--------------------------------------------------|
| Enable styled-components      | `compiler.styledComponents: true` in next.config |
| Create style registry         | `useServerInsertedHTML` + library sheet API       |
| Inject into app               | Wrap `children` in root layout with registry     |
| styled-jsx version required   | v5.1.0+                                          |
| Server Components support     | CSS-in-JS only works in Client Components        |
| Emotion status                | Not yet supported (in progress)                  |
