# Chat Input Component

**File:** `src/components/chat-input.tsx`

## Layout

```
┌──────────────────────────────────────────────────┐
│ How can I help you today?             (textarea) │
│                                                  │
│ [+] [⇄]               Claude Sonnet 4 ↓  [↑]   │
└──────────────────────────────────────────────────┘
Upgrade to connect your tools  ◉ ◉ ◉  [>]   ← BELOW input, separate div
```

Container: `border border-[#E0E0E0] rounded-xl bg-white shadow-sm overflow-hidden`

## Textarea

- Auto-resize: `textareaRef.current.style.height = scrollHeight + "px"` in `onInput`, max 200px
- `Enter` sends message, `Shift+Enter` = newline
- Placeholder: "How can I help you today?" (home) / "Reply to Claude..." (conversation)

## Toolbar Buttons

| Button | State | Class |
|--------|-------|-------|
| `+` Attach | default | `w-8 h-8 rounded-lg text-[#6B6B6B] hover:bg-gray-100` |
| `×` Close | when menu open | same — shows `CloseIcon` instead of `PlusIcon` |
| `⇄` Style | always | same — shows `StyleIcon` (sliders, NOT bolt) |
| Model | always | `text-xs text-[#6B6B6B] hover:text-gray-900 flex items-center gap-1` |
| `↑` Send | enabled | `w-8 h-8 rounded-full bg-[#C96A4A] text-white hover:bg-[#B05A3C]` |
| `↑` Send | disabled | `w-8 h-8 rounded-full bg-gray-200 text-gray-400 cursor-not-allowed` |
| `■` Stop | isStreaming | `w-8 h-8 rounded-full bg-gray-900 text-white hover:bg-gray-700` |

## StyleIcon SVG (3 lines of decreasing length — NOT a bolt)

```tsx
function StyleIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 6h13M8 12h9m-9 6h5" />
    </svg>
  );
}
```

## StopIcon SVG

```tsx
function StopIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
      <rect x="6" y="6" width="12" height="12" rx="2" />
    </svg>
  );
}
```

## Upload Dropdown (from `+` button)

Position: `absolute bottom-full left-0 mb-2 w-52 rounded-xl border border-[#E0E0E0] bg-white shadow-lg py-1 z-20`
Options: "Upload a file" / "Take a screenshot" / "Add from GitHub"

## Style Picker Dropdown (from `⇄` button)

Position: same as upload, `w-52`
Options: `✓ Normal` / `Concise` / `Explanatory` / `Formal` / `─────` / `Create & edit styles`

## Props Interface

```tsx
interface ChatInputProps {
  onSend?: (message: string) => void;
  onStop?: () => void;
  placeholder?: string;
  isStreaming?: boolean;
}
```
