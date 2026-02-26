# Fix Patterns: OAuth & Social Login + Email Verification

## OAuth Fixes

### Fix: Env-Gated Provider Config
```typescript
// In auth.ts socialProviders
socialProviders: {
  google: {
    enabled: Boolean(
      process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET
    ),
    clientId: process.env.GOOGLE_CLIENT_ID ?? "",
    clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? "",
  },
  github: {
    enabled: Boolean(
      process.env.GITHUB_CLIENT_ID && process.env.GITHUB_CLIENT_SECRET
    ),
    clientId: process.env.GITHUB_CLIENT_ID ?? "",
    clientSecret: process.env.GITHUB_CLIENT_SECRET ?? "",
  },
},
```
**Key**: Use `enabled: Boolean(...)` to cleanly disable unconfigured providers.

### Fix: Account Linking
```typescript
account: {
  accountLinking: {
    enabled: true,
    trustedProviders: ["google", "github"],
    // NEVER use ["*"] — explicitly list trusted providers
  },
},
```

### Fix: OAuth Error Handling
```typescript
// Verify Better Auth handles OAuth errors gracefully
// Check: /api/auth/callback/google?error=access_denied
// Should redirect to /sign-in?error=OAuthCallbackError
// NOT show a 500 page or leak provider error details
```

### Fix: OAuth Callback URL Validation
```typescript
// Better Auth validates callback URLs internally
// Verify BETTER_AUTH_URL matches your domain exactly
// In production: BETTER_AUTH_URL=https://yourdomain.com
// NO trailing slash, NO path prefix
```

## Email Verification Fixes

### Fix: Auto-Enable Based on Email Provider
```typescript
emailVerification: {
  sendOnSignUp: true,
  autoSignInAfterVerification: true,
  sendVerificationEmail: async ({ user, url }) => {
    // Only send if email provider is configured
    if (!process.env.RESEND_API_KEY) {
      return; // Skip silently in dev
    }
    await sendEmail({
      to: user.email,
      subject: "Verify your email",
      html: `<a href="${url}">Verify email</a>`,
    });
  },
},
```

### Fix: Require Verification Gate
```typescript
// In Better Auth config
emailAndPassword: {
  requireEmailVerification: Boolean(process.env.RESEND_API_KEY),
},
```
This auto-disables verification requirement when no email provider is set.

### Fix: Verification Token Expiry
Better Auth handles token expiry internally. Verify:
- Token expires after reasonable time (default: 1 hour)
- Expired tokens show clear error message
- Users can request new verification email

### Fix: Rate Limit Verification Emails
```typescript
// In the sendVerificationEmail function:
// Better Auth handles rate limiting of verification sends
// Verify: user cannot spam "resend verification" endpoint
// Check /api/auth/send-verification-email has rate limiting
```

### Fix: Email Change Verification
```typescript
// When user changes email:
// 1. New email must be verified before becoming active
// 2. Notification sent to OLD email about the change
// Better Auth handles this via emailVerification config
```
