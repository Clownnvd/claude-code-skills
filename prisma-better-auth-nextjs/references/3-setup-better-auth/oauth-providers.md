# Step 3.4: OAuth Providers (Google, GitHub)

> Source: King Template codebase — production OAuth configuration

## Install

No extra packages — Better Auth includes OAuth support.

## Environment Variables

```env
# Google OAuth — https://console.cloud.google.com/apis/credentials
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# GitHub OAuth — https://github.com/settings/developers
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

## Update `src/lib/auth.ts`

Add `socialProviders` and `account` to the `betterAuth` config:

```typescript
export const auth = betterAuth({
  // ... database, emailAndPassword ...

  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID ?? "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? "",
      enabled: Boolean(
        process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET
      ),
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID ?? "",
      clientSecret: process.env.GITHUB_CLIENT_SECRET ?? "",
      enabled: Boolean(
        process.env.GITHUB_CLIENT_ID && process.env.GITHUB_CLIENT_SECRET
      ),
    },
  },

  account: {
    accountLinking: {
      enabled: true,
      trustedProviders: ["google", "github"],
    },
  },
});
```

## Client-Side Usage

```typescript
import { signIn } from "@/lib/auth-client";

// Google sign-in
await signIn.social({ provider: "google", callbackURL: "/dashboard" });

// GitHub sign-in
await signIn.social({ provider: "github", callbackURL: "/dashboard" });
```

## Key Patterns

| Pattern | Details |
|---------|---------|
| Conditional enable | `enabled: Boolean(ID && SECRET)` — graceful when not configured |
| Account linking | Users can link multiple providers to one account |
| Trusted providers | Only listed providers can auto-link (prevents account takeover) |
| Callback URL | Where to redirect after OAuth flow completes |
| Fallback values | `?? ""` prevents undefined errors when env vars missing |

## OAuth Callback URLs

Configure these in each provider's dashboard:

| Provider | Callback URL |
|----------|-------------|
| Google | `http://localhost:3000/api/auth/callback/google` |
| GitHub | `http://localhost:3000/api/auth/callback/github` |

In production, replace `localhost:3000` with your domain.
