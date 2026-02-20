# Custom Server

> Source: https://nextjs.org/docs/app/guides/custom-server (v16.1.6)

A custom server lets you start Next.js programmatically for custom patterns. **Most apps do not need this** -- it disables Automatic Static Optimization and is incompatible with `standalone` output mode.

## Setup

```ts
// server.ts
import { createServer } from 'http'
import next from 'next'

const port = parseInt(process.env.PORT || '3000', 10)
const dev = process.env.NODE_ENV !== 'production'
const app = next({ dev })
const handle = app.getRequestHandler()

app.prepare().then(() => {
  createServer((req, res) => {
    handle(req, res)
  }).listen(port)

  console.log(
    `> Server listening at http://localhost:${port} as ${
      dev ? 'development' : process.env.NODE_ENV
    }`
  )
})
```

## Package Scripts

```json
{
  "scripts": {
    "dev": "node server.js",
    "build": "next build",
    "start": "NODE_ENV=production node server.js"
  }
}
```

## `next()` Options

| Option | Type | Description |
|---|---|---|
| `conf` | `Object` | Same as `next.config.js`. Default `{}` |
| `dev` | `Boolean` | Dev mode. Default `false` |
| `dir` | `String` | Project location. Default `'.'` |
| `quiet` | `Boolean` | Hide server error messages. Default `false` |
| `hostname` | `String` | Hostname the server runs behind |
| `port` | `Number` | Port the server runs behind |
| `httpServer` | `node:http#Server` | HTTP Server instance |
| `turbopack` | `Boolean` | Enable Turbopack (default) |
| `webpack` | `Boolean` | Enable webpack |

## Caveats

- `server.ts` is **not** processed by the Next.js Compiler -- must be compatible with your Node.js version
- Disables **Automatic Static Optimization**
- Incompatible with **standalone output mode** (`output: 'standalone'`)
- The returned `app` object handles requests via `app.getRequestHandler()`

## Quick Reference

| Task | How |
|---|---|
| Create custom server | `const app = next({ dev }); app.prepare()` |
| Handle requests | `app.getRequestHandler()` returns `(req, res) => void` |
| Run dev mode | `NODE_ENV !== 'production'` sets `dev: true` |
| Run production | `NODE_ENV=production node server.js` |
| Use with nodemon | See [example repo](https://github.com/vercel/next.js/tree/canary/examples/custom-server) |
