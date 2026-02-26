# Recents Page (/recents)

**File:** `src/app/(chat)/recents/page.tsx`

## Layout

```
Your chat history              [+ New chat]   ← serif h1 + black pill button
───────────────────────────────────────────────
[🔍  Search your chats...                  ]  ← full-width, max-w-2xl
───────────────────────────────────────────────
You have N previous chats with Claude  Select
(search active: There are N chats matching "q"  Select)
"Select" = text-[#3B82A0] hover:underline cursor-pointer
───────────────────────────────────────────────
Chat list:
  ┌──────────────────────────────────────────┐
  │ Chat title                          [🗑] │  ← trash: opacity-0 group-hover:opacity-100
  │ Last message 3 seconds ago               │
  └──────────────────────────────────────────┘
```

## Key Styles

- Header `h1`: serif, `text-2xl text-gray-900`
- "+ New chat": `flex items-center gap-1.5 bg-gray-900 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-gray-700`
- Search container: `relative max-w-2xl mx-auto`
- Search icon: `absolute left-3 top-1/2 -translate-y-1/2 text-[#6B6B6B]`
- Search input: `w-full pl-9 pr-4 py-2.5 border border-[#E0E0E0] rounded-lg bg-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30`
- Cards: `group flex items-center gap-3 px-4 py-3.5 rounded-xl border border-[#E0E0E0] bg-white hover:bg-gray-50`
- **NO preview text** — only title + "Last message X ago"

## Card Structure

```tsx
<div className="group flex items-center gap-3 px-4 py-3.5 rounded-xl border border-[#E0E0E0] bg-white hover:bg-gray-50 transition-colors duration-150 cursor-pointer">
  {/* Checkbox — only in select mode */}
  {isSelecting && (
    <div className={`w-4 h-4 rounded border flex items-center justify-center ${
      selected.has(chat.id) ? "bg-gray-900 border-gray-900" : "border-gray-300 bg-white"
    }`} onClick={e => { e.stopPropagation(); toggleSelect(chat.id); }}>
      {selected.has(chat.id) && <CheckIcon className="w-3 h-3 text-white" />}
    </div>
  )}
  {/* Info — NO preview text */}
  <div className="flex-1 min-w-0">
    <p className="text-sm font-medium text-gray-900 truncate">{chat.title}</p>
    <p className="text-xs text-[#6B6B6B] mt-0.5">Last message {chat.time}</p>
  </div>
  {/* Trash icon — hover only */}
  <button
    className="opacity-0 group-hover:opacity-100 w-7 h-7 flex items-center justify-center rounded-lg text-[#6B6B6B] hover:bg-gray-200"
    onClick={e => { e.stopPropagation(); /* delete */ }}
    aria-label="Delete chat">
    <TrashIcon />
  </button>
</div>
```

## Select Mode Toolbar

```tsx
{isSelecting && selected.size > 0 && (
  <div className="flex items-center gap-4 px-6 py-2 border-b border-[#E0E0E0] max-w-2xl mx-auto w-full">
    <span className="text-sm text-[#6B6B6B]">{selected.size} selected</span>
    <button className="text-sm text-[#3B82A0] hover:underline cursor-pointer">
      {selected.size === filtered.length ? "Deselect all" : "Select all"}
    </button>
    <button className="ml-auto text-sm text-red-600 font-medium cursor-pointer">Delete</button>
    <button className="text-sm text-[#6B6B6B] cursor-pointer"
      onClick={() => { setIsSelecting(false); setSelected(new Set()); }}>
      Cancel
    </button>
  </div>
)}
```

Delete → shows Delete Confirm modal — see `references/components/modals.md`.
