# SDK Compatibility & Setup Patterns

> Sections 1-2 from the Anthropic SDK reference. Covers version matrix, runtime compatibility, client initialization, env vars, and API key security.

---

## SDK Compatibility

### Version Matrix

| Component | Version | Notes |
|-----------|---------|-------|
| `@anthropic-ai/sdk` | ^0.39+ | Latest TypeScript SDK |
| Node.js | >= 20 LTS | Non-EOL versions only |
| TypeScript | >= 4.9 | Full type support |
| Next.js 16 | 16.1.6 | App Router, Route Handlers |
| Runtime | Node.js | **Not Edge Runtime** for direct SDK |

### Next.js 16 Specific Notes

- The Anthropic SDK works in **Route Handlers** (`app/api/*/route.ts`) using Node.js runtime
- Error objects **cannot cross RSC boundaries** -- catch and serialize before returning
- Streaming responses work in Route Handlers with no special handling required
- `proxy.ts` (Next.js 16's replacement for `middleware.ts`) runs on Node.js runtime, so Prisma + Anthropic both work
- No need for `serverExternalPackages` -- the SDK is pure JS/TS

### Runtime Compatibility

| Runtime | Direct SDK | Vercel AI SDK |
|---------|-----------|---------------|
| Node.js (Route Handler) | Works | Works |
| Edge Runtime | Not supported | Works via `@ai-sdk/anthropic` |
| Serverless Function | Works | Works |
| Browser | Blocked by default | N/A (server only) |

**Important**: The SDK blocks browser usage by default to prevent API key exposure. Setting `dangerouslyAllowBrowser: true` is available but **never recommended** for production.

---

## Setup Patterns

### Client Initialization

```ts
// src/lib/claude.ts
import Anthropic from "@anthropic-ai/sdk"

// The SDK auto-reads ANTHROPIC_API_KEY from env if not specified
export const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
  // maxRetries: 2,    // default: 2 retries with exponential backoff
  // timeout: 600000,  // default: 10 minutes
})

export const MODEL = "claude-sonnet-4-6" // CViet uses Sonnet for cost/quality balance
```

### Environment Variables

```env
# .env.local (NEVER commit this file)
ANTHROPIC_API_KEY=sk-ant-api03-...
```

- Prefix: `sk-ant-api03-` (API key format)
- **Never** use `NEXT_PUBLIC_` prefix -- this would expose the key to the browser
- The SDK automatically reads `ANTHROPIC_API_KEY` from `process.env` if no `apiKey` is passed

### API Key Security Checklist

- [ ] API key stored in `.env.local` only
- [ ] `.env.local` is in `.gitignore`
- [ ] No `NEXT_PUBLIC_ANTHROPIC_*` variables
- [ ] All Claude calls happen in Route Handlers or Server Actions
- [ ] `dangerouslyAllowBrowser` is **never** set to `true`
