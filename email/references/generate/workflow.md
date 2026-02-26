# Generate Mode -- Email System

Generate new email code that meets all 10 categories at 9-10/10.

## Process

1. **Parse request** -- Identify what email functionality to generate (e.g., welcome email, password reset, order confirmation)
2. **Load criteria** -- Read all 4 criteria files from `scoring/criteria/`
3. **Load patterns** -- Read `resend-patterns.md` and `react-email-patterns.md`
4. **Generate code** meeting all 10 categories:
   - Transactional: Service layer with typed functions per email type
   - Templates: React Email components with layout, typed props, responsive
   - Queue: QStash integration with retry, DLQ, signature verification
   - Provider: Resend init with env validation, error handling
   - Deliverability: Env-based from address, domain verification docs
   - Bounce: Webhook endpoint with Svix verification, suppression list
   - Auth: DNS record documentation (SPF/DKIM/DMARC)
   - Rate Limiting: Upstash Ratelimit on email-triggering endpoints
   - Analytics: Webhook event tracking for delivery metrics
   - Testing: PreviewProps, render tests, webhook handler tests
5. **Self-check** -- Score generated code against all 10 categories
6. **Output** -- Fill `assets/templates/generated-code.md.template`

## Files to Generate

| File | Purpose |
|------|---------|
| `src/lib/resend.ts` | Resend client with env validation |
| `src/lib/queue.ts` | QStash client with enqueue function |
| `src/lib/email.ts` | Email service layer with typed send functions |
| `src/lib/rate-limit.ts` | Rate limiting for email endpoints |
| `src/emails/components/layout.tsx` | Shared email layout component |
| `src/emails/[type].tsx` | Template per email type requested |
| `src/app/api/queue/email/route.ts` | Queue worker endpoint |
| `src/app/api/webhooks/resend/route.ts` | Webhook handler |
| `.env.example` | All required environment variables |

## Quality Gate

Generated code must score >= 90/100 (A-) when self-checked. If below, iterate.
