# Auth Fix — Overview

## Purpose

Systematically fix auth issues identified by auth-scoring. Parse scorecard, prioritize by severity × weight, implement fixes, verify, re-score.

## Integration with auth-scoring

```
auth-scoring → scorecard + issues → auth-fix → improved code → auth-scoring (re-score)
```

## Priority Order

1. **CRITICAL** (score 0-3 or auth bypass) — Fix immediately, blocks deploy
2. **HIGH + high weight** (score 4-5, weight ≥ 12%) — Sessions, CSRF, Rate Limiting, Passwords
3. **HIGH + low weight** (score 4-5, weight < 12%) — Audit, Authorization
4. **MEDIUM** (score 6-7) — Next sprint
5. **LOW** (score 8) — Backlog

## Score Targets

| Context | Target | Grade |
|---------|--------|-------|
| Internal tool | 77+ | C+ |
| Public SaaS | 87+ | B+ |
| Enterprise | 90+ | A- |
| Compliance | 93+ | A |

## Safe vs Dangerous Changes

| Safe (low risk) | Dangerous (high risk) |
|---|---|
| Add security headers | Change session storage mechanism |
| Add rate limiting | Modify OAuth callback flow |
| Add audit logging | Change password hashing algorithm |
| Add CSRF validation | Modify session cookie config |
| Add 2FA plugin | Change auth proxy logic |

For dangerous changes: read existing code first, make minimal surgical edits, test immediately.

## Loop Mode

When "fix until 100" requested:
1. Parse new scorecard after each round
2. Fix remaining deductions
3. Verify (typecheck + tests + build)
4. Re-score with auth-scoring
5. Max 5 iterations
6. Stop if delta = 0 for 2 consecutive iterations
