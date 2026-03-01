# Environment Variable Management

## Variable Classification

| Variable | Type | Build-time? | Runtime? | Public? |
|----------|------|-------------|----------|---------|
| `DATABASE_URL` | Secret | Fake for build | Real | No |
| `BETTER_AUTH_SECRET` | Secret | Fake for build | Real | No |
| `ANTHROPIC_API_KEY` | Secret | No | Yes | No |
| `POLAR_ACCESS_TOKEN` | Secret | No | Yes | No |
| `POLAR_WEBHOOK_SECRET` | Secret | No | Yes | No |
| `POLAR_PRO_PRODUCT_ID` | Config | No | Yes | No |
| `GOOGLE_CLIENT_ID` | Secret | No | Yes | No |
| `GOOGLE_CLIENT_SECRET` | Secret | No | Yes | No |
| `NEXT_PUBLIC_APP_URL` | Config | Yes (inlined) | Yes | Yes |

## Environment Files Strategy

```
.env                    # Default values (committed, no secrets)
.env.local              # Local overrides (gitignored, contains secrets)
.env.development        # Dev defaults (committed)
.env.production         # Prod defaults (committed, no secrets)
.env.production.local   # Prod secrets (gitignored)
```

**Template for `.env.local` (gitignored):**

```env
# Database (Neon)
DATABASE_URL="postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"
DIRECT_DATABASE_URL="postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Auth
BETTER_AUTH_SECRET="your-secret-min-32-chars"
GOOGLE_CLIENT_ID="xxx.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="xxx"

# Payments (Polar)
POLAR_ACCESS_TOKEN="polar_xxx"
POLAR_WEBHOOK_SECRET="whsec_xxx"
POLAR_PRO_PRODUCT_ID="prod_xxx"

# AI
ANTHROPIC_API_KEY="sk-ant-xxx"

# App
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

## GitHub Actions Secrets

Store all secrets in GitHub repo Settings -> Secrets and Variables -> Actions:

```
VERCEL_TOKEN              # From vercel.com/account/tokens
VERCEL_ORG_ID             # From .vercel/project.json after `vercel link`
VERCEL_PROJECT_ID         # From .vercel/project.json after `vercel link`
DATABASE_URL              # Production Neon connection string
DIRECT_DATABASE_URL       # Direct Neon connection (for migrations)
NEON_PROJECT_ID           # From Neon Console
NEON_API_KEY              # From Neon Console -> API Keys
NEON_DB_USERNAME          # Your Neon database username
BETTER_AUTH_SECRET        # Production auth secret
```

## NEXT_PUBLIC_ Warning

Variables prefixed with `NEXT_PUBLIC_` are inlined into the client-side JavaScript bundle at BUILD time. This means:

1. They are visible to anyone who inspects your deployed JavaScript
2. Changing them requires a rebuild (not just a restart)
3. NEVER put secrets in `NEXT_PUBLIC_` variables
4. Preview deployments inherit `NEXT_PUBLIC_APP_URL` from build time -- if you need per-deployment URLs, use Vercel's automatic `VERCEL_URL` env var

```tsx
// This is safe (server-only)
const apiKey = process.env.ANTHROPIC_API_KEY

// This is embedded in client JS (visible to users)
const appUrl = process.env.NEXT_PUBLIC_APP_URL
```
