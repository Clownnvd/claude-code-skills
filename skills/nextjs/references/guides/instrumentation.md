# Instrumentation

> Source: https://nextjs.org/docs/app/guides/instrumentation (v16.1.6)

Instrumentation integrates monitoring and logging tools into your app. The `register` function runs **once** when a new Next.js server instance starts, before the server handles requests.

## Setup

Create `instrumentation.ts` in the **project root** (or `src/` if using `src` folder). Do NOT place inside `app/` or `pages/`.

```typescript
// instrumentation.ts
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel('next-app')
}
```

## Importing Files with Side Effects

Import packages inside `register` (not at top of file) to colocate side effects:

```typescript
// instrumentation.ts
export async function register() {
  await import('package-with-side-effect')
}
```

## Runtime-Specific Code

Use `NEXT_RUNTIME` env var to conditionally import code for Node.js vs Edge:

```typescript
// instrumentation.ts
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./instrumentation-node')
  }

  if (process.env.NEXT_RUNTIME === 'edge') {
    await import('./instrumentation-edge')
  }
}
```

## Quick Reference

| Item | Detail |
|------|--------|
| File | `instrumentation.ts` in project root or `src/` |
| Export | `register()` function |
| Timing | Called once per server instance, before handling requests |
| Runtimes | `NEXT_RUNTIME` = `'nodejs'` or `'edge'` |
| `pageExtensions` | If configured, update instrumentation filename to match |
| OpenTelemetry | Use `@vercel/otel` package with `registerOTel()` |
