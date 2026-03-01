# Polar Appendices

> Appendices A-D from the Polar Payment SDK Comprehensive Reference.
> Covers Polar vs Stripe comparison, CViet file map, pricing configuration, and sources.

---

## Appendix A: Polar vs Stripe Quick Comparison

| Feature | Polar | Stripe |
|---------|-------|--------|
| Pricing model | Merchant of Record (MoR) | Payment processor |
| Tax handling | Polar handles all taxes | You handle (or add Stripe Tax) |
| Pricing | 4% + $0.40/tx | 2.9% + $0.30/tx |
| Monthly fee | None | None (core) |
| Setup complexity | Low | Medium-High |
| Dashboard | Developer-focused | Feature-rich but complex |
| Target audience | Indie devs, SaaS | Everyone |
| Subscription billing | Built-in | Stripe Billing (add-on) |
| Customer portal | Built-in hosted | Stripe Customer Portal |
| Webhook spec | Standard Webhooks | Custom |

## Appendix B: CViet File Map

| File | Purpose |
|------|---------|
| `src/lib/polar.ts` | Polar SDK instance |
| `src/app/api/polar/route.ts` | Webhook handler |
| `src/app/api/polar/checkout/route.ts` | Checkout session creation |
| `src/app/(app)/billing/page.tsx` | Billing page with plan comparison |
| `src/proxy.ts` | Auth guard (excludes API routes) |
| `.env` | `POLAR_ACCESS_TOKEN`, `POLAR_WEBHOOK_SECRET`, `POLAR_PRO_PRODUCT_ID` |

## Appendix C: Pricing Configuration

Polar supports these pricing types:
- **Fixed** -- standard price (e.g., $5/month)
- **Pay-what-you-want** -- optional minimum and default amounts
- **Free** -- $0 products
- **Seat-based** -- per-seat pricing with $0/seat option
- **Metered** -- usage-based billing via events

Currencies supported: USD, EUR, GBP, CAD, AUD, JPY, CHF, SEK, INR, BRL.
Polar auto-detects customer location and displays appropriate currency.

## Appendix D: Sources

- [Polar Official Docs](https://polar.sh/docs)
- [Polar Next.js Integration Guide](https://polar.sh/docs/guides/nextjs)
- [Polar Next.js Adapter](https://polar.sh/docs/integrate/sdk/adapters/nextjs)
- [Polar API Reference](https://polar.sh/docs/api-reference/introduction)
- [Polar API Changelog](https://polar.sh/docs/changelog/api)
- [Polar Customer State](https://polar.sh/docs/integrate/customer-state)
- [Polar Customer Portal](https://polar.sh/docs/features/customer-portal)
- [Polar Embedded Checkout](https://polar.sh/docs/features/checkout/embed)
- [Polar Webhook Delivery](https://polar.sh/docs/integrate/webhooks/delivery)
- [Polar Products](https://polar.sh/docs/features/products)
- [@polar-sh/nextjs on npm](https://www.npmjs.com/package/@polar-sh/nextjs)
- [@polar-sh/sdk on npm](https://www.npmjs.com/package/@polar-sh/sdk)
- [Polar GitHub - polar-js](https://github.com/polarsource/polar-js)
- [Polar Better Auth Plugin](https://www.better-auth.com/docs/plugins/polar)
- [Hookdeck Polar Webhook Guide](https://hookdeck.com/webhooks/platforms/guide-to-polar-webhooks-features-and-best-practices)
- [Polar vs Stripe Comparison](https://polar.sh/resources/comparison/stripe)
- [Polar Pricing](https://polar.sh/resources/pricing)
- [CViet Project - Ecosystem Compatibility](ecosystem-compatibility.md)
- [CViet Project - Next.js 16 Research](nextjs16-research.md)
