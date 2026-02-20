# Step 3.5: Two-Factor Authentication (2FA)

> Source: King Template codebase — TOTP-based 2FA with Better Auth

## Install

No extra packages — `twoFactor` is a built-in Better Auth plugin.

## Server Config

Add the `twoFactor` plugin to `src/lib/auth.ts`:

```typescript
import { twoFactor } from "better-auth/plugins";

export const auth = betterAuth({
  // ... database, emailAndPassword, socialProviders ...

  plugins: [
    twoFactor({
      issuer: "Your App Name", // Shows in authenticator apps
    }),
  ],
});
```

## Client Config

Add the client plugin to `src/lib/auth-client.ts`:

```typescript
import { createAuthClient } from "better-auth/react";
import { twoFactorClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [twoFactorClient()],
});

export const {
  signIn,
  signUp,
  signOut,
  useSession,
  twoFactor,
} = authClient;
```

## Client-Side Usage

```typescript
import { twoFactor } from "@/lib/auth-client";

// Enable 2FA — returns QR code URI for authenticator app
const { data } = await twoFactor.enable({ password: "user-password" });
// data.totpURI → render as QR code

// Verify 2FA code during setup
await twoFactor.verifyTotp({ code: "123456" });

// Disable 2FA
await twoFactor.disable({ password: "user-password" });
```

## Schema Requirement

The `twoFactor` plugin adds fields to the `User` model automatically. Run migration after enabling:

```bash
npx @better-auth/cli generate
npx prisma migrate dev --name add-2fa-fields
npx prisma generate
```

## Quick Reference

| Feature | Details |
|---------|---------|
| Method | TOTP (Time-based One-Time Password) |
| Server plugin | `twoFactor({ issuer: "App Name" })` |
| Client plugin | `twoFactorClient()` |
| Enable | `twoFactor.enable({ password })` → returns `totpURI` |
| Verify | `twoFactor.verifyTotp({ code })` |
| Disable | `twoFactor.disable({ password })` |
| Authenticator apps | Google Authenticator, Authy, 1Password, etc. |
