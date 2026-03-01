# Messages API Patterns

> Section 3 from the Anthropic SDK reference. Covers single/multi-turn requests, system prompts, parameters, response structure, and available models.

---

## Single Turn (Simple Request)

```ts
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Improve this bullet point: Managed team projects" }
  ],
})

const text = response.content[0].type === "text" ? response.content[0].text : ""
const { input_tokens, output_tokens } = response.usage
```

## With System Prompt

```ts
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  system: "You are an expert CV writer specializing in the Vietnamese job market.",
  messages: [
    { role: "user", content: "Write a professional summary for a software engineer." }
  ],
})
```

## System Prompt as Array (for Caching)

```ts
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "You are an expert CV writer specializing in the Vietnamese job market. ...(long instructions)...",
      cache_control: { type: "ephemeral" }  // Cache this block for 5 minutes
    }
  ],
  messages: [{ role: "user", content: prompt }],
})
```

## Multi-Turn Conversation

```ts
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  system: "You are a CV writing assistant.",
  messages: [
    { role: "user", content: "Here are my bullet points: ..." },
    { role: "assistant", content: "I've improved them. Here are the results: ..." },
    { role: "user", content: "Can you make them more quantitative?" },
  ],
})
```

## Key Request Parameters

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `model` | string | required | e.g., `"claude-sonnet-4-6"` |
| `max_tokens` | number | required | Max output tokens (model-dependent max) |
| `messages` | array | required | Up to 100,000 messages |
| `system` | string or array | optional | System prompt (no "system" role in messages) |
| `temperature` | number | 1.0 | 0.0-1.0. Use 0 for deterministic, 1 for creative |
| `top_p` | number | optional | Don't combine with temperature |
| `top_k` | number | optional | Advanced sampling control |
| `stop_sequences` | string[] | optional | Custom stop strings |
| `stream` | boolean | false | Enable SSE streaming |
| `metadata` | object | optional | `{ user_id: "hash" }` for abuse detection |

## Response Structure

```ts
interface Message {
  id: string                    // "msg_..."
  type: "message"
  role: "assistant"
  content: ContentBlock[]       // TextBlock | ToolUseBlock | ThinkingBlock
  model: string
  stop_reason: "end_turn" | "stop_sequence" | "max_tokens" | "tool_use"
  stop_sequence: string | null
  usage: {
    input_tokens: number
    output_tokens: number
    cache_creation_input_tokens: number
    cache_read_input_tokens: number
  }
}
```

## Available Models (Feb 2026)

| Model ID | Use Case | Input/MTok | Output/MTok |
|----------|----------|-----------|-------------|
| `claude-opus-4-6` | Most intelligent, agents/coding | $5 | $25 |
| `claude-sonnet-4-6` | Balanced intelligence at scale | $3 | $15 |
| `claude-haiku-4-5` | Fastest, lightweight tasks | $1 | $5 |
| `claude-opus-4-5` | Premium intelligence | $5 | $25 |
| `claude-sonnet-4-5` | Previous gen balanced | $3 | $15 |

**CViet uses `claude-sonnet-4-6`** -- best balance of cost, speed, and quality for CV tasks.
