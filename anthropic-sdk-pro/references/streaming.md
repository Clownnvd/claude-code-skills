# Streaming Patterns

> Section 4 from the Anthropic SDK reference. Covers `create()` with `stream: true`, `.stream()` helper, client-side consumption, and stream event types.

---

## Method 1: `create()` with `stream: true` (Lower Memory)

```ts
// src/app/api/ai/stream/route.ts
import { NextRequest } from "next/server"
import { anthropic, MODEL } from "@/lib/claude"

export async function POST(req: NextRequest) {
  const { prompt, system } = await req.json()

  const stream = await anthropic.messages.create({
    model: MODEL,
    max_tokens: 1024,
    system,
    messages: [{ role: "user", content: prompt }],
    stream: true,
  })

  // Convert to ReadableStream for Next.js Response
  const encoder = new TextEncoder()
  const readable = new ReadableStream({
    async start(controller) {
      for await (const event of stream) {
        if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
          controller.enqueue(encoder.encode(`data: ${JSON.stringify({ text: event.delta.text })}\n\n`))
        }
        if (event.type === "message_stop") {
          controller.enqueue(encoder.encode("data: [DONE]\n\n"))
          controller.close()
        }
      }
    },
  })

  return new Response(readable, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive",
    },
  })
}
```

## Method 2: `.stream()` Helper (With Accumulation)

```ts
const stream = anthropic.messages
  .stream({
    model: MODEL,
    max_tokens: 1024,
    system: "You are a CV writing assistant.",
    messages: [{ role: "user", content: prompt }],
  })
  .on("text", (text) => {
    // Handle each text chunk
    console.log(text)
  })

// Get the final accumulated message
const finalMessage = await stream.finalMessage()
console.log(finalMessage.usage) // { input_tokens, output_tokens }
```

## Client-Side Consumption (React)

```tsx
"use client"

import { useState } from "react"

export function AIEnhancer() {
  const [result, setResult] = useState("")
  const [loading, setLoading] = useState(false)

  async function enhance(bullets: string[]) {
    setLoading(true)
    setResult("")

    const res = await fetch("/api/ai/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: bullets.join("\n"), system: "..." }),
    })

    if (!res.ok) throw new Error("Stream failed")
    const reader = res.body!.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value)
      const lines = chunk.split("\n").filter(l => l.startsWith("data: "))
      for (const line of lines) {
        const data = line.slice(6)
        if (data === "[DONE]") break
        const parsed = JSON.parse(data)
        setResult(prev => prev + parsed.text)
      }
    }
    setLoading(false)
  }

  return (/* UI */)
}
```

## Stream Event Types

| Event Type | Description |
|------------|-------------|
| `message_start` | Start of message, contains initial `Message` |
| `content_block_start` | New content block begins |
| `content_block_delta` | Incremental update to content block |
| `content_block_stop` | Content block completed |
| `message_delta` | Changes to the final `Message` (stop_reason, usage) |
| `message_stop` | Stream is done |
| `ping` | Keep-alive event |
