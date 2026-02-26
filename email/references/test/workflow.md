# Test Mode -- Email System

Generate tests from scoring criteria covering all 10 categories.

## Process

1. **Map categories to test assertions** -- Each category maps to specific test types
2. **Generate test files** -- Create test files per area
3. **Output** -- Fill `assets/templates/test-suite.md.template`

## Category -> Test Mapping

| Category | Test Type | Key Assertions |
|----------|-----------|---------------|
| Transactional Email | Integration | Service functions callable, correct template selected |
| Templates & Rendering | Unit | `render()` produces valid HTML, typed props enforced |
| Queue & Delivery | Integration | QStash publish succeeds, worker processes message |
| Provider Integration | Unit | Resend client initializes, env vars validated |
| Deliverability | Config | From address from env, domain verification docs exist |
| Bounce Handling | Integration | Webhook processes bounce/complaint, suppression updated |
| Email Auth | Config | DNS records documented, DMARC policy set |
| Rate Limiting | Integration | Endpoint returns 429 after limit exceeded |
| Analytics | Integration | Webhook events logged, metrics queryable |
| Testing & Preview | Meta | PreviewProps defined, render tests exist |

## Test File Structure

```
src/
  lib/__tests__/
    email.test.ts         -- Service layer tests
    queue.test.ts         -- Queue integration tests
    rate-limit.test.ts    -- Rate limiting tests
  emails/__tests__/
    welcome.test.ts       -- Template render tests
    layout.test.ts        -- Layout component tests
  app/api/webhooks/resend/__tests__/
    route.test.ts         -- Webhook handler tests
```

## Coverage Target

Every category should have at least 2 test cases. Total minimum: 20 tests.
