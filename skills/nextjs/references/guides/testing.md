# Testing

> Source: https://nextjs.org/docs/app/guides/testing (v16.1.6)

Overview of testing strategies and supported tools for Next.js applications.

## Types of Tests

| Type | Purpose | Scope |
|---|---|---|
| Unit Testing | Test individual functions, hooks, or components in isolation | Single unit |
| Component Testing | Test React component rendering, props, and user event behavior | Single component |
| Integration Testing | Test how multiple units (components, hooks, functions) work together | Multiple units |
| End-to-End (E2E) | Test full user flows in a real browser-like environment | Entire application |
| Snapshot Testing | Capture rendered output and compare against saved snapshots | Component output |

## Async Server Components

`async` Server Components are new to the React ecosystem. Some tools do not fully support them yet. **Recommendation**: Use E2E testing over unit testing for `async` Server Components.

## Supported Testing Tools

| Tool | Best For | Guide |
|---|---|---|
| **Vitest** | Unit testing | `/docs/app/guides/testing/vitest` |
| **Jest** | Unit testing, snapshot testing | `/docs/app/guides/testing/jest` |
| **Playwright** | End-to-End (E2E) testing | `/docs/app/guides/testing/playwright` |
| **Cypress** | E2E and component testing | `/docs/app/guides/testing/cypress` |

## Quick Reference

| Task | Recommended Tool |
|---|---|
| Unit tests (functions, hooks) | Vitest or Jest |
| Component tests | Vitest, Jest, or Cypress Component Testing |
| Integration tests | Vitest or Jest |
| E2E tests | Playwright or Cypress |
| Snapshot tests | Jest |
| Async Server Components | E2E tests (Playwright / Cypress) |
