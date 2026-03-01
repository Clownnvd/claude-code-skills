# Cost Optimization

> Section 11 from the Anthropic SDK reference. Covers model selection strategy, prompt caching (90% savings), Batch API (50% off), CViet cost estimation, and optimization checklist.

---

## Model Selection Strategy

| Task | Recommended Model | Cost Impact |
|------|-------------------|-------------|
| Simple bullet improvement | `claude-haiku-4-5` | $1/$5 per MTok (cheapest) |
| Professional summary | `claude-sonnet-4-6` | $3/$15 per MTok (balanced) |
| Complex translation | `claude-sonnet-4-6` | Needs quality for nuance |
| Skill suggestions | `claude-haiku-4-5` | Structured output, doesn't need premium |
| Full CV analysis | `claude-sonnet-4-6` | Requires deeper understanding |

## Prompt Caching (90% Input Cost Reduction)

```ts
// Cache the system prompt for repeated requests
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: `You are an expert CV writer specializing in the Vietnamese job market.
      Your role is to help users create professional, ATS-optimized CVs.
      ... (long detailed instructions, should be 1024+ tokens to meet minimum) ...`,
      cache_control: { type: "ephemeral" }  // 5-minute TTL
    }
  ],
  messages: [{ role: "user", content: userPrompt }],
})

// Cost breakdown:
// First request:  system prompt charged at 1.25x (cache write)
// Next requests:  system prompt charged at 0.1x  (cache read) -- 90% savings!
// Cache read tokens also don't count toward ITPM rate limits
```

**Cache pricing multipliers**:
- Cache write (5m): 1.25x base input price
- Cache write (1h): 2.0x base input price
- Cache read: 0.1x base input price (90% savings)
- Breakeven: Cache hits > 1.15x cache misses (for 5m TTL)

**Minimum cacheable sizes**: 1024-4096 tokens depending on model.

## Batch API (50% Discount)

For non-time-sensitive operations (e.g., nightly CV analysis reports):

```ts
const batch = await anthropic.messages.batches.create({
  requests: cvIds.map((id, i) => ({
    custom_id: `cv-analysis-${id}`,
    params: {
      model: "claude-sonnet-4-6",
      max_tokens: 1024,
      messages: [{ role: "user", content: `Analyze CV: ${cvData[i]}` }],
    },
  })),
})

// Results processed asynchronously (within 24 hours)
// All input/output tokens charged at 50% standard rate
```

## Cost Estimation for CViet

```
Average CV enhancement request:
  Input:  ~500 tokens (system + prompt + bullets)
  Output: ~200 tokens (improved bullets)

Per-request cost (Sonnet 4.6):
  Input:  500 * $3 / 1,000,000 = $0.0015
  Output: 200 * $15 / 1,000,000 = $0.003
  Total:  ~$0.0045 per request

With caching (90% input savings after first request):
  Input:  500 * $0.30 / 1,000,000 = $0.00015
  Output: 200 * $15 / 1,000,000 = $0.003
  Total:  ~$0.00315 per request (30% savings)

Monthly cost estimate (1,000 free-tier users, 3 requests each):
  3,000 requests * $0.0045 = ~$13.50/month

Monthly cost estimate (100 Pro users, 30 requests each):
  3,000 requests * $0.00315 (with caching) = ~$9.45/month
```

## Cost Optimization Checklist

- [ ] Use `claude-haiku-4-5` for simple tasks (3x cheaper)
- [ ] Implement prompt caching for system prompts
- [ ] Set appropriate `max_tokens` (don't over-allocate)
- [ ] Use Batch API for non-real-time operations (50% off)
- [ ] Track actual token usage per user for cost monitoring
- [ ] Consider `stop_sequences` to end generation early
- [ ] Limit context -- send only relevant CV sections
- [ ] Use structured output instructions to avoid verbose responses
