# Deploying

> Source: nextjs.org/docs/app/getting-started/deploying (v16.1.6)

## Deployment Options

| Option | Feature Support | Use Case |
|--------|----------------|----------|
| Node.js server | All | Any Node.js hosting provider |
| Docker container | All | Container orchestrators (Kubernetes, cloud providers) |
| Static export | Limited (no server features) | Static hosting (S3, Nginx, Apache, GitHub Pages) |
| Adapters | Platform-specific | Vercel, Cloudflare, AWS Amplify, Netlify, etc. |

## Node.js Server

Supports **all** Next.js features.

```json
// package.json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

```bash
npm run build   # Build for production
npm run start   # Start Node.js server
```

Can eject to a custom server if needed. See self-hosting guide for infrastructure config.

### Node.js Templates

- Flightcontrol, Railway, Replit

## Docker

Supports **all** Next.js features. Use container orchestrators (Kubernetes) or any Docker-capable cloud provider.

Use local dev (`npm run dev`) instead of Docker during development on Mac/Windows for better performance.

### Docker Templates

- Docker, Docker Multi-Environment
- DigitalOcean, Fly.io, Google Cloud Run, Render, SST

## Static Export

Start as static site or SPA, optionally upgrade to server features later.

- Can be hosted on any web server serving HTML/CSS/JS
- **Does not** support features requiring a server (Route Handlers, proxy, ISR, etc.)
- See static exports guide for unsupported features list

### Static Template

- GitHub Pages

## Adapters

Platform-specific adapters for different infrastructure:

| Provider | Docs |
|----------|------|
| Vercel | vercel.com/docs/frameworks/nextjs |
| Cloudflare | developers.cloudflare.com/workers/frameworks |
| AWS Amplify | docs.amplify.aws/nextjs |
| Netlify | docs.netlify.com/frameworks/next-js |
| Firebase | firebase.google.com/docs/app-hosting |
| Deno Deploy | docs.deno.com/examples/next_tutorial |
| Appwrite Sites | appwrite.io/docs/products/sites |

A Deployment Adapters API is in development for all platforms.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `next build` | Create production build |
| `next start` | Start Node.js production server |
| `output: 'export'` in next.config | Enable static export |

| Deployment | All Features? | Server Required? |
|------------|--------------|-----------------|
| Node.js | Yes | Yes |
| Docker | Yes | Yes |
| Static export | No | No |
| Adapters | Varies | Varies |
