# Deployment Target Comparison

> Part of: CI/CD & Deployment Reference -- Next.js 16 + Prisma + Neon (CViet)
> Stack: Next.js 16.1.6 (App Router, Webpack mode) | Prisma 6 + Neon PostgreSQL | pnpm | TypeScript

---

| Feature | Vercel | Docker (Self-Host) | Node.js Server | Cloudflare Workers |
|---------|--------|-------------------|----------------|-------------------|
| **Setup complexity** | Minimal (zero-config) | Medium | Medium | High (adapter needed) |
| **All Next.js features** | Yes | Yes | Yes | Limited (no Node.js APIs) |
| **Serverless functions** | Built-in | Manual | Manual | Built-in (Workers) |
| **Preview deployments** | Automatic per PR | Manual via CI | Manual | Via Pages |
| **Custom domains** | Dashboard/CLI | DNS + reverse proxy | DNS + reverse proxy | Dashboard |
| **SSL/TLS** | Automatic | Certbot/Caddy | Certbot/Caddy | Automatic |
| **Scaling** | Automatic | Kubernetes/Compose | PM2/systemd | Automatic |
| **Cost (hobby)** | Free tier generous | VPS ~$5-20/mo | VPS ~$5-20/mo | Free tier generous |
| **Cost (production)** | $20/mo Pro | VPS ~$20-100/mo | VPS ~$20-100/mo | $5/mo Workers Paid |
| **Database branching** | Neon integration | Manual | Manual | Manual |
| **Cold starts** | Yes (serverless) | No | No | Yes (Workers) |
| **`@react-pdf/renderer`** | Works (Node.js runtime) | Works | Works | Does NOT work (no Node.js) |
| **Prisma** | Works | Works | Works | Requires edge adapter |
| **Better Auth** | Works | Works | Works | Limited |
| **Rollback** | Instant (1 click) | Container tag revert | Git revert + rebuild | Dashboard rollback |
| **Build cache** | Automatic | Volume mount needed | Filesystem persistent | Limited |

## Recommendation for CViet

**Primary: Vercel** -- Zero-config, automatic preview deployments, Neon integration, instant rollback. The free tier handles early-stage SaaS well. `@react-pdf/renderer` and Prisma both work because Vercel runs Next.js on Node.js runtime by default.

**Fallback: Docker on Railway/Fly.io** -- If Vercel costs become prohibitive at scale or you need more control over the runtime environment.

**Not recommended: Cloudflare Workers** -- `@react-pdf/renderer` requires Node.js APIs (`fs`, `stream`, `Buffer`) that Workers does not provide. Better Auth also has limited Workers support.

---

> **Sources:**
> - [Next.js Deploying Docs](https://nextjs.org/docs/app/getting-started/deploying)
> - [Vercel Deployments Overview](https://vercel.com/docs/deployments/overview)
> - [Complete Guide to Deploying Next.js Apps in 2026 (DEV Community)](https://dev.to/zahg_81752b307f5df5d56035/the-complete-guide-to-deploying-nextjs-apps-in-2026-vercel-self-hosted-and-everything-in-between-48ia)
