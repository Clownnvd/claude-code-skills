# VSCode Integration

> IntelliSense setup, NODE_ENV fix, and classRegex for clsx/cn with Tailwind CSS v4

---

## Required Extension

Install "Tailwind CSS IntelliSense" (publisher: `bradlc.vscode-tailwindcss`).

## Activation Requirements for v4

The extension requires a CSS file with `@import "tailwindcss"` to activate. It scans the project and locates your root CSS file automatically.

## VSCode Settings

```json
{
  "editor.quickSuggestions": {
    "strings": "on"
  },
  "tailwindCSS.experimental.classRegex": [
    ["clsx\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"],
    ["cn\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ],
  "tailwindCSS.includeLanguages": {
    "typescriptreact": "html"
  },
  "files.associations": {
    "*.css": "tailwindcss"
  }
}
```

## NODE_ENV Fix (Critical for Next.js + VSCode)

**Problem**: VSCode terminal sets `NODE_ENV=production`, which breaks Tailwind v4's CSS parsing in webpack dev mode.

**Fix**: Use `cross-env` in dev script:

```json
{
  "scripts": {
    "dev": "cross-env NODE_ENV=development next dev --webpack"
  },
  "dependencies": {
    "cross-env": "^7.0.3"
  }
}
```

## Restart IntelliSense

If suggestions stop working:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Run "Tailwind CSS: Restart IntelliSense Server"
3. Or "Developer: Restart Extension Host"

## File Association

Associate `.css` files with Tailwind for syntax highlighting of `@theme`, `@utility`, etc.:

```json
{
  "files.associations": {
    "*.css": "tailwindcss"
  }
}
```
