# Self-Hosted Node.js Server

> Part of: CI/CD & Deployment Reference -- Next.js 16 + Prisma + Neon (CViet)
> Stack: Next.js 16.1.6 (App Router, Webpack mode) | Prisma 6 + Neon PostgreSQL | pnpm | TypeScript

---

## 4.1 Direct Node.js Deployment (PM2)

```bash
# On server
git pull origin main
pnpm install --frozen-lockfile
node scripts/postinstall.js
pnpm db:generate
pnpm build

# Start with PM2
pm2 start npm --name "cviet" -- start
pm2 save
pm2 startup
```

## 4.2 PM2 Ecosystem File

```js
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'cviet',
    script: 'node_modules/.bin/next',
    args: 'start',
    instances: 'max',
    exec_mode: 'cluster',
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000,
    },
    max_memory_restart: '512M',
    error_file: '/var/log/cviet/error.log',
    out_file: '/var/log/cviet/output.log',
  }],
};
```

## 4.3 Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/cviet
server {
    listen 80;
    server_name cviet.vn www.cviet.vn;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cviet.vn www.cviet.vn;

    ssl_certificate /etc/letsencrypt/live/cviet.vn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/cviet.vn/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Static assets (long cache)
    location /_next/static {
        proxy_pass http://127.0.0.1:3000;
        expires 365d;
        add_header Cache-Control "public, immutable";
    }
}
```

## 4.4 Kamal Deployment (Modern Alternative)

Kamal (from 37signals) provides Docker-based deployments via SSH without Kubernetes:

```yaml
# config/deploy.yml
service: cviet
image: your-registry/cviet

servers:
  web:
    - 192.168.1.100

registry:
  server: ghcr.io
  username: your-github-user
  password:
    - KAMAL_REGISTRY_PASSWORD

env:
  clear:
    NEXT_PUBLIC_APP_URL: https://cviet.vn
  secret:
    - DATABASE_URL
    - BETTER_AUTH_SECRET
    - ANTHROPIC_API_KEY

proxy:
  ssl: true
  host: cviet.vn

builder:
  remote: false
  arch: amd64
```

---

> **Sources:**
> - [Next.js Deploying Docs](https://nextjs.org/docs/app/getting-started/deploying)
> - [Complete Guide to Deploying Next.js Apps in 2026 (DEV Community)](https://dev.to/zahg_81752b307f5df5d56035/the-complete-guide-to-deploying-nextjs-apps-in-2026-vercel-self-hosted-and-everything-in-between-48ia)
