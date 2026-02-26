# Fix Patterns: Content & Copy

Fixes for Content & Copy (8%) and Conversion & CTA (10%) categories — the 18% previously uncovered.

## Headline Fixes

### Generic → specific
```tsx
// Before: vague
"Revolutionize your workflow"
"The best solution for your needs"

// After: specific outcome
"Ship your SaaS in days, not months"
"Save 200+ hours of boilerplate setup"
```

### Feature-dump → benefit-led
```tsx
// Before: what it IS
"Next.js 16 with TypeScript and Prisma"

// After: what it DOES for you
"Full-stack TypeScript — type-safe from database to dashboard"
```

### Headline hierarchy rule
- H1 (hero): promise/outcome — WHY they should care
- H2 (sections): specific benefit per section
- H3 (subsections): feature name → explained by description below

## Social Proof Fixes

### Vague numbers → specific
```tsx
// Before
"Trusted by 100+ developers"
"Thousands of users"

// After
"Trusted by 127 developers"
"Used by 2,412 teams worldwide"
```

### Generic testimonials → credible
```tsx
// Before: no evidence
{ quote: "Great product, highly recommend!" }

// After: specific outcome + attribution
{
  name: "Sarah Chen",
  role: "CTO at Acme",
  quote: "Saved our team 3 weeks. Paid for itself on day 1.",
  metric: "3 weeks saved",
}
```

### Social proof placement
- Near hero CTA (avatar stack + count)
- After features (logos of companies using it)
- Before pricing (testimonials with outcomes)
- Near payment CTA (trust badges, guarantee)

## CTA Copy Fixes

### Weak → action-specific
```tsx
// Before: generic
"Submit"
"Click here"
"Learn more"
"Get started"

// After: action + value
"Get [Product Name] — $99"
"Start building your SaaS"
"Deploy in 5 minutes"
"Claim your lifetime access"
```

### CTA hierarchy (one primary per viewport)
```tsx
// Primary: high contrast, gradient bg, large
className="bg-gradient-primary text-white px-6 py-3 text-sm font-medium"

// Secondary: outline, lower visual weight
className="border border-primary/20 text-foreground px-6 py-3"

// Tertiary: text link only
className="text-primary text-sm underline-offset-4 hover:underline"
```

### CTA placement pattern
1. **Hero**: Primary "Buy" + Secondary "Explore"
2. **After features**: inline "Get started" within context
3. **Pricing card**: Primary "Buy" with price
4. **Final CTA**: Primary "Buy" with guarantee text
5. **Sticky header**: Compact "Buy" on scroll

## Friction Reducer Fixes

### Add microcopy near CTAs
```tsx
// Below primary CTA
<p className="mt-2 text-xs text-muted-foreground">
  30-day money-back guarantee. No questions asked.
</p>

// Below payment form
<p className="text-xs text-muted-foreground">
  Secured by Stripe. We never store your card details.
</p>
```

### Common friction reducers
| Objection | Reducer |
|-----------|---------|
| "Is it worth the money?" | Money-back guarantee, ROI comparison |
| "Is it secure?" | Stripe badge, SSL indicator, "secured by" text |
| "Will it work for me?" | Testimonials with similar use case |
| "Can I get support?" | "Email support included" or community link |
| "What if I need help?" | "Detailed docs included" |

## Content Structure Fixes

### Wall of text → scannable list
Replace paragraphs with `<ul>` + checkmark icons (`<Check className="mt-0.5 size-4 text-primary" />`).

### Feature → benefit transformation
| Feature | Benefit |
|---------|---------|
| "OAuth integration" | "Sign in with GitHub in one click" |
| "Stripe webhooks" | "Payments verified automatically" |
| "i18n support" | "Reach global users — 2 languages included" |
| "Rate limiting" | "Built-in DDoS protection from day one" |

## Voice & Tone

- "you/your" not "we/our" — active voice, present tense
- Sentence case headings — no ALL CAPS
- Numbers over words ("3 steps" not "a few steps")
- No buzzwords ("revolutionary", "cutting-edge", "seamlessly", "leverage")
- One consistent term ("template" not alternating with "starter kit")
