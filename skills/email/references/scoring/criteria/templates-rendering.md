# Scoring Criteria: Email Templates & Rendering (12%) + Testing & Preview (6%)

## Email Templates & Rendering (12%)

Measures component system, responsive design, plain text fallback, and dynamic content.

### Point Breakdown

| Points | Requirement |
|--------|------------|
| 0 | No templates; raw HTML strings or no email content |
| 1 | Single hardcoded HTML string in send call |
| 2 | Multiple HTML strings but no component system |
| 3 | Basic React Email components without shared layout |
| 4 | Shared layout component but no responsive design |
| 5 | Responsive layout with Tailwind but missing plain text fallback |
| 6 | Full component system: layout, typed props, responsive, plain text |
| 7 | + Reusable components (buttons, headers, footers), consistent styling |
| 8 | + Dynamic content rendering, conditional sections, locale support |
| 9 | + Template versioning, design system alignment, accessibility (alt text) |
| 10 | + Multi-variant templates, dark mode support, comprehensive component lib |

### What to Check

- `src/emails/` -- Does a templates directory exist with `.tsx` files?
- `src/emails/components/` -- Are there shared layout and reusable components?
- `render()` usage -- Is `@react-email/render` used to convert components to HTML?
- Plain text -- Is `render(template, { plainText: true })` called for text version?
- Tailwind -- Is `<Tailwind>` wrapper used for responsive styles?
- Props typing -- Do templates have TypeScript interfaces for props?

### Common Issues

| Score | Issue | Severity |
|-------|-------|----------|
| 0-2 | Raw HTML strings instead of React Email components | CRITICAL |
| 3 | No shared layout; each template duplicates structure | HIGH |
| 4-5 | No responsive design or plain text fallback | HIGH |
| 6-7 | No typed props; templates accept `any` | MEDIUM |

---

## Testing & Preview (6%)

Measures preview server, render tests, integration tests, and email client compatibility.

### Point Breakdown

| Points | Requirement |
|--------|------------|
| 0 | No email testing at all |
| 1 | Manual testing by sending real emails only |
| 2 | `PreviewProps` defined but no automated tests |
| 3 | Basic render tests that check for non-empty HTML output |
| 4 | Render tests with content assertions (subject, key text) |
| 5 | + Snapshot tests for template output consistency |
| 6 | + Webhook handler tests with mock payloads |
| 7 | + Queue worker tests with mock messages, integration tests |
| 8 | + Email client compatibility testing (Litmus/Email on Acid) |
| 9 | + Automated visual regression tests, accessibility checks |
| 10 | + Full CI pipeline: render, lint, preview, client test, deploy |

### What to Check

- `PreviewProps` -- Do templates export preview props for `email dev`?
- Test files -- Do `*.test.ts` files exist for email service and templates?
- Render tests -- Do tests call `render()` and assert on output content?
- Webhook tests -- Are webhook handlers tested with mock Svix signatures?
- Queue tests -- Are queue workers tested with mock messages?
- CI integration -- Are email tests part of the CI pipeline?

### Common Issues

| Score | Issue | Severity |
|-------|-------|----------|
| 0-1 | No testing; only manual verification | HIGH |
| 2-3 | No render tests for templates | HIGH |
| 4-5 | No webhook or queue handler tests | MEDIUM |
| 6-7 | No email client compatibility testing | LOW |
