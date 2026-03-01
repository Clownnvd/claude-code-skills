# Better Auth -- Cookie Configuration & Rate Limiting

> Sections 7-8 from the comprehensive reference.

---

## 7. Cookie Configuration

### 7.1 Default Cookie Names

| Cookie Name | Purpose |
|-------------|---------|
| `better-auth.session_token` | Session token |
| `better-auth.session_data` | Session data (when cookie cache enabled) |
| `better-auth.dont_remember` | Flag when rememberMe is disabled |

### 7.2 Cookie Prefix

```typescript
export const auth = betterAuth({
  advanced: {
    cookiePrefix: "cviet",  // cookies become "cviet.session_token" etc.
  },
})
```

### 7.3 Secure Cookies

```typescript
export const auth = betterAuth({
  advanced: {
    useSecureCookies: true,  // force HTTPS-only cookies
    cookies: {
      session_token: {
        name: "custom_session_token",  // custom cookie name
        attributes: {
          httpOnly: true,
          secure: true,
          sameSite: "lax",
        },
      },
    },
  },
})
```

### 7.4 Cross-Subdomain Cookies

```typescript
export const auth = betterAuth({
  advanced: {
    crossSubDomainCookies: {
      enabled: true,
      domain: "example.com",
    },
  },
  trustedOrigins: [
    "https://app.example.com",
    "https://admin.example.com",
  ],
})
```

### 7.5 nextCookies Plugin

Required when calling Better Auth methods that set cookies from server actions:

```typescript
import { nextCookies } from "better-auth/next-js"

export const auth = betterAuth({
  plugins: [nextCookies()],  // MUST be the LAST plugin in the array
})
```

Without this plugin, cookies set by `signInEmail`, `signUpEmail`, etc. in server actions will NOT reach the browser.

---

## 8. Rate Limiting

### 8.1 Default Configuration

- **Production**: Enabled by default (100 requests / 60 seconds per IP)
- **Development**: Disabled by default
- **Server-side `auth.api.*` calls**: NOT rate limited

### 8.2 Custom Configuration

```typescript
export const auth = betterAuth({
  rateLimit: {
    enabled: true,               // enable in dev too
    window: 60,                  // seconds
    max: 100,                    // max requests per window
    storage: "memory",           // "memory" | "database" | "secondary-storage"
    customRules: {
      "/sign-in/email": {
        window: 10,
        max: 3,                  // 3 login attempts per 10 seconds
      },
      "/sign-up/email": {
        window: 60,
        max: 5,
      },
      "/get-session": false,     // disable rate limiting for this route
    },
  },
})
```

### 8.3 Rate Limit Storage Options

```typescript
// Database storage (for serverless)
rateLimit: {
  storage: "database",
  modelName: "rateLimit",    // requires schema migration
}

// Redis / Secondary storage
rateLimit: {
  storage: "secondary-storage",
}

// Custom storage
rateLimit: {
  customStorage: {
    get: async (key) => await redis.get(key),
    set: async (key, value) => await redis.setex(key, 60, JSON.stringify(value)),
  },
}
```

### 8.4 Handling Rate Limit Errors (Client)

```typescript
// Global handler
const authClient = createAuthClient({
  fetchOptions: {
    onError: async (context) => {
      if (context.response.status === 429) {
        const retryAfter = context.response.headers.get("X-Retry-After")
        alert(`Too many requests. Try again in ${retryAfter} seconds.`)
      }
    },
  },
})

// Per-request handler
await authClient.signIn.email({
  email, password,
  fetchOptions: {
    onError: async (ctx) => {
      if (ctx.response.status === 429) {
        const retry = ctx.response.headers.get("X-Retry-After")
        setError(`Qua nhieu yeu cau. Thu lai sau ${retry} giay.`)
      }
    },
  },
})
```

### 8.5 IPv6 Subnet Rate Limiting

Prevents attackers from rotating IPv6 addresses:

```typescript
rateLimit: {
  ipv6Subnet: 64,  // rate limit by /64 subnet
}
```
