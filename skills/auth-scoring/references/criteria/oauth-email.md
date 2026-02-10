# Criteria: OAuth & Social Login (10%) + Email Verification (8%)

## 3. OAuth & Social Login (10%)

### Score 9-10: Enterprise-grade
- Multiple providers (Google, GitHub, etc.) with graceful disable
- Account linking enabled with trusted provider list
- State parameter validated (CSRF protection for OAuth)
- PKCE flow for public clients
- Provider-specific scopes minimized (only what's needed)
- OAuth callback URL restricted to known domains
- Error handling: provider failures don't leak info

### Score 7-8: Production-ready
- At least 2 OAuth providers configured
- Account linking with `trustedProviders`
- Env-based enable/disable (`Boolean(process.env.CLIENT_ID)`)
- Proper callback URLs in provider config

### Score 5-6: Minimum
- At least 1 OAuth provider
- Basic error handling on callback
- Provider credentials in env vars

### Score 3-4: Below minimum
- OAuth without state parameter
- Hardcoded client credentials
- No account linking strategy

### Score 0-2: Critical
- OAuth credentials in source code
- No CSRF protection on OAuth flow
- Open redirect in callback URL

### Checklist
- [ ] OAuth providers gated by env vars (not hardcoded)
- [ ] Account linking configured with trusted providers
- [ ] State parameter / CSRF validated on callback
- [ ] Callback URLs restricted (not wildcard)
- [ ] Provider failures handled gracefully (no info leak)
- [ ] Minimal scopes requested

## 4. Email Verification (8%)

### Score 9-10: Enterprise-grade
- Verification required before access to protected features
- Time-limited verification tokens (< 24h)
- Auto-enabled when email service configured (`Boolean(process.env.RESEND_API_KEY)`)
- Resend verification with rate limiting
- Custom branded email templates
- Verification on both sign-up and sign-in (new device)

### Score 7-8: Production-ready
- Verification sent on sign-up
- Time-limited tokens
- Branded email templates
- Auto-sign-in after verification

### Score 5-6: Minimum
- Basic verification email sent
- Token exists with some expiry
- Generic email template

### Score 3-4: Below minimum
- Verification optional with no enforcement
- Long-lived tokens (> 7 days)
- No resend mechanism

### Score 0-2: Critical
- No email verification
- Verification tokens guessable
- Email verification bypassable

### Checklist
- [ ] Email verification enabled when email service available
- [ ] Sent on sign-up (and optionally sign-in)
- [ ] Time-limited tokens (< 24 hours)
- [ ] Auto-sign-in after verification
- [ ] Branded email templates (not plain text)
- [ ] Rate limiting on resend endpoint
- [ ] Secure token generation (crypto random)
