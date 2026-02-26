# Chat Messages

## User Message — LEFT-ALIGNED

**CRITICAL: user messages are left-aligned in Claude.ai — DO NOT use `flex justify-end`.**

```tsx
function UserMessage({ content }: { content: string }) {
  return (
    <div className="flex items-start gap-3">
      <div className="w-7 h-7 rounded-full bg-gray-700 text-white text-xs font-medium flex items-center justify-center flex-shrink-0 mt-0.5">
        ST
      </div>
      <div className="bg-white border border-[#E0E0E0] rounded-2xl rounded-tl-sm px-4 py-2.5 text-sm text-gray-900 shadow-sm max-w-[75%]">
        {content}
      </div>
    </div>
  );
}
```

## Assistant Message

```tsx
function AssistantMessage({ content }: { content: string }) {
  return (
    <div className="flex items-start gap-3">
      <div className="w-7 h-7 rounded-full bg-[#C96A4A] flex items-center justify-center flex-shrink-0 mt-0.5">
        <AnthropicMark className="w-4 h-4 text-white" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-sm text-gray-900 leading-relaxed">
          {content}
        </div>
        <ResponseToolbar />
        <p className="text-xs text-[#6B6B6B] mt-2">
          Claude can make mistakes. Please double-check responses.
        </p>
      </div>
    </div>
  );
}
```

## Response Toolbar — ALWAYS VISIBLE (not hover-only)

```tsx
function ResponseToolbar() {
  return (
    <div className="flex items-center gap-1 mt-2">
      <button className="w-7 h-7 flex items-center justify-center rounded-lg text-[#6B6B6B] hover:bg-black/5 cursor-pointer" aria-label="Copy">
        <CopyIcon />
      </button>
      <button className="w-7 h-7 flex items-center justify-center rounded-lg text-[#6B6B6B] hover:bg-black/5 cursor-pointer" aria-label="Good response">
        <ThumbsUpIcon />
      </button>
      <button className="w-7 h-7 flex items-center justify-center rounded-lg text-[#6B6B6B] hover:bg-black/5 cursor-pointer" aria-label="Bad response">
        <ThumbsDownIcon />
      </button>
      <button className="flex items-center gap-1 px-2 py-1 rounded-lg text-xs text-[#6B6B6B] hover:bg-black/5 cursor-pointer">
        Retry <ChevronDownIcon />
      </button>
    </div>
  );
}
```

Clicking 👍/👎 opens Feedback modal — see `references/components/modals.md`.

## Streaming / Loading State

```tsx
// While isStreaming: show animated Anthropic mark + typing indicator
<div className="flex items-start gap-3">
  <div className="w-7 h-7 rounded-full bg-[#C96A4A] flex items-center justify-center flex-shrink-0 animate-pulse">
    <AnthropicMark className="w-4 h-4 text-white" />
  </div>
  <div className="text-sm text-[#6B6B6B]">...</div>
</div>
```

## AnthropicMark SVG

```tsx
function AnthropicMark({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={className} aria-hidden="true">
      <path d="M12 2L9.5 8.5H3L8.5 12.5L6 19L12 15L18 19L15.5 12.5L21 8.5H14.5L12 2Z" />
    </svg>
  );
}
```

Color: `text-[#C96A4A]` on cream background, `text-white` on brand background.
Refactor tip: extract to `src/components/icons.tsx` to avoid duplication across files.
