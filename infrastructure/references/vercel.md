# Vercel Deployment

> Part of: CI/CD & Deployment Reference -- Next.js 16 + Prisma + Neon (CViet)
> Stack: Next.js 16.1.6 (App Router, Webpack mode) | Prisma 6 + Neon PostgreSQL | pnpm | TypeScript

---

## 2.1 Project Setup

```bash
# Install Vercel CLI
pnpm add -g vercel

# Link project (run from project root)
vercel link

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

## 2.2 Project Configuration (vercel.json)

For most Next.js projects, `vercel.json` is optional. Vercel auto-detects Next.js. However, for CViet-specific needs:

```json
{
  "buildCommand": "pnpm build",
  "installCommand": "pnpm install",
  "framework": "nextjs",
  "regions": ["sin1"],
  "functions": {
    "src/app/api/export/[id]/route.ts": {
      "memory": 1024,
      "maxDuration": 30
    },
    "src/app/api/ai/enhance/route.ts": {
      "memory": 512,
      "maxDuration": 60
    }
  }
}
```

**Key notes:**
- `regions`: Set to Southeast Asia (`sin1` = Singapore) for Vietnamese market. Other options: `hkg1` (Hong Kong), `icn1` (Seoul).
- `functions`: PDF export needs more memory for `@react-pdf/renderer`. AI endpoint needs longer timeout for Claude API calls.
- `installCommand`: Must be `pnpm install` (not `npm install`). Vercel auto-detects pnpm from `pnpm-lock.yaml`.

## 2.3 Environment Variables

Set via Dashboard (Settings -> Environment Variables) or CLI:

```bash
# Production only
vercel env add DATABASE_URL production
vercel env add BETTER_AUTH_SECRET production
vercel env add ANTHROPIC_API_KEY production
vercel env add POLAR_ACCESS_TOKEN production
vercel env add POLAR_WEBHOOK_SECRET production
vercel env add POLAR_PRO_PRODUCT_ID production
vercel env add GOOGLE_CLIENT_ID production
vercel env add GOOGLE_CLIENT_SECRET production

# All environments (production + preview + development)
vercel env add NEXT_PUBLIC_APP_URL  # Set different values per environment

# Preview-specific
# Use Neon integration for automatic DATABASE_URL per preview branch
```

**Environment-specific `NEXT_PUBLIC_APP_URL`:**
- Production: `https://cviet.vn`
- Preview: `https://<branch>-cviet.vercel.app` (auto-generated)
- Development: `http://localhost:3000`

## 2.4 Preview Deployments

Every push to a non-production branch creates a preview deployment automatically.

**Branch protection setup (GitHub):**
1. Go to repo Settings -> Branches -> Branch protection rules
2. Add rule for `main` (or `master`)
3. Enable "Require status checks to pass before merging"
4. Add `Vercel` as a required status check
5. Enable "Require branches to be up to date before merging"

**Selective preview builds (skip unnecessary deploys):**

In Vercel Dashboard -> Settings -> Git -> Ignored Build Step:

```bash
# Only build if src/ or package.json changed
git diff --quiet HEAD^ HEAD -- src/ package.json prisma/ || exit 1
```

## 2.5 Custom Domain Setup

1. Dashboard -> Project -> Settings -> Domains
2. Add `cviet.vn` and `www.cviet.vn`
3. Configure DNS:
   - `cviet.vn` -> `A` record -> `76.76.21.21`
   - `www.cviet.vn` -> `CNAME` -> `cname.vercel-dns.com`
4. SSL is automatic (Let's Encrypt)

## 2.6 Vercel + Neon Integration

The Vercel Neon integration automatically provisions a database branch for each preview deployment:

1. Go to Vercel Dashboard -> Integrations -> Browse Marketplace -> Neon
2. Install and connect your Neon project
3. The integration automatically:
   - Sets `DATABASE_URL` for production
   - Creates a Neon branch + sets `DATABASE_URL` for each preview deployment
   - Cleans up branches when preview deployments are deleted

**Alternative (Neon-managed integration):**
- Install from Neon Console -> Integrations -> Vercel
- Provides Git-branch-based cleanup instead of deployment-based
- Better for teams with existing Neon billing

---

> **Sources:**
> - [Vercel Deployments Overview](https://vercel.com/docs/deployments/overview)
> - [Neon + Vercel Integration](https://neon.com/docs/guides/vercel)
> - [Vercel Deployment Protection](https://vercel.com/docs/deployment-protection)
