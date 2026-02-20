# Next.js Installation

> Source: nextjs.org/docs/app/getting-started/installation (v16.1.6)

## System Requirements

| Requirement | Minimum |
|-------------|---------|
| Node.js | 20.9+ |
| TypeScript | 5.1.0+ |
| OS | macOS, Windows (WSL), Linux |

Browsers: Chrome 111+, Edge 111+, Firefox 111+, Safari 16.4+

## Quick Start (CLI)

```bash
# pnpm (recommended)
pnpm create next-app@latest my-app --yes
cd my-app && pnpm dev

# npm
npx create-next-app@latest my-app --yes
cd my-app && npm run dev

# bun
bun create next-app@latest my-app --yes
cd my-app && bun dev
```

`--yes` skips prompts, uses defaults: TypeScript, Tailwind, ESLint, App Router, Turbopack, alias `@/*`.

## CLI Prompts (without --yes)

| Prompt | Options |
|--------|---------|
| Use recommended defaults? | Yes / Reuse previous / Customize |
| TypeScript? | Yes / No |
| Linter? | ESLint / Biome / None |
| React Compiler? | Yes / No |
| Tailwind CSS? | Yes / No |
| `src/` directory? | Yes / No |
| App Router? | Yes (recommended) / No |
| Custom import alias? | Yes / No (default `@/*`) |

## Manual Installation

```bash
pnpm i next@latest react@latest react-dom@latest
```

### Required package.json scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "lint:fix": "eslint --fix"
  }
}
```

- `next dev` — dev server (Turbopack default). Use `--webpack` for Webpack.
- `next build` — production build. No longer runs linter automatically (v16+).
- `next start` — production server.

### Minimal file structure

```
app/
├── layout.tsx    # Required root layout (must have <html> + <body>)
└── page.tsx      # Home page (/)
public/           # Optional static assets (images, fonts)
```

#### Root layout (required)

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

#### Home page

```tsx
// app/page.tsx
export default function Page() {
  return <h1>Hello, Next.js!</h1>
}
```

If root layout missing, `next dev` auto-creates it.

### Static assets

Place in `public/`. Reference from root path:

```tsx
import Image from 'next/image'
// public/profile.png → src="/profile.png"
<Image src="/profile.png" alt="Profile" width={100} height={100} />
```

## TypeScript Setup

Rename any file to `.ts`/`.tsx` → run `next dev` → auto-installs deps + creates `tsconfig.json`.

**VS Code plugin**: Cmd/Ctrl+Shift+P → "TypeScript: Select TypeScript Version" → "Use Workspace Version"

## Linting Setup

**ESLint** (recommended):
```json
{ "scripts": { "lint": "eslint", "lint:fix": "eslint --fix" } }
```

**Biome** (alternative — fast linter + formatter):
```json
{ "scripts": { "lint": "biome check", "format": "biome format --write" } }
```

Migrate from `next lint`: `npx @next/codemod@canary next-lint-to-eslint-cli .`

## Import Aliases

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": "src/",
    "paths": {
      "@/*": ["./*"],
      "@/components/*": ["components/*"],
      "@/styles/*": ["styles/*"]
    }
  }
}
```

Paths are relative to `baseUrl`.
