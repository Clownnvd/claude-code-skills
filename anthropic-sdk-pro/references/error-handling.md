# Error Handling

> Section 6 from the Anthropic SDK reference. Covers SDK error classes, automatic retry behavior, retry/timeout configuration, request ID tracking, and the Next.js Route Handler error pattern.

---

## SDK Error Classes

The SDK throws typed errors that extend `APIError`:

```ts
import Anthropic from "@anthropic-ai/sdk"

try {
  const response = await anthropic.messages.create({ /* ... */ })
} catch (error) {
  if (error instanceof Anthropic.APIError) {
    console.log(error.status)    // HTTP status code
    console.log(error.message)   // Error message
    console.log(error.headers)   // Response headers
    // error._request_id available for logging
  }

  // Specific error types
  if (error instanceof Anthropic.AuthenticationError) {
    // 401 - Invalid API key
  } else if (error instanceof Anthropic.PermissionDeniedError) {
    // 403 - Access denied
  } else if (error instanceof Anthropic.NotFoundError) {
    // 404 - Resource not found
  } else if (error instanceof Anthropic.RateLimitError) {
    // 429 - Rate limited
  } else if (error instanceof Anthropic.InternalServerError) {
    // 500+ - Server error
  } else if (error instanceof Anthropic.APIConnectionError) {
    // Network error
  } else if (error instanceof Anthropic.APIConnectionTimeoutError) {
    // Timeout
  }
}
```

## Automatic Retry Behavior

The SDK **automatically retries** these errors 2 times with exponential backoff:

| Error Type | Retried? | Status Code |
|-----------|----------|-------------|
| Connection errors | Yes | N/A |
| Request Timeout | Yes | 408 |
| Conflict | Yes | 409 |
| Rate Limit | Yes | 429 |
| Internal Server Error | Yes | 500+ |
| Authentication Error | No | 401 |
| Permission Denied | No | 403 |
| Bad Request | No | 400 |
| Not Found | No | 404 |

## Configuring Retries

```ts
// Globally
const client = new Anthropic({
  maxRetries: 0,  // Disable retries
})

// Per-request
const response = await client.messages.create(
  { /* params */ },
  { maxRetries: 5 }  // Override for this request
)
```

## Timeout Configuration

```ts
// Global timeout (default: 10 minutes / 600,000ms)
const client = new Anthropic({
  timeout: 30000, // 30 seconds
})

// Per-request timeout
const response = await client.messages.create(
  { /* params */ },
  { timeout: 60000 } // 60 seconds for this request
)
```

**Important**: The SDK throws an error if a non-streaming request is expected to take longer than ~10 minutes. Use `stream: true` for long operations.

## Request ID Tracking

```ts
try {
  const response = await anthropic.messages.create({ /* ... */ })
  console.log(response._request_id) // Log for debugging
} catch (error) {
  if (error instanceof Anthropic.APIError) {
    console.error(`Request ${error._request_id} failed: ${error.message}`)
    // Report this ID to Anthropic support for investigation
  }
}
```

## Next.js Route Handler Error Pattern (CViet)

```ts
// src/app/api/ai/enhance/route.ts
import { NextRequest, NextResponse } from "next/server"
import Anthropic from "@anthropic-ai/sdk"
import { anthropic, MODEL, checkAILimit, callClaude } from "@/lib/claude"

export async function POST(req: NextRequest) {
  try {
    // 1. Auth check
    const session = await auth.api.getSession({ headers: await headers() })
    if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })

    // 2. Rate limit check (app-level)
    const { allowed, remaining } = await checkAILimit(session.user.id)
    if (!allowed) {
      return NextResponse.json(
        { error: "AI usage limit reached", remaining: 0 },
        { status: 429 }
      )
    }

    // 3. Input validation
    const body = await req.json()
    if (!body.bullets?.length) {
      return NextResponse.json({ error: "Missing content" }, { status: 400 })
    }

    // 4. Call Claude
    const { text } = await callClaude(prompt, system, session.user.id)

    // 5. Parse and return
    return NextResponse.json({ result: text, remaining: remaining - 1 })

  } catch (error) {
    // CRITICAL: Serialize errors before returning (RSC boundary issue)
    if (error instanceof Anthropic.RateLimitError) {
      return NextResponse.json(
        { error: "AI service busy. Please try again in a moment." },
        { status: 503 }
      )
    }
    if (error instanceof Anthropic.APIError) {
      console.error(`Claude API error [${error.status}]: ${error.message}`)
      return NextResponse.json(
        { error: "AI service temporarily unavailable." },
        { status: 502 }
      )
    }
    console.error("Unexpected AI error:", error)
    return NextResponse.json(
      { error: "An unexpected error occurred." },
      { status: 500 }
    )
  }
}
```
