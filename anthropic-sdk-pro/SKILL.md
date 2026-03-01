---
name: anthropic-sdk-pro
description: "Anthropic SDK (Claude AI) for Next.js 16. Messages API, streaming, tool use, prompt engineering, token optimization, 18 documented errors. Triggers: anthropic, claude, ai, claude api, streaming, tool use, prompt, ai enhancement, ai sdk."
---

# Anthropic SDK Pro -- Claude AI for Next.js 16

## When to Use

Trigger on any mention of: anthropic, claude, claude api, ai sdk, ai enhancement, streaming response, tool use, function calling, prompt engineering, token counting, ai rate limit, claude sonnet, claude haiku.

## Reference Files

Load the relevant file(s) from `references/` based on the task:

| File | Content |
|------|---------|
| `setup.md` | SDK compatibility (version matrix, runtime), client init, env vars, API key security |
| `messages-api.md` | Single/multi-turn requests, system prompts, parameters, response structure, models + pricing |
| `streaming.md` | `stream: true` vs `.stream()`, SSE route handlers, client-side consumption, event types |
| `tool-use.md` | JSON Schema tools, agentic loop, Zod-based tools, tool choice, structured output via tools |
| `error-handling.md` | SDK error classes, auto retry behavior, timeout config, request ID tracking, Route Handler pattern |
| `token-management.md` | Token estimation, countTokens() API, usage tracking, max_tokens strategies, optimization tips |
| `cv-ai-patterns.md` | 6 prompts: bullet enhance, summary, skills, translate, ATS, cover letter + endpoint table |
| `errors.md` | 18 error entries (AI-001 through AI-018) with exact messages, causes, and fixes |
| `rate-limiting.md` | Tier tables (1-4), RPM/ITPM/OTPM limits, cache-aware ITPM, app-level usage tracking |
| `cost-optimization.md` | Model selection, prompt caching (90% savings), Batch API (50% off), CViet cost estimates |
| `vercel-ai-sdk.md` | @ai-sdk/anthropic, streamText, generateText, useChat, structured output, extended thinking |
| `security.md` | Input sanitization, prompt injection prevention, output validation, defense-in-depth |
| `prompt-engineering.md` | General principles, system prompt template, temperature guide, output format, structured output |

## Error Quick Lookup

| ID | Error | Fix |
|----|-------|-----|
| AI-001 | Error objects crossing RSC boundary | Catch + return `{ error: e.message }` plain object |
| AI-002 | 401 authentication_error | Check `ANTHROPIC_API_KEY` env var |
| AI-003 | 429 rate_limit_error | Implement exponential backoff, check tier limits |
| AI-004 | 529 overloaded_error | Retry with delay, SDK auto-retries 2x |
| AI-005 | 400 invalid_request_error | Validate all params before sending |
| AI-006 | Context length exceeded | Truncate input, use `countTokens()` before sending |
| AI-007 | Streaming timeout | Set `maxDuration` in route config, use `stream: true` |
| AI-008 | JSON parsing failure | Use regex extraction or structured outputs |
| AI-009 | Model not found | Use exact model ID: `claude-sonnet-4-6` |
| AI-010 | Content policy violation | Review input, handle gracefully |
| AI-011 | Empty content response | Check `stop_reason`, increase `max_tokens` |
| AI-012 | TypeScript compilation errors | Pin SDK version, check changelog |
| AI-013 | Network connection error | Check connectivity, SDK auto-retries 2x |
| AI-014 | Non-streaming request too long | Use `stream: true` or increase timeout |
| AI-015 | Invalid API key format | Must start with `sk-ant-api03-`, regenerate key |
| AI-016 | Concurrent request limit | Queue requests, upgrade API tier |
| AI-017 | Output truncated | Increase `max_tokens`, check `stop_reason` |
| AI-018 | Prompt caching minimum size | Content must exceed 1024-4096 token threshold |

## Key Patterns

### CV Bullet Enhancement
```tsx
// app/api/ai/enhance/route.ts
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-6',
  max_tokens: 1024,
  system: 'You are an expert CV writer. Rewrite bullet points to be impactful and ATS-friendly.',
  messages: [{ role: 'user', content: `Rewrite these bullets:\n${bullets.join('\n')}` }]
})
```

### Streaming in Route Handler
```tsx
export async function POST(req: Request) {
  const stream = await anthropic.messages.stream({
    model: 'claude-sonnet-4-6',
    max_tokens: 1024,
    messages: [{ role: 'user', content: prompt }]
  })
  return new Response(stream.toReadableStream())
}
```

### Usage Tracking (Free/Pro Gating)
```tsx
if (user.plan === 'FREE' && user.aiUsageThisMonth >= 3) {
  return NextResponse.json({ error: 'AI limit reached' }, { status: 429 })
}
await db.user.update({ where: { id: user.id }, data: { aiUsageThisMonth: { increment: 1 } } })
```
