# Vercel AI SDK Integration

> Section 12 from the Anthropic SDK reference. Covers installation, provider setup, streamText, generateText, useChat hook, structured output, prompt caching, extended thinking, and when to use each approach.

---

## Installation

```bash
pnpm add ai @ai-sdk/anthropic
```

## Provider Setup

```ts
// Using the provider
import { anthropic } from "@ai-sdk/anthropic"
// Auto-reads ANTHROPIC_API_KEY from env

// Or create custom instance
import { createAnthropic } from "@ai-sdk/anthropic"
const anthropic = createAnthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
  // baseURL, headers, fetch options available
})
```

## streamText in Route Handler

```ts
// src/app/api/chat/route.ts
import { streamText } from "ai"
import { anthropic } from "@ai-sdk/anthropic"

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = streamText({
    model: anthropic("claude-sonnet-4-6"),
    system: "You are a CV writing assistant.",
    messages,
  })

  return result.toDataStreamResponse()
}
```

## generateText (Non-Streaming)

```ts
import { generateText } from "ai"
import { anthropic } from "@ai-sdk/anthropic"

const { text, usage } = await generateText({
  model: anthropic("claude-sonnet-4-6"),
  prompt: "Improve this bullet point: Managed team projects",
})
```

## useChat Hook (Client Component)

```tsx
"use client"

import { useChat } from "ai/react"

export function CVAssistant() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat",
    // Defaults to POST /api/chat
  })

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>{m.role}: {m.content}</div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button type="submit" disabled={isLoading}>Send</button>
      </form>
    </div>
  )
}
```

## Structured Output with AI SDK

```ts
import { generateObject } from "ai"
import { anthropic } from "@ai-sdk/anthropic"
import { z } from "zod"

const { object } = await generateObject({
  model: anthropic("claude-sonnet-4-6"),
  schema: z.object({
    skills: z.array(z.object({
      category: z.string(),
      items: z.array(z.string()),
    })),
  }),
  prompt: "Suggest skills for a frontend developer in Vietnam",
})
// object is fully typed and validated
```

## Prompt Caching with AI SDK

```ts
import { generateText } from "ai"
import { anthropic } from "@ai-sdk/anthropic"

const result = await generateText({
  model: anthropic("claude-sonnet-4-6"),
  messages: [
    {
      role: "system",
      content: "Long system prompt...",
      providerOptions: {
        anthropic: {
          cacheControl: { type: "ephemeral" },
        },
      },
    },
    { role: "user", content: userMessage },
  ],
})
```

## Extended Thinking with AI SDK

```ts
import { generateText } from "ai"
import { anthropic } from "@ai-sdk/anthropic"

const { text, reasoningText } = await generateText({
  model: anthropic("claude-sonnet-4-6"),
  prompt: "Complex analysis task...",
  providerOptions: {
    anthropic: {
      thinking: { type: "enabled", budgetTokens: 12000 },
    },
  },
})
```

## When to Use Each Approach

| Approach | When to Use |
|----------|-------------|
| **Direct `@anthropic-ai/sdk`** | Full API control, batch API, tool runner, MCP integration |
| **Vercel AI SDK `ai` + `@ai-sdk/anthropic`** | Streaming chat UIs, `useChat` hook, easy provider switching, structured output |

**CViet currently uses direct SDK** -- suitable for its use case of discrete API calls (enhance, summarize, translate). The Vercel AI SDK would be beneficial if adding a chat-based CV assistant feature.
