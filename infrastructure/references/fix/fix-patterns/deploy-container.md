# Fix Patterns: Production Deploy + Containerization

## Production Deploy Fixes

### Add Manual Approval Gate (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://your-app.com
    needs: [build, test]
    steps:
      - name: Deploy to production
        run: echo "Deploying..."
```

Configure in GitHub Settings > Environments > production:
- Required reviewers: 1+ team members
- Wait timer: optional delay

### Vercel Production Approval

Vercel Pro/Enterprise: Settings > Git > Production Branch Protection
- Require approval before deploying to production

### Rollback Documentation

Create `docs/runbooks/rollback.md`:
```markdown
## Rollback Procedure

### Vercel
1. Go to Vercel Dashboard > Deployments
2. Find last known good deployment
3. Click "..." > "Promote to Production"

### Docker
1. `docker pull app:previous-tag`
2. `docker-compose up -d`

### Database
1. Check if migration rollback needed
2. Run `prisma migrate resolve --rolled-back <migration>`
```

### Post-Deploy Health Check

```typescript
// scripts/smoke-test.ts
const DEPLOY_URL = process.env.DEPLOY_URL || "http://localhost:3000";

async function smokeTest() {
  const endpoints = ["/api/health", "/api/ready"];

  for (const endpoint of endpoints) {
    const res = await fetch(`${DEPLOY_URL}${endpoint}`);
    if (!res.ok) {
      console.error(`FAIL: ${endpoint} returned ${res.status}`);
      process.exit(1);
    }
    console.log(`PASS: ${endpoint} returned ${res.status}`);
  }
}

smokeTest();
```

---

## Containerization Fixes

### Optimized Multi-Stage Dockerfile (Next.js)

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
RUN corepack enable
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Stage 2: Build
FROM node:20-alpine AS builder
RUN corepack enable
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000 HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
```

### .dockerignore

```
node_modules
.next
.git
.gitignore
.env
.env.*
*.md
tests/
__tests__/
coverage/
.vscode/
.claude/
```

### docker-compose.yml (Local Dev)

```yaml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: king_template
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### Serverless (No Docker Needed)

If deploying to Vercel (serverless), containerization category weight redistributes:
- +6% to CI Pipeline
- +6% to Monitoring

Document this in scorecard as: "Containerization: N/A (serverless — weight redistributed)"
