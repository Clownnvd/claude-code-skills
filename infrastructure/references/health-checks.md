# Health Checks & Monitoring

> Part of: CI/CD & Deployment Reference -- Next.js 16 + Prisma + Neon (CViet)
> Stack: Next.js 16.1.6 (App Router, Webpack mode) | Prisma 6 + Neon PostgreSQL | pnpm | TypeScript

---

## 10.1 Health Check API Route

```ts
// src/app/api/health/route.ts
import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'

export const dynamic = 'force-dynamic'

export async function GET() {
  const health: Record<string, unknown> = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    version: process.env.npm_package_version || '0.1.0',
  }

  // Check database connectivity
  try {
    await prisma.$queryRaw`SELECT 1`
    health.database = 'connected'
  } catch (error) {
    health.database = 'disconnected'
    health.status = 'degraded'
  }

  const statusCode = health.status === 'ok' ? 200 : 503
  return NextResponse.json(health, { status: statusCode })
}
```

## 10.2 Lightweight Health Check (No DB)

For Docker/load balancer checks that should not hit the database:

```ts
// src/app/api/ping/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({ status: 'ok' }, { status: 200 })
}
```

## 10.3 Error Tracking with Sentry

```bash
pnpm add @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

```ts
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,           // 10% of transactions
  replaysSessionSampleRate: 0.01,  // 1% of sessions
  replaysOnErrorSampleRate: 1.0,   // 100% of error sessions
})
```

## 10.4 Web Vitals Monitoring

```tsx
// src/app/layout.tsx (or a client component)
'use client'
import { useReportWebVitals } from 'next/web-vitals'

export function WebVitals() {
  useReportWebVitals((metric) => {
    // Send to analytics service
    console.log(metric)
    // Example: send to Vercel Analytics, Google Analytics, etc.
  })
  return null
}
```

## 10.5 Uptime Monitoring Services

| Service | Free Tier | Check Interval |
|---------|-----------|---------------|
| UptimeRobot | 50 monitors | 5 min |
| Hyperping | 10 monitors | 1 min |
| Better Stack | 10 monitors | 3 min |
| Vercel Analytics | Included (Hobby) | Continuous |

**Recommended endpoints to monitor:**
- `https://cviet.vn/api/health` -- Full health (DB check)
- `https://cviet.vn/api/ping` -- Basic availability
- `https://cviet.vn` -- Landing page (user experience)
- `https://cviet.vn/login` -- Auth flow availability

## 10.6 Structured Logging (Production)

```ts
// src/lib/logger.ts
const LOG_LEVELS = { debug: 0, info: 1, warn: 2, error: 3 } as const

type LogLevel = keyof typeof LOG_LEVELS

function log(level: LogLevel, message: string, meta?: Record<string, unknown>) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    ...meta,
  }

  if (LOG_LEVELS[level] >= LOG_LEVELS[process.env.LOG_LEVEL as LogLevel || 'info']) {
    console[level === 'error' ? 'error' : level === 'warn' ? 'warn' : 'log'](
      JSON.stringify(entry)
    )
  }
}

export const logger = {
  debug: (msg: string, meta?: Record<string, unknown>) => log('debug', msg, meta),
  info: (msg: string, meta?: Record<string, unknown>) => log('info', msg, meta),
  warn: (msg: string, meta?: Record<string, unknown>) => log('warn', msg, meta),
  error: (msg: string, meta?: Record<string, unknown>) => log('error', msg, meta),
}
```

---

> **Sources:**
> - [Next.js Deploying Docs](https://nextjs.org/docs/app/getting-started/deploying)
> - [Vercel Deployments Overview](https://vercel.com/docs/deployments/overview)
