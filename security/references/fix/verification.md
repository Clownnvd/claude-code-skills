# Security Fix — Verification

## Post-Fix Checklist

After each fix batch:

### 1. Type Safety
```bash
pnpm typecheck  # 0 errors
```

### 2. Tests Pass
```bash
pnpm test  # all pass, no regressions
```

### 3. No New Issues
- Fix didn't introduce new vulnerability
- Error responses still functional
- Auth flow still works
- Webhook processing still works

### 4. Security-Specific Checks
- [ ] No hardcoded secrets in diff
- [ ] No `console.log` added to API routes
- [ ] CSP changes tested in browser
- [ ] Redirect validation tested with `//evil.com`
- [ ] Error responses don't leak info

## Re-Scoring Protocol

1. Run `security-scoring` with full audit
2. Compare new scorecard vs previous
3. Verify fixed issues no longer appear
4. Check for new issues introduced by fixes

## Loop Mode Protocol

Max 5 iterations. Target: A- (90+) for enterprise, B+ (87+) for production

```
Round 1: Fix all CRITICAL + HIGH issues
  → typecheck + test
  → re-score
  → expect jump of 15-25 points

Round 2: Fix remaining MEDIUM issues
  → typecheck + test
  → re-score
  → expect jump of 5-10 points

Round 3: Fix LOW issues + polish
  → typecheck + test
  → re-score
  → expect jump of 2-5 points
```

## Common Verification Failures

| Failure | Cause | Fix |
|---------|-------|-----|
| Type error after Zod addition | Schema type not exported | Export schema type: `type X = z.infer<typeof xSchema>` |
| Test fail after error response change | Test expects old format | Update test expectations |
| CSP blocks page rendering | Too restrictive directive | Add specific domain to CSP allowlist |
| Webhook test fails | Signature verification added | Update test mock to include valid signature |
| Auth flow broken | Redirect validation too strict | Allow auth callback URLs in validation |
