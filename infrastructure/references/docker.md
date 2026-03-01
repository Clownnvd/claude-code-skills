# Docker Deployment

> Part of: CI/CD & Deployment Reference -- Next.js 16 + Prisma + Neon (CViet)
> Stack: Next.js 16.1.6 (App Router, Webpack mode) | Prisma 6 + Neon PostgreSQL | pnpm | TypeScript

---

## 3.1 next.config.ts for Standalone Output

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'standalone',
  serverExternalPackages: ["@react-pdf/renderer"],
  compiler: {},
}

export default nextConfig
```

**IMPORTANT:** The current CViet `next.config.ts` does NOT have `output: 'standalone'`. Add it only when targeting Docker deployment. Do not add it for Vercel (Vercel handles optimization internally).

## 3.2 Multi-Stage Dockerfile

```dockerfile
# ============================================================
# Stage 1: Dependencies
# ============================================================
FROM node:22-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@10 --activate

# Copy dependency manifests
COPY package.json pnpm-lock.yaml ./

# Install dependencies (production + dev for build)
RUN pnpm install --frozen-lockfile

# ============================================================
# Stage 2: Builder
# ============================================================
FROM node:22-alpine AS builder
RUN corepack enable && corepack prepare pnpm@10 --activate
WORKDIR /app

# Copy deps from previous stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Run postinstall patches (CRITICAL for Next.js 16.1.6)
RUN node scripts/postinstall.js

# Generate Prisma client
RUN pnpm db:generate

# Build with fake DB URL (Prisma generate already done, build only needs types)
ARG DATABASE_URL="postgresql://fake:fake@localhost:5432/fake"
ARG BETTER_AUTH_SECRET="build-time-secret-not-used-at-runtime"
ARG NEXT_PUBLIC_APP_URL="http://localhost:3000"

ENV DATABASE_URL=${DATABASE_URL}
ENV BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
ENV NEXT_PUBLIC_APP_URL=${NEXT_PUBLIC_APP_URL}

RUN pnpm build

# ============================================================
# Stage 3: Runner (production)
# ============================================================
FROM node:22-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy standalone output
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Copy Prisma schema + generated client (needed at runtime)
COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma
COPY --from=builder /app/node_modules/@prisma ./node_modules/@prisma
COPY --from=builder /app/prisma ./prisma

USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
```

## 3.3 .dockerignore

```
node_modules
.next
.git
.gitignore
*.md
.env*
.vercel
.tmp
screenshots
```

## 3.4 Docker Compose (Development + Production)

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        NEXT_PUBLIC_APP_URL: ${NEXT_PUBLIC_APP_URL:-http://localhost:3000}
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - POLAR_ACCESS_TOKEN=${POLAR_ACCESS_TOKEN}
      - POLAR_WEBHOOK_SECRET=${POLAR_WEBHOOK_SECRET}
      - POLAR_PRO_PRODUCT_ID=${POLAR_PRO_PRODUCT_ID}
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - NEXT_PUBLIC_APP_URL=${NEXT_PUBLIC_APP_URL:-http://localhost:3000}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
```

## 3.5 Build & Run Commands

```bash
# Build image
docker build -t cviet:latest .

# Run with env file
docker run -p 3000:3000 --env-file .env.production cviet:latest

# Build + run with docker compose
docker compose up -d --build

# Check image size (target: < 300MB)
docker images cviet:latest
```

## 3.6 Image Size Optimization

| Technique | Expected Savings |
|-----------|-----------------|
| Multi-stage build | ~70% reduction |
| `node:22-alpine` base | ~400MB saved vs `node:22` |
| `output: 'standalone'` | ~80% of node_modules removed |
| `.dockerignore` | Faster build context |
| Layer ordering (deps first) | Cache hits on code-only changes |

**Typical result:** 150-300MB final image (down from 1.5-2.5GB naive build).

---

> **Sources:**
> - [Optimizing Next.js Docker Images with Standalone Mode](https://dev.to/angojay/optimizing-nextjs-docker-images-with-standalone-mode-2nnh)
> - [Next.js Deploying Docs](https://nextjs.org/docs/app/getting-started/deploying)
