# Modal Components

All modals share the same wrapper:
```tsx
// Overlay
<div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
     onClick={onClose}>
  // Panel (stop propagation)
  <div className="bg-white rounded-2xl p-6 max-w-sm w-full shadow-xl"
       onClick={e => e.stopPropagation()}>
```

## Rename Chat Modal

```
┌────────────────────────────────────────────┐
│ Rename chat                                │
│ ┌──────────────────────────────────────┐   │
│ │ (empty — old title shown as hint)   │   │  ← autoFocus
│ └──────────────────────────────────────┘   │
│                          [Cancel] [Save]   │
└────────────────────────────────────────────┘
```

- Panel: `max-w-lg` (wider than default)
- Input: `defaultValue=""`, `placeholder={chat.title}`, `autoFocus`
- `Enter` triggers save
- Save: `bg-black text-white rounded-lg px-4 py-2`
- Cancel: `border border-[#E0E0E0] rounded-lg px-4 py-2`

## Share Modal

```
┌────────────────────────────────────────────┐
│ Share chat                            [×]  │
│                                            │
│ 🔒 Private (only you have access)         │  ← toggle row
│                                            │
│ Only messages up until now will be         │
│ shared. Don't share personal info.         │
│                                            │
│                      [Copy link]  [Done]   │
└────────────────────────────────────────────┘
```

- Default state: Private (lock icon)
- Toggle to Public → generates shareable URL
- Done: `bg-black text-white rounded-lg px-4 py-2`

## Feedback Modal (👍 / 👎)

```
┌────────────────────────────────────────────┐
│ Feedback                                   │
│ Please provide details: (optional)         │
│ ┌──────────────────────────────────────┐   │
│ │ What was satisfying about this       │   │  ← thumbs up
│ │ response?                            │   │  ← thumbs down: "What went wrong?"
│ └──────────────────────────────────────┘   │
│ Submitting will send the conversation to   │
│ Anthropic. Learn More                      │
│                         [Submit] [Cancel]  │
└────────────────────────────────────────────┘
```

Textarea: `rows={4}`, `resize-none`, `focus:ring-2 focus:ring-[#C96A4A]/30`
Submit: `bg-black text-white rounded-lg px-4 py-2`

## Delete Confirm Modal (recents bulk delete)

```
┌────────────────────────────────────────────┐
│ Delete N chat(s)?                          │
│ This action cannot be undone.              │
│                       [Cancel]  [Delete]   │
└────────────────────────────────────────────┘
```

Delete: `bg-red-600 text-white rounded-lg hover:bg-red-700`

## Delete Account Modal (settings)

Requires typing "delete my account" to enable confirm button.

```tsx
<input
  value={confirmText}
  onChange={e => setConfirmText(e.target.value)}
  placeholder="delete my account"
  className="w-full border border-[#E0E0E0] rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-red-500/30"
/>
<button
  disabled={confirmText !== "delete my account"}
  className={`w-full rounded-lg py-2.5 text-sm font-medium ${
    confirmText === "delete my account"
      ? "bg-red-600 text-white hover:bg-red-700 cursor-pointer"
      : "bg-gray-100 text-gray-400 cursor-not-allowed"
  }`}>
  Delete account
</button>
```
