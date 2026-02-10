# Criteria: Authorization / RBAC (8%) + 2FA / MFA (5%)

## 9. Authorization & Route Protection (8%)

### Score 9-10: Enterprise-grade
- Two-layer auth: middleware (Edge) + API route (Node)
- Middleware: fast cookie check for page redirects + security headers
- API routes: full session verification with DB lookup (`requireAuth()`)
- Role-based access control (RBAC) with admin/user roles
- Object-level authorization (users can only access own resources)
- Route protection covers ALL sensitive paths
- Callback URL preserved on redirect to login

### Score 7-8: Production-ready
- Two-layer auth implemented
- Protected routes list in middleware
- `requireAuth()` helper in API routes
- User can only access own data (BOLA prevention)

### Score 5-6: Minimum
- Basic route protection exists
- Some API routes check authentication
- Redirect to login on unauthorized

### Score 3-4: Below minimum
- Only client-side auth checks
- Some API routes unprotected
- No BOLA prevention

### Score 0-2: Critical
- No route protection
- API routes accessible without authentication
- Privilege escalation possible

### Checklist
- [ ] Middleware protects page routes (cookie check)
- [ ] API routes use `requireAuth()` (DB session verification)
- [ ] Protected routes list is comprehensive
- [ ] Callback URL preserved on login redirect
- [ ] Object-level authorization (own resources only)
- [ ] Admin routes require admin role (if applicable)
- [ ] No client-only auth gates (always server-verified)

## 10. Two-Factor Authentication (5%)

### Score 9-10: Enterprise-grade
- TOTP-based 2FA (authenticator app)
- Backup/recovery codes generated on setup
- 2FA enforced for admin accounts
- Graceful setup flow (QR code + manual entry)
- 2FA status shown in user settings
- Re-authentication required to disable 2FA

### Score 7-8: Production-ready
- TOTP 2FA available via Better Auth plugin
- Backup codes provided
- Setup and disable flows implemented

### Score 5-6: Minimum
- 2FA plugin configured
- Basic TOTP flow works
- No backup codes

### Score 3-4: Below minimum
- 2FA code in config but not functional
- No user-facing setup flow
- No recovery mechanism

### Score 0-2: Not implemented
- No 2FA capability
- Note: For simple SaaS without sensitive data, score 5 is acceptable baseline

### Scoring Note

2FA weight is 5% — lowest category. For simple consumer SaaS:
- No 2FA = score 5 (neutral, acceptable for MVP)
- Having 2FA config but not enforced = score 6-7
- Full 2FA with recovery = score 9-10

### Checklist
- [ ] Better Auth `twoFactor` plugin enabled (if applicable)
- [ ] TOTP generation and verification
- [ ] Backup/recovery codes
- [ ] User-facing enable/disable flow
- [ ] Re-authentication before disabling
- [ ] 2FA enforcement for admin roles (if applicable)
