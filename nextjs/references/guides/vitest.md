# Vitest

> Source: nextjs.org/docs/app/guides/testing/vitest (v16.1.6)

## Overview

Vitest and React Testing Library for **Unit Testing** with Next.js.

> `async` Server Components are not supported by Vitest. Use E2E tests for `async` components.

## Quickstart

```bash
npx create-next-app@latest --example with-vitest with-vitest-app
```

## Manual Setup

### Install

```bash
# TypeScript
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom vite-tsconfig-paths

# JavaScript (no vite-tsconfig-paths needed)
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom
```

### Configure

```typescript
// vitest.config.mts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: {
    environment: 'jsdom',
  },
})
```

### Scripts

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

`vitest` runs in **watch mode** by default.

## Example Test

```tsx
// __tests__/page.test.tsx
import { expect, test } from 'vitest'
import { render, screen } from '@testing-library/react'
import Page from '../app/page'

test('Page', () => {
  render(<Page />)
  expect(
    screen.getByRole('heading', { level: 1, name: 'Home' })
  ).toBeDefined()
})
```

> Test files can use `__tests__/` convention or be colocated in `app/` directory.

## Quick Reference

| Feature | Details |
|---------|---------|
| Test type | Unit |
| Install | `vitest @vitejs/plugin-react jsdom @testing-library/react` |
| TS support | Add `vite-tsconfig-paths` plugin |
| Config | `vitest.config.mts` |
| Run | `npx vitest` (watch mode default) |
| Test location | `__tests__/` or colocated in `app/` |
| Server Components | Sync only (use E2E for async) |
| Example | `with-vitest` |
