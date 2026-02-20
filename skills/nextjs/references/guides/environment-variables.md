# Environment Variables

> Source: https://nextjs.org/docs/app/guides/environment-variables (v16.1.6)

## Loading

Next.js auto-loads `.env*` files into `process.env`. Supports multiline values and `$VARIABLE` expansion.

```txt
# .env
DB_HOST=localhost
DB_USER=myuser
TWITTER_USER=nextjs
TWITTER_URL=https://x.com/$TWITTER_USER
# Escape literal $: \$
```

> `.env` files must be in the project root, **not** inside `/src`.

## Load Order

Variables are resolved top-to-bottom, first match wins:

| Priority | File | Notes |
|---|---|---|
| 1 | `process.env` | Already set in environment |
| 2 | `.env.$(NODE_ENV).local` | Per-environment local overrides |
| 3 | `.env.local` | **Skipped** when `NODE_ENV=test` |
| 4 | `.env.$(NODE_ENV)` | Per-environment defaults |
| 5 | `.env` | Base defaults |

`NODE_ENV` allowed values: `production`, `development`, `test`. Auto-set to `development` for `next dev`, `production` otherwise.

## Browser vs Server

| Prefix | Available On | Behavior |
|---|---|---|
| None | Server only | `process.env.SECRET` -- runtime value |
| `NEXT_PUBLIC_` | Server + Browser | Inlined at **build time**, frozen after build |

```txt
# .env
SECRET_KEY=server-only
NEXT_PUBLIC_APP_URL=https://example.com
```

### Dynamic Lookups NOT Inlined

```ts
// These will NOT work in browser:
const key = 'NEXT_PUBLIC_URL'
process.env[key]        // undefined
const env = process.env
env.NEXT_PUBLIC_URL     // undefined
```

### Runtime Server Variables

```ts
import { connection } from 'next/server'

export default async function Page() {
  await connection() // opts into dynamic rendering
  const value = process.env.MY_VALUE // evaluated at runtime
}
```

## Loading Outside Next.js Runtime

Use `@next/env` for ORM configs, test runners, etc.:

```ts
// envConfig.ts
import { loadEnvConfig } from '@next/env'
loadEnvConfig(process.cwd())
```

```ts
// orm.config.ts
import './envConfig.ts'
export default defineConfig({
  dbCredentials: { connectionString: process.env.DATABASE_URL! },
})
```

## Test Environment

- `.env.test` loaded when `NODE_ENV=test`
- `.env.local` is **not** loaded during tests (ensures consistent results)
- `.env.test` should be committed; `.env.test.local` should not

```ts
// Jest global setup
import { loadEnvConfig } from '@next/env'
export default async () => { loadEnvConfig(process.cwd()) }
```

## Git Rules

| File | Commit? |
|---|---|
| `.env` | Yes (defaults only, no secrets) |
| `.env.example` | Yes |
| `.env.local` | No (in `.gitignore`) |
| `.env*.local` | No (in `.gitignore`) |

## Quick Reference

| Task | How |
|---|---|
| Expose to browser | Prefix with `NEXT_PUBLIC_` |
| Server-only var | No prefix, access via `process.env.VAR` |
| Reference other vars | `URL=https://x.com/$USER` |
| Runtime server var | Use dynamic rendering (`connection()`, `cookies()`, etc.) |
| Load in tests | `loadEnvConfig(process.cwd())` via `@next/env` |
| Override locally | `.env.local` (highest priority after `process.env`) |
| Escape `$` | Use `\$` |
