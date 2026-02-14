# Email Fix -- Best Practices

## Fix Discipline

| Do | Don't |
|----|-------|
| Fix one issue at a time, verify, then move on | Apply all fixes at once without verification |
| Check TypeScript compilation after each fix | Skip type checking until the end |
| Test email sending after provider changes | Assume send works because code compiles |
| Verify webhook signatures in tests | Skip webhook verification testing |
| Keep existing email triggers working | Refactor triggers while fixing templates |
| Add env vars to `.env.example` | Add env vars only to `.env.local` |

## Safe Changes (Low Risk)

These fixes rarely break existing functionality:

| Fix | Risk Level | Verify With |
|-----|-----------|-------------|
| Add env var validation to Resend init | Low | `tsc --noEmit` |
| Add plain text fallback to templates | Low | Render test |
| Add `PreviewProps` to templates | Low | `email dev` preview |
| Add rate limit middleware to endpoint | Low | Manual endpoint test |
| Document DNS records in README | None | N/A |
| Add `.env.example` entries | None | N/A |

## Dangerous Changes (High Risk)

These fixes can break email delivery if done incorrectly:

| Fix | Risk | Mitigation |
|-----|------|------------|
| Move from sync to queue-based sending | May lose emails if queue not configured | Test queue roundtrip before switching |
| Refactor email service layer | May break import paths for triggers | Search all callers before refactoring |
| Change from address or domain | Emails may go to spam | Verify new domain first |
| Add suppression list check | May block legitimate sends | Test with known-good addresses |
| Upgrade Resend SDK version | API changes may break send calls | Check changelog, test send |

## Template Safety

| Do | Don't |
|----|-------|
| Create new components alongside old ones | Delete old templates before new ones work |
| Test render output for each template | Assume template renders correctly from code review |
| Keep `PreviewProps` up to date with real data shapes | Use `any` or empty objects for preview |
| Use `render()` + `plainText: true` for text version | Generate plain text manually |

## Queue Safety

| Do | Don't |
|----|-------|
| Verify QStash signature in every worker | Skip verification in development |
| Set reasonable retry count (3-5) | Set unlimited retries |
| Configure dead letter queue | Silently drop failed messages |
| Log all queue events (enqueue, process, fail) | Log only errors |
| Test worker endpoint with mock payload | Test only by sending real emails |

## Provider Safety

| Do | Don't |
|----|-------|
| Validate API key exists at module load | Validate only when first email is sent |
| Check `{ data, error }` from every send call | Use `.then()` without error handling |
| Use env var for from address | Hardcode domain in from field |
| Test with Resend test mode first | Test directly against production |

## Common Mistakes

1. **Breaking import paths during refactor**: Always search for all imports of a moved file.
2. **Forgetting to update callers after renaming**: Use TypeScript compiler to find all references.
3. **Adding queue but not the worker**: Email gets enqueued but never processed.
4. **Webhook route without signature verification**: Security vulnerability.
5. **Rate limiting only by IP**: Users behind NAT or VPN share IPs. Add per-user limits.
6. **Suppression check after send**: Check BEFORE calling send, not after.

## Fix Order for Maximum Safety

1. Environment and configuration fixes (env vars, SDK init)
2. Provider integration fixes (error handling, domain verification)
3. Template fixes (component system, rendering)
4. Queue and delivery fixes (async sending, retry logic)
5. Security and compliance fixes (auth, bounce, rate limiting)
6. Analytics and testing fixes (tracking, preview, tests)

This order ensures each layer is stable before building the next.
