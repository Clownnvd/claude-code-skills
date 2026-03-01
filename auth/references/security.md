# Better Auth -- Security Best Practices

> Section 9 from the comprehensive reference.

---

## 9. Security Best Practices

### 9.1 CSRF Protection

Better Auth implements multi-layer CSRF protection:

1. **Request type restrictions**: Only accepts `application/json` content-type
2. **Origin validation**: Verifies `Origin` header against `trustedOrigins`
3. **Cookie SameSite**: Defaults to `Lax`
4. **Fetch Metadata**: Validates `Sec-Fetch-Site`, `Sec-Fetch-Mode`, `Sec-Fetch-Dest`

**Configuration:**
```typescript
export const auth = betterAuth({
  trustedOrigins: [
    "https://example.com",
    "https://*.example.com",  // wildcard subdomain
  ],
  // DANGER: Only disable for testing
  // advanced: { disableCSRFCheck: true }
})
```

### 9.2 Password Hashing

Default: `scrypt` (memory-hard, CPU-intensive). Customize with argon2 or bcrypt if needed.

### 9.3 Session Security Checklist

- [ ] Set appropriate `expiresIn` (default 7 days)
- [ ] Enable `cookieCache` for performance without sacrificing too much security
- [ ] Use `revokeOtherSessions: true` on password change
- [ ] Validate session in page/route handler, not just proxy
- [ ] Set `freshAge` for sensitive operations (e.g., billing changes)

### 9.4 OAuth Security

- PKCE (Proof Key for Code Exchange) is used automatically for OAuth flows
- OAuth state values are stored in the database and removed after use
- Always set `BETTER_AUTH_URL` to prevent redirect_uri_mismatch

### 9.5 IP Address Configuration (Behind Proxy/CDN)

```typescript
export const auth = betterAuth({
  advanced: {
    ipAddress: {
      ipAddressHeaders: ["cf-connecting-ip"],  // Cloudflare
      // ipAddressHeaders: ["x-real-ip"],      // Nginx
    },
  },
})
```

### 9.6 Proxy Header Trust

```typescript
export const auth = betterAuth({
  advanced: {
    trustedProxyHeaders: true,  // trust X-Forwarded-Host, X-Forwarded-Proto
  },
})
```

### 9.7 TypeScript Strict Mode

Better Auth requires `strict: true` or at minimum `strictNullChecks: true` in `tsconfig.json`. Without it, type inference may fail silently.
