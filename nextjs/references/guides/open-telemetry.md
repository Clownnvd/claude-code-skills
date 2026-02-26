# OpenTelemetry Instrumentation

> Source: https://nextjs.org/docs/app/guides/open-telemetry (v16.1.6)

## Quick Setup with @vercel/otel

```bash
pnpm add @vercel/otel @opentelemetry/sdk-logs @opentelemetry/api-logs @opentelemetry/instrumentation
```

```typescript
// instrumentation.ts (project root or src/)
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel({ serviceName: 'next-app' })
}
```

> File must be in project root (or `src/`), NOT inside `app/` or `pages/`.

## Manual Configuration (Node.js only)

```bash
pnpm add @opentelemetry/sdk-node @opentelemetry/resources @opentelemetry/semantic-conventions @opentelemetry/sdk-trace-node @opentelemetry/exporter-trace-otlp-http
```

```typescript
// instrumentation.ts
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./instrumentation.node.ts')
  }
}
```

```typescript
// instrumentation.node.ts
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { resourceFromAttributes } from '@opentelemetry/resources'
import { NodeSDK } from '@opentelemetry/sdk-node'
import { SimpleSpanProcessor } from '@opentelemetry/sdk-trace-node'
import { ATTR_SERVICE_NAME } from '@opentelemetry/semantic-conventions'

const sdk = new NodeSDK({
  resource: resourceFromAttributes({
    [ATTR_SERVICE_NAME]: 'next-app',
  }),
  spanProcessor: new SimpleSpanProcessor(new OTLPTraceExporter()),
})
sdk.start()
```

## Custom Spans

```bash
pnpm add @opentelemetry/api
```

```typescript
import { trace } from '@opentelemetry/api'

export async function fetchGithubStars() {
  return await trace
    .getTracer('nextjs-example')
    .startActiveSpan('fetchGithubStars', async (span) => {
      try {
        return await getValue()
      } finally {
        span.end()
      }
    })
}
```

## Default Spans

| Span | Type | Description |
|------|------|-------------|
| `[method] [route]` | `BaseServer.handleRequest` | Root span per request |
| `render route (app) [route]` | `AppRender.getBodyResult` | App Router render |
| `fetch [method] [url]` | `AppRender.fetch` | Fetch in code |
| `executing api route (app) [route]` | `AppRouteRouteHandlers.runHandler` | API route handler |
| `getServerSideProps [route]` | `Render.getServerSideProps` | Pages SSR data |
| `getStaticProps [route]` | `Render.getStaticProps` | Pages SSG data |
| `render route (pages) [route]` | `Render.renderDocument` | Pages render |
| `generateMetadata [page]` | `ResolveMetadata.generateMetadata` | Metadata generation |
| `resolve page components` | `NextNodeServer.findPageComponents` | Page component resolution |
| `resolve segment modules` | `NextNodeServer.getLayoutOrPageModule` | Layout/page module loading |
| `start response` | `NextNodeServer.startResponse` | First byte sent |

## Custom Attributes

| Attribute | Description |
|-----------|-------------|
| `next.span_name` | Duplicates span name |
| `next.span_type` | Unique span type ID |
| `next.route` | Route pattern (e.g., `/[param]/user`) |
| `next.rsc` | Whether request is RSC (true/false) |
| `next.page` | Internal value for special files |

## Environment Variables

| Variable | Effect |
|----------|--------|
| `NEXT_OTEL_VERBOSE=1` | Show all spans (more than default) |
| `NEXT_OTEL_FETCH_DISABLED=1` | Disable fetch span instrumentation |

## Deployment

| Platform | Approach |
|----------|----------|
| Vercel | `@vercel/otel` works out of the box |
| Self-hosted | Run your own OpenTelemetry Collector |
| Custom exporter | Use with `@vercel/otel` or manual config |

## Quick Reference

| Need | Solution |
|------|----------|
| Fastest setup | `@vercel/otel` + `instrumentation.ts` |
| Node.js only features | Manual `NodeSDK` in `instrumentation.node.ts` |
| Edge runtime support | Use `@vercel/otel` (not `NodeSDK`) |
| Custom traces | `@opentelemetry/api` `trace.getTracer().startActiveSpan()` |
| More spans | Set `NEXT_OTEL_VERBOSE=1` |
| Disable fetch spans | Set `NEXT_OTEL_FETCH_DISABLED=1` |
| Example project | [with-opentelemetry](https://github.com/vercel/next.js/tree/canary/examples/with-opentelemetry) |
