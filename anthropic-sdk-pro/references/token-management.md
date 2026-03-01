# Token Management

> Section 7 from the Anthropic SDK reference. Covers token estimation, countTokens() API, usage tracking from responses, max_tokens strategies, and optimization tips.

---

## Token Estimation

- **Rough estimate**: 1 token ~ 4 characters or 0.75 words (English)
- **Vietnamese**: Generally slightly more tokens per word due to diacritics and multi-byte characters
- For exact counts, use the **Token Counting API** before sending:

```ts
const countResult = await anthropic.messages.countTokens({
  model: "claude-sonnet-4-6",
  system: "You are a CV writer.",
  messages: [{ role: "user", content: longPrompt }],
})
console.log(countResult.input_tokens) // Exact count
```

## Usage Tracking from Responses

```ts
const response = await anthropic.messages.create({ /* ... */ })

const usage = response.usage
console.log({
  inputTokens: usage.input_tokens,           // Tokens in your request
  outputTokens: usage.output_tokens,          // Tokens in the response
  cacheWrites: usage.cache_creation_input_tokens,  // New cache entries
  cacheReads: usage.cache_read_input_tokens,       // Cache hits
})
```

## max_tokens Strategy for CViet

| AI Feature | Recommended max_tokens | Reasoning |
|-----------|----------------------|-----------|
| Bullet enhancement | 1024 | Short output, 3-5 bullets |
| Professional summary | 512 | 3-4 sentence paragraph |
| Skill suggestions | 1024 | JSON object with categories |
| CV translation | 4096 | Full CV data structure |
| Full CV review | 2048 | Detailed feedback |

## Optimizing Token Usage

1. **Be concise in system prompts**: Every token counts toward input cost
2. **Use structured output instructions**: "Return ONLY JSON" saves tokens vs. verbose explanations
3. **Limit context**: Send only relevant CV sections, not the entire document
4. **Use `stop_sequences`**: Stop generation early when format is predictable

```ts
const response = await anthropic.messages.create({
  model: MODEL,
  max_tokens: 512,
  stop_sequences: ["\n\n---"],  // Stop when Claude outputs a separator
  messages: [{ role: "user", content: prompt }],
})
```
