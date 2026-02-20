# Jest

> Source: nextjs.org/docs/app/guides/testing/jest (v16.1.6)

## Overview

Jest and React Testing Library for **Unit Testing** and **Snapshot Testing** with Next.js.

> `async` Server Components are not supported by Jest. Use E2E tests for `async` components.

## Quickstart

```bash
npx create-next-app@latest --example with-jest with-jest-app
```

## Manual Setup

### Install

```bash
npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom ts-node @types/jest
```

### Generate Config

```bash
npm init jest@latest
```

### Configure `next/jest`

```typescript
// jest.config.ts
import type { Config } from 'jest'
import nextJest from 'next/jest.js'

const createJestConfig = nextJest({
  dir: './', // path to Next.js app (loads next.config.js + .env)
})

const config: Config = {
  coverageProvider: 'v8',
  testEnvironment: 'jsdom',
  // setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
}

// Must export this way for async Next.js config loading
export default createJestConfig(config)
```

### What `next/jest` Auto-Configures

- `transform` using Next.js Compiler (SWC)
- Auto mocks: stylesheets (`.css`, `.module.css`, `.scss`), images, `next/font`
- Loads `.env` variants into `process.env`
- Ignores `node_modules` and `.next` from resolving/transforms
- Loads `next.config.js` for SWC transform flags

## Custom Matchers

```typescript
// jest.config.ts — add to config:
setupFilesAfterEnv: ['<rootDir>/jest.setup.ts']
```

```typescript
// jest.setup.ts
import '@testing-library/jest-dom'
```

Provides matchers like `.toBeInTheDocument()`, `.toHaveTextContent()`, etc.

## Module Path Aliases

Match `tsconfig.json` paths in `jest.config.ts`:

```typescript
// tsconfig.json: "paths": { "@/components/*": ["components/*"] }
// jest.config.ts — add to config:
moduleNameMapper: {
  '^@/components/(.*)$': '<rootDir>/components/$1',
}
```

## Scripts

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch"
  }
}
```

## Example Tests

### Unit Test

```tsx
// __tests__/page.test.tsx
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import Page from '../app/page'

describe('Page', () => {
  it('renders a heading', () => {
    render(<Page />)
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeInTheDocument()
  })
})
```

### Snapshot Test

```tsx
// __tests__/snapshot.test.tsx
import { render } from '@testing-library/react'
import Page from '../app/page'

it('renders homepage unchanged', () => {
  const { container } = render(<Page />)
  expect(container).toMatchSnapshot()
})
```

## Quick Reference

| Feature | Details |
|---------|---------|
| Test types | Unit + Snapshot |
| Install | `jest jest-environment-jsdom @testing-library/react` |
| Config | `jest.config.ts` with `next/jest` |
| Run | `npx jest` or `jest --watch` |
| Test location | `__tests__/` or colocated |
| Custom matchers | `@testing-library/jest-dom` via `jest.setup.ts` |
| Path aliases | `moduleNameMapper` matching `tsconfig.json` paths |
| Server Components | Sync only (use E2E for async) |
| Example | `with-jest` |
