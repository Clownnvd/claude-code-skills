# Rate Limiting & Usage Tracking

> Section 10 from the Anthropic SDK reference. Covers API rate limits (token bucket algorithm), tier tables (1-4), cache-aware ITPM, response headers, and CViet application-level usage tracking.

---

## Anthropic API Rate Limits (Token Bucket Algorithm)

The API uses a **token bucket algorithm** -- capacity continuously replenishes up to your max, not fixed interval resets.

**Tier 1** (default for new accounts, $5 deposit):

| Model | RPM | ITPM | OTPM |
|-------|-----|------|------|
| Claude Sonnet 4.x | 50 | 30,000 | 8,000 |
| Claude Opus 4.x | 50 | 30,000 | 8,000 |
| Claude Haiku 4.5 | 50 | 50,000 | 10,000 |

**Tier 2** ($40 cumulative deposit):

| Model | RPM | ITPM | OTPM |
|-------|-----|------|------|
| Claude Sonnet 4.x | 1,000 | 450,000 | 90,000 |
| Claude Opus 4.x | 1,000 | 450,000 | 90,000 |
| Claude Haiku 4.5 | 1,000 | 450,000 | 90,000 |

**Tier 3** ($200 cumulative):

| Model | RPM | ITPM | OTPM |
|-------|-----|------|------|
| Claude Sonnet 4.x | 2,000 | 800,000 | 160,000 |
| Claude Opus 4.x | 2,000 | 800,000 | 160,000 |

**Tier 4** ($400 cumulative):

| Model | RPM | ITPM | OTPM |
|-------|-----|------|------|
| Claude Sonnet 4.x | 4,000 | 2,000,000 | 400,000 |
| Claude Opus 4.x | 4,000 | 2,000,000 | 400,000 |

## Cache-Aware ITPM (Key Advantage)

**Cached input tokens do NOT count toward ITPM rate limits** for most models. Only uncached tokens and cache writes count. This means with 80% cache hit rate, your effective throughput is 5x the listed ITPM.

## Response Headers for Rate Limit Monitoring

```ts
// Available in response headers
const headers = {
  "retry-after": "30",                                // Seconds to wait (on 429)
  "anthropic-ratelimit-requests-limit": "1000",        // Max RPM
  "anthropic-ratelimit-requests-remaining": "950",     // Remaining RPM
  "anthropic-ratelimit-tokens-limit": "450000",        // Max ITPM
  "anthropic-ratelimit-tokens-remaining": "400000",    // Remaining ITPM
  "anthropic-ratelimit-input-tokens-limit": "450000",
  "anthropic-ratelimit-input-tokens-remaining": "400000",
  "anthropic-ratelimit-output-tokens-limit": "90000",
  "anthropic-ratelimit-output-tokens-remaining": "85000",
}
```

## CViet Application-Level Usage Tracking

The current CViet implementation uses a **lazy monthly reset** pattern:

```ts
// src/lib/claude.ts (current implementation)

// Free plan: 3 AI enhancements/month
// Pro plan: unlimited

export async function checkAILimit(userId: string): Promise<{ allowed: boolean; remaining: number }> {
  const user = await db.user.findUnique({
    where: { id: userId },
    select: { plan: true, aiUsageThisMonth: true, aiUsageResetAt: true },
  })
  if (!user) return { allowed: false, remaining: 0 }

  // Pro users: unlimited
  if (user.plan === "PRO") return { allowed: true, remaining: Infinity }

  // Lazy monthly reset
  const now = new Date()
  const resetAt = new Date(user.aiUsageResetAt)
  const needsReset = now.getMonth() !== resetAt.getMonth() ||
                     now.getFullYear() !== resetAt.getFullYear()

  if (needsReset) {
    await db.user.update({
      where: { id: userId },
      data: { aiUsageThisMonth: 0, aiUsageResetAt: now },
    })
    return { allowed: true, remaining: 3 }
  }

  const FREE_LIMIT = 3
  const remaining = FREE_LIMIT - user.aiUsageThisMonth
  return { allowed: remaining > 0, remaining }
}
```

## Enhanced Usage Tracking (Recommended Improvement)

```ts
// Track both request count AND token usage
export async function trackAIUsage(
  userId: string,
  inputTokens: number,
  outputTokens: number
) {
  await db.aiUsage.create({
    data: {
      userId,
      inputTokens,
      outputTokens,
      model: MODEL,
      timestamp: new Date(),
      // Estimate cost for monitoring
      estimatedCost: (inputTokens * 3 + outputTokens * 15) / 1_000_000,
    },
  })

  await db.user.update({
    where: { id: userId },
    data: { aiUsageThisMonth: { increment: 1 } },
  })
}
```
