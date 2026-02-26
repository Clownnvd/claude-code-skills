# Migrate Mode -- Email System

Upgrade email code for provider or library changes.

## Process

1. **Detect versions** -- Check `package.json` for current versions of `resend`, `@react-email/*`, `@upstash/qstash`
2. **Map breaking changes** -- Compare current vs target version changelogs
3. **Apply migrations** -- Update code for each breaking change
4. **Verify** -- TypeScript compiles, tests pass, emails send correctly
5. **Output** -- Fill `assets/templates/migration-report.md.template`

## Common Migrations

| From | To | Key Changes |
|------|----|-------------|
| Nodemailer | Resend SDK | Replace SMTP transport with API client |
| EJS/Handlebars templates | React Email | Convert to TSX components with `render()` |
| No queue | QStash | Add queue client, worker endpoint, retry logic |
| `resend` v1 | `resend` v2+ | Check API surface changes, batch method |
| Manual webhooks | Svix verification | Add `svix` library, verify signatures |

## Verification Checklist

- [ ] `npx tsc --noEmit` exits 0
- [ ] `pnpm test` passes
- [ ] `pnpm build` succeeds
- [ ] Test email sends successfully
- [ ] Re-score shows no regressions
