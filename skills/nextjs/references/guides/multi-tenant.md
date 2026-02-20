# Multi-Tenant Architecture

> Source: https://nextjs.org/docs/app/guides/multi-tenant (v16.1.6)

## Overview

Next.js supports building multi-tenant applications where a single app serves multiple tenants (customers/organizations) with tenant-specific content, data, and configuration.

## Recommended Architecture

Vercel provides a reference implementation: [Platforms Starter Kit](https://vercel.com/templates/next.js/platforms-starter-kit)

## Common Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Subdomain-based | `tenant.example.com` | SaaS platforms, white-label apps |
| Path-based | `example.com/tenant` | Simpler setups, shared domain |
| Custom domain | `tenant-custom.com` | Full white-labeling |

## Implementation Approaches

### Subdomain-based Routing with Middleware

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') || ''
  const subdomain = hostname.split('.')[0]

  // Rewrite to tenant-specific path
  return NextResponse.rewrite(
    new URL(`/${subdomain}${request.nextUrl.pathname}`, request.url)
  )
}
```

### Dynamic Route Structure

```
app/
  [tenant]/
    page.tsx        # Tenant home
    layout.tsx      # Tenant layout with branding
    dashboard/
      page.tsx      # Tenant dashboard
```

### Tenant Data Resolution

```typescript
// app/[tenant]/layout.tsx
export default async function TenantLayout({
  params,
  children,
}: {
  params: Promise<{ tenant: string }>
  children: React.ReactNode
}) {
  const { tenant } = await params
  const tenantConfig = await getTenantConfig(tenant)

  if (!tenantConfig) {
    return notFound()
  }

  return (
    <div style={{ '--brand-color': tenantConfig.color } as React.CSSProperties}>
      {children}
    </div>
  )
}
```

## Quick Reference

| Need | Solution |
|------|----------|
| Reference implementation | [Platforms Starter Kit](https://vercel.com/templates/next.js/platforms-starter-kit) |
| Subdomain routing | Middleware + URL rewrite |
| Path-based routing | Dynamic `[tenant]` route segments |
| Custom domains | Middleware hostname detection + rewrite |
| Tenant config | Resolve in layout via `params` |
