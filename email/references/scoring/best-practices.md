# Email Scoring -- Best Practices

## Transactional Email (15%)

| Do | Don't |
|----|-------|
| Trigger emails from business events (user signup, order placed) | Fire emails from UI components directly |
| Use a service layer (`sendWelcomeEmail(user)`) | Call `resend.emails.send()` scattered across routes |
| Confirm delivery via webhook events | Assume send() success means delivered |
| Include unsubscribe link in marketing emails | Send marketing without unsubscribe |

## Email Templates & Rendering (12%)

| Do | Don't |
|----|-------|
| Use React Email components (`Html`, `Body`, `Container`) | Use raw HTML string concatenation |
| Render with `render()` from `@react-email/render` | Pass JSX directly to Resend |
| Provide plain text fallback via `plainText: true` | Send HTML only |
| Use `Tailwind` wrapper for responsive styles | Use external CSS files (not supported in email) |

## Notification Queue & Delivery (12%)

| Do | Don't |
|----|-------|
| Route email through QStash or similar queue | Call `resend.emails.send()` synchronously in request |
| Configure retries with exponential backoff | Use infinite retry or no retry |
| Set up dead letter queue for failed messages | Silently drop failed emails |
| Verify QStash signatures on worker endpoints | Accept unverified queue messages |

## Email Provider Integration (12%)

| Do | Don't |
|----|-------|
| Validate `RESEND_API_KEY` at startup | Use optional chaining on API key |
| Check domain verification status | Send from unverified domains |
| Handle Resend API errors with typed responses | Swallow errors with empty catch blocks |
| Use environment variables for from address | Hardcode `from: "noreply@example.com"` |

## Deliverability & Reputation (10%)

| Do | Don't |
|----|-------|
| Verify sending domain with DNS records | Send from `onboarding@resend.dev` in production |
| Maintain suppression list from bounces | Keep sending to bounced addresses |
| Use consistent from address and domain | Change from address frequently |
| Keep bounce rate under 2% | Ignore bounce metrics |

## Bounce & Complaint Handling (10%)

| Do | Don't |
|----|-------|
| Set up webhook endpoint for Resend events | Poll API for delivery status |
| Verify webhook signatures with Svix | Accept unverified webhook payloads |
| Add bounced addresses to suppression list | Continue sending to hard bounces |
| Process complaints and auto-unsubscribe | Ignore complaint events |

## Email Auth -- SPF/DKIM/DMARC (8%)

| Do | Don't |
|----|-------|
| Configure SPF record for sending domain | Skip DNS configuration |
| Set up DKIM with Resend-provided CNAME records | Use default shared DKIM |
| Publish DMARC policy (`p=quarantine` minimum) | Set DMARC to `p=none` permanently |
| Monitor DMARC aggregate reports | Set and forget DNS records |

## Rate Limiting & Throttling (8%)

| Do | Don't |
|----|-------|
| Rate limit email-triggering endpoints | Allow unlimited password reset requests |
| Use Upstash Ratelimit or similar | Build custom rate limiter from scratch |
| Throttle queue processing to stay within provider limits | Burst-send entire queue at once |
| Set per-user and per-IP limits | Use only global rate limits |

## Analytics & Tracking (7%)

| Do | Don't |
|----|-------|
| Track opens and clicks via webhook events | Ignore delivery metrics entirely |
| Log delivery status per email | Only track send attempts |
| Set up alerts for delivery rate drops | Wait for user reports of missing emails |
| Dashboard for email health metrics | Rely solely on provider dashboard |

## Testing & Preview (6%)

| Do | Don't |
|----|-------|
| Run React Email preview server (`email dev`) | Test only by sending real emails |
| Write render tests for template output | Skip template testing |
| Test webhook handler with mock payloads | Test webhooks only in production |
| Test queue worker with mock messages | Skip queue integration tests |

## Pre-Deploy Checklist

- [ ] Domain verified in Resend dashboard
- [ ] SPF, DKIM, DMARC records published
- [ ] `RESEND_API_KEY` in production environment
- [ ] `QSTASH_TOKEN` and signing keys in production
- [ ] Webhook endpoint accessible and signature-verified
- [ ] Suppression list check before every send
- [ ] Rate limiting on all email-triggering endpoints
- [ ] Error handling and retry logic tested
- [ ] Plain text fallback for all templates
- [ ] Unsubscribe link in marketing emails

## Common Pitfalls

1. **Synchronous sending** -- Blocks request until Resend responds. Use queue.
2. **No error handling** -- `resend.emails.send()` returns `{ data, error }`. Check both.
3. **Hardcoded from address** -- Breaks when domain changes. Use env var.
4. **Missing webhook verification** -- Security risk. Always verify Svix signatures.
5. **No suppression list** -- Sending to bounced addresses damages reputation.
