# Auth Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| Session Management (15%) | Integration | Cookie flags, expiry, rotation on privilege change |
| Password Security (12%) | Unit | Hash verification, strength validation, breach check |
| OAuth & Social Login (10%) | Integration | State param present, token exchange, account linking |
| Email Verification (8%) | Integration | Token generation, expiry, one-time use |
| CSRF & Origin (12%) | Integration | Token validation, origin check, SameSite cookie |
| Security Headers (10%) | Integration | All headers present in response |
| Rate Limiting (12%) | Integration | Lockout after N failures, exponential backoff |
| Audit Logging (8%) | Unit | Events logged with correct context |
| Authorization (8%) | Integration | Role-based access, route protection |
| 2FA/MFA (5%) | Integration | TOTP validation, backup codes, recovery |

2. **Generate Test Files** — Test files for:
   - `__tests__/auth/session.test.ts` — Session lifecycle
   - `__tests__/auth/login.test.ts` — Login flow + rate limiting
   - `__tests__/auth/middleware.test.ts` — CSRF, headers, route protection
   - `__tests__/auth/oauth.test.ts` — OAuth flows

3. **Output** — Test files + coverage matrix
