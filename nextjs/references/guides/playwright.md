# Playwright

> Source: nextjs.org/docs/app/guides/testing/playwright (v16.1.6)

## Overview

Playwright automates **Chromium, Firefox, and WebKit** with a single API for **E2E testing**.

## Quickstart

```bash
npx create-next-app@latest --example with-playwright with-playwright-app
```

## Manual Setup

```bash
npm init playwright
```

This creates `playwright.config.ts` and prompts for project configuration.

## E2E Test Example

```typescript
// tests/example.spec.ts
import { test, expect } from '@playwright/test'

test('should navigate to the about page', async ({ page }) => {
  await page.goto('http://localhost:3000/')
  await page.click('text=About')
  await expect(page).toHaveURL('http://localhost:3000/about')
  await expect(page.locator('h1')).toContainText('About')
})
```

> Use `baseURL: 'http://localhost:3000'` in `playwright.config.ts` to enable `page.goto("/")`.

## Running Tests

Playwright tests run against 3 browsers (Chromium, Firefox, WebKit). Requires Next.js server running:

```bash
npm run build && npm run start
# In another terminal:
npx playwright test
```

### Using `webServer`

Auto-start dev server from `playwright.config.ts`:

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: 'http://localhost:3000',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
})
```

## CI

Playwright runs in **headless mode** by default. Install dependencies for CI:

```bash
npx playwright install-deps
```

## Quick Reference

| Feature | Details |
|---------|---------|
| Test type | E2E |
| Browsers | Chromium, Firefox, WebKit |
| Install | `npm init playwright` |
| Config | `playwright.config.ts` |
| Run | `npx playwright test` |
| Headless | Default in CI |
| Auto server | `webServer` in config |
| Test location | `tests/` directory |
| CI deps | `npx playwright install-deps` |
| Example | `with-playwright` |
