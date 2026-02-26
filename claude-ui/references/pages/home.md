# Home Page (/new)

**File:** `src/app/(chat)/new/page.tsx`

## Empty State

```
         [Free plan · Upgrade]             ← text-sm text-[#6B6B6B] centered
                                             "Upgrade" = text-[#C96A4A] cursor-pointer

         [✳] How was your day, Sarah?      ← serif text-3xl, first name only
                                             ✳ = AnthropicMark text-[#C96A4A] inline
    ┌──────────────────────────────────────────┐
    │ How can I help you today?                │
    │  [+] [⇄]              Claude Sonnet 4 ↓ [↑]│
    └──────────────────────────────────────────┘
    Upgrade to connect your tools  ◉ ◉ ◉  [>]

    [◇ Create] [📊 Strategize] [✏ Write] [🎓 Learn] [</> Code]
```

- Max width: `max-w-2xl w-full`
- Pills: `flex items-center gap-1.5 px-4 py-1.5 rounded-full border border-[#E0E0E0] bg-white text-sm cursor-pointer hover:border-gray-400 hover:text-gray-900 transition-colors duration-200`
- No topbar in empty state

## Conversation View

```
[Chat title ↓]                      [Share ↗]   ← topbar (hidden in empty state)
─────────────────────────────────────────────────
                                                  ← flex-1 overflow-y-auto
  max-w-2xl mx-auto px-4 py-6 space-y-6

  [ST] User message (left-aligned)               ← see components/messages.md
  [✳]  Claude response...
       [📋][👍][👎][Retry ↓]                    ← response toolbar ALWAYS visible
─────────────────────────────────────────────────
  px-4 py-4 border-t border-[#E0E0E0]
  <ChatInput placeholder="Reply to Claude..." />
```

## Topbar (conversation only)

```tsx
<header className="flex items-center justify-between px-4 py-3 border-b border-[#E0E0E0] bg-white flex-shrink-0">
  <button
    onClick={() => setRenameOpen(true)}
    className="flex items-center gap-1.5 text-sm font-medium text-gray-900 hover:bg-gray-100 px-2 py-1.5 rounded-lg transition-colors duration-200 cursor-pointer">
    {chatTitle}
    <ChevronDownIcon className="w-4 h-4 text-[#6B6B6B]" />
  </button>
  <button
    onClick={() => setShareOpen(true)}
    className="flex items-center gap-1.5 text-sm text-[#6B6B6B] hover:text-gray-900 hover:bg-gray-100 px-3 py-1.5 rounded-lg transition-colors duration-200 cursor-pointer">
    <ShareIcon className="w-4 h-4" /> Share
  </button>
</header>
```

Clicking title or `↓` opens Rename modal — see `references/components/modals.md`.
Share button opens Share modal — see `references/components/modals.md`.

## Upgrade Banner (below input)

```tsx
<div className="flex items-center gap-3 px-4 py-2.5 border-t border-[#E0E0E0] bg-white">
  <span className="text-xs text-[#6B6B6B] flex-1">
    Upgrade to connect your tools to Claude
  </span>
  <div className="flex items-center gap-1">
    {/* 3 colored tool dots */}
    <span className="w-3 h-3 rounded-full bg-green-500" />
    <span className="w-3 h-3 rounded-full bg-blue-500" />
    <span className="w-3 h-3 rounded-full bg-orange-500" />
  </div>
  <ChevronRightIcon className="w-4 h-4 text-[#6B6B6B] cursor-pointer" />
</div>
```
