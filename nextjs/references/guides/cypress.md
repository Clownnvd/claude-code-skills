# Cypress

> Source: nextjs.org/docs/app/guides/testing/cypress (v16.1.6)

## Overview

Cypress is a test runner for **E2E** and **Component Testing** with Next.js.

> Cypress < 13.6.3 doesn't support TypeScript 5 with `moduleResolution:"bundler"`. Use 13.6.3+.

## Quickstart

```bash
npx create-next-app@latest --example with-cypress with-cypress-app
```

## Manual Setup

```bash
npm install -D cypress
```

```json
// package.json
{
  "scripts": {
    "cypress:open": "cypress open"
  }
}
```

Run `npm run cypress:open` to open the Cypress testing suite. Select E2E Testing and/or Component Testing — this creates `cypress.config.ts` and `cypress/` folder.

## E2E Testing

### Config

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    setupNodeEvents(on, config) {},
    baseUrl: 'http://localhost:3000', // optional, enables cy.visit("/")
  },
})
```

### Example Test

```typescript
// cypress/e2e/app.cy.ts
describe('Navigation', () => {
  it('should navigate to the about page', () => {
    cy.visit('http://localhost:3000/')
    cy.get('a[href*="about"]').click()
    cy.url().should('include', '/about')
    cy.get('h1').contains('About')
  })
})
```

### Running E2E Tests

Requires Next.js server running. Build + start production, then run Cypress:

```bash
npm run build && npm run start
# In another terminal:
npm run cypress:open
```

Or use `start-server-and-test`:

```json
{
  "scripts": {
    "e2e": "start-server-and-test dev http://localhost:3000 \"cypress open --e2e\"",
    "e2e:headless": "start-server-and-test dev http://localhost:3000 \"cypress run --e2e\""
  }
}
```

## Component Testing

### Config

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress'

export default defineConfig({
  component: {
    devServer: {
      framework: 'next',
      bundler: 'webpack',
    },
  },
})
```

### Example Test

```tsx
// cypress/component/about.cy.tsx
import Page from '../../app/page'

describe('<Page />', () => {
  it('should render and display expected content', () => {
    cy.mount(<Page />)
    cy.get('h1').contains('Home')
    cy.get('a[href="/about"]').should('be.visible')
  })
})
```

> Cypress doesn't support Component Testing for `async` Server Components. Use E2E testing instead.

## CI Scripts

```json
{
  "scripts": {
    "e2e": "start-server-and-test dev http://localhost:3000 \"cypress open --e2e\"",
    "e2e:headless": "start-server-and-test dev http://localhost:3000 \"cypress run --e2e\"",
    "component": "cypress open --component",
    "component:headless": "cypress run --component"
  }
}
```

## Quick Reference

| Feature | Details |
|---------|---------|
| Test types | E2E + Component |
| Install | `npm install -D cypress` |
| Open | `npx cypress open` |
| Headless | `npx cypress run` |
| Config | `cypress.config.ts` |
| E2E tests | `cypress/e2e/*.cy.ts` |
| Component tests | `cypress/component/*.cy.tsx` |
| Server Components | Not supported (use E2E) |
| CI helper | `start-server-and-test` |
| Example | `with-cypress` |
