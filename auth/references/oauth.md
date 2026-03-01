# Better Auth -- OAuth Setup (Google, GitHub)

> Section 4 from the comprehensive reference.

---

## 4. OAuth Setup (Google, GitHub)

### 4.1 Google OAuth

#### Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. APIs & Services --> Credentials --> Create Credentials --> OAuth client ID
3. Application type: Web application
4. Add Authorized redirect URIs:
   - Development: `http://localhost:3000/api/auth/callback/google`
   - Production: `https://yourdomain.com/api/auth/callback/google`

#### Server Configuration

```typescript
export const auth = betterAuth({
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      // Optional:
      // prompt: "select_account",           // force account selector
      // accessType: "offline",              // get refresh token
      // scopes: ["email", "profile"],       // default scopes
    },
  },
})
```

#### Client Sign-In

```typescript
// Standard OAuth redirect flow
await authClient.signIn.social({
  provider: "google",
  callbackURL: "/dashboard",
})

// With ID token (mobile/native apps)
await authClient.signIn.social({
  provider: "google",
  idToken: { token: googleIdToken, accessToken: googleAccessToken },
})
```

#### Request Additional Scopes (Post-Signup)

```typescript
await authClient.linkSocial({
  provider: "google",
  scopes: ["https://www.googleapis.com/auth/drive.file"],
})
```

Requires Better Auth >= 1.2.7.

### 4.2 GitHub OAuth

```typescript
export const auth = betterAuth({
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
})
```

Callback URL: `http://localhost:3000/api/auth/callback/github`

### 4.3 Account Linking

When a user signs up with email/password and later signs in with Google using the same email, Better Auth can link accounts automatically. This is the default behavior.

To disable: configure `accountLinking` options in the auth config.
