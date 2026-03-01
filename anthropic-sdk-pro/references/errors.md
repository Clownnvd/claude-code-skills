# Common Errors Reference

> Section 9 from the Anthropic SDK reference. All 18 documented error entries (AI-001 through AI-018) with exact messages, causes, and fixes.

---

## AI-001: Error Objects Crossing RSC Boundary

| Field | Value |
|-------|-------|
| **Error** | `Error: Objects are not valid as a React child` or serialization errors |
| **Cause** | Anthropic error objects contain non-serializable properties. Passing raw error to client component. |
| **Fix** | Catch and return `{ error: e.message }` plain object. Never pass SDK error objects across the RSC boundary. |

```ts
// BAD
return NextResponse.json({ error }) // SDK error object

// GOOD
return NextResponse.json({ error: error.message }) // Plain string
```

## AI-002: API Key Not Found

| Field | Value |
|-------|-------|
| **Error** | `AuthenticationError: Missing API key` |
| **Cause** | `ANTHROPIC_API_KEY` not set in `.env.local` or not accessible in the runtime environment |
| **Fix** | Add to `.env.local`. Restart dev server. For production, add to hosting env vars. |

## AI-003: Rate Limit Exceeded (429)

| Field | Value |
|-------|-------|
| **Error** | `RateLimitError: 429 {"error":{"type":"rate_limit_error","message":"Rate limit exceeded"}}` |
| **Cause** | Too many requests per minute, or token limit exceeded |
| **Fix** | SDK auto-retries 2x. For app-level, implement user-facing cooldown. Check `retry-after` header. |

```ts
if (error instanceof Anthropic.RateLimitError) {
  const retryAfter = error.headers?.["retry-after"]
  return NextResponse.json(
    { error: "Service busy", retryAfter: Number(retryAfter) || 30 },
    { status: 429 }
  )
}
```

## AI-004: Overloaded (529)

| Field | Value |
|-------|-------|
| **Error** | `APIError: 529 {"error":{"type":"overloaded_error","message":"Overloaded"}}` |
| **Cause** | Anthropic's servers are at capacity |
| **Fix** | SDK auto-retries. Implement exponential backoff on app side. Show user-friendly "Please try again" message. |

## AI-005: Invalid Request (400)

| Field | Value |
|-------|-------|
| **Error** | `BadRequestError: 400 {"error":{"type":"invalid_request_error","message":"..."}}` |
| **Cause** | Malformed request: missing `max_tokens`, invalid `model`, empty `messages`, etc. |
| **Fix** | Validate all parameters before sending. Check model string matches available models. |

## AI-006: Context Length Exceeded

| Field | Value |
|-------|-------|
| **Error** | `BadRequestError: 400 {"error":{"type":"invalid_request_error","message":"prompt is too long"}}` |
| **Cause** | Input tokens + max_tokens exceeds model's context window |
| **Fix** | Use `countTokens()` API before sending. Truncate input or reduce `max_tokens`. |

## AI-007: Streaming Timeout

| Field | Value |
|-------|-------|
| **Error** | `APIConnectionTimeoutError: Request timed out` |
| **Cause** | Network drops idle connection during long generation |
| **Fix** | Use `stream: true` for any request that might take >30 seconds. Increase timeout. |

```ts
// For long requests, always use streaming
const stream = await anthropic.messages.create(
  { /* params */ },
  { timeout: 120000 }  // 2 minutes
)
```

## AI-008: JSON Parsing Failure from Claude

| Field | Value |
|-------|-------|
| **Error** | `SyntaxError: Unexpected token` when parsing Claude's response |
| **Cause** | Claude returned non-JSON text despite instructions |
| **Fix** | Use regex extraction (`text.match(/\{[\s\S]*\}/)`), add retry logic, or use structured outputs. |

```ts
// Robust JSON extraction
try {
  const jsonMatch = text.match(/\{[\s\S]*\}/)
  const data = jsonMatch ? JSON.parse(jsonMatch[0]) : null
  if (!data) throw new Error("No JSON found in response")
} catch {
  return NextResponse.json({ error: "Could not parse AI response" }, { status: 500 })
}
```

## AI-009: Model Not Found

| Field | Value |
|-------|-------|
| **Error** | `NotFoundError: 404 {"error":{"type":"not_found_error","message":"model: ..."}}` |
| **Cause** | Invalid model ID string |
| **Fix** | Use exact model IDs. Check for typos. Available: `claude-sonnet-4-6`, `claude-opus-4-6`, `claude-haiku-4-5`. |

## AI-010: Content Policy Violation

| Field | Value |
|-------|-------|
| **Error** | `BadRequestError: 400 {"error":{"type":"invalid_request_error","message":"Output blocked by content filtering"}}` |
| **Cause** | Claude's safety filters triggered on input or output |
| **Fix** | Review input content. For CV content this is rare but can happen with certain industry terms. Handle gracefully. |

## AI-011: Empty Content Response

| Field | Value |
|-------|-------|
| **Error** | `response.content` is an empty array or first block has no text |
| **Cause** | `max_tokens` too low, `stop_sequences` triggered immediately, or content filtered |
| **Fix** | Check `stop_reason`. Increase `max_tokens`. Verify content isn't blocked. |

```ts
const text = response.content[0]?.type === "text" ? response.content[0].text : ""
if (!text) {
  console.warn(`Empty response. stop_reason: ${response.stop_reason}`)
}
```

## AI-012: TypeScript Compilation Errors

| Field | Value |
|-------|-------|
| **Error** | Various type errors after SDK version update |
| **Cause** | Breaking changes in SDK types between versions |
| **Fix** | Pin SDK version in `package.json`. Check changelog before upgrading. |

## AI-013: Network Connection Error

| Field | Value |
|-------|-------|
| **Error** | `APIConnectionError: Connection error` |
| **Cause** | Cannot reach `api.anthropic.com`. Firewall, DNS, or network issue. |
| **Fix** | Check network connectivity. Verify no proxy/firewall blocking. SDK auto-retries 2x. |

## AI-014: Non-Streaming Request Too Long

| Field | Value |
|-------|-------|
| **Error** | `Error: This request is expected to take longer than 10 minutes. Use stream: true or increase timeout.` |
| **Cause** | SDK estimates request will exceed timeout based on `max_tokens` |
| **Fix** | Use `stream: true` or increase timeout via client/request options. |

## AI-015: Invalid API Key Format

| Field | Value |
|-------|-------|
| **Error** | `AuthenticationError: Invalid API Key` |
| **Cause** | API key has wrong prefix or format (should start with `sk-ant-api03-`) |
| **Fix** | Regenerate key from [console.anthropic.com](https://console.anthropic.com). |

## AI-016: Concurrent Request Limit

| Field | Value |
|-------|-------|
| **Error** | `RateLimitError: 429` with message about requests per minute |
| **Cause** | Exceeding RPM (requests per minute) limit for your tier |
| **Fix** | Queue requests. Implement request pooling. Upgrade API tier. |

## AI-017: Output Truncated

| Field | Value |
|-------|-------|
| **Error** | Response `stop_reason` is `"max_tokens"` and output is incomplete |
| **Cause** | `max_tokens` too low for the requested output |
| **Fix** | Increase `max_tokens`. For CViet translation, use 4096+. Check `stop_reason` in response. |

```ts
if (response.stop_reason === "max_tokens") {
  console.warn("Response was truncated. Consider increasing max_tokens.")
}
```

## AI-018: Prompt Caching Minimum Size

| Field | Value |
|-------|-------|
| **Error** | Cache not being created (no `cache_creation_input_tokens` in usage) |
| **Cause** | Content block is below minimum cacheable size (1024-4096 tokens depending on model) |
| **Fix** | Ensure cached content exceeds minimum threshold. Combine small blocks. |
