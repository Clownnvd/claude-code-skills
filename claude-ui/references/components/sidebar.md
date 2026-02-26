# Sidebar Component

**File:** `src/components/sidebar.tsx`
**State:** `const [expanded, setExpanded] = useState(false)`

## Collapsed State (w-12 = 48px)

```
[≡]      → setExpanded(true) — w-9 h-9 rounded-lg text-[#6B6B6B] hover:bg-black/5
[+]      → <Link href="/new"> — w-9 h-9 rounded-full bg-[#C96A4A] text-white
[💬]     → <Link href="/recents"> — chat bubble icon
[📁]     → projects — text-[#6B6B6B]/40 disabled, no hover state
[⊞]      → <Link href="#"> — 2×2 grid squares icon (artifacts)
─ mt-auto ─
[ST]     → opens account menu popup — w-8 h-8 rounded-full bg-gray-700
```

**No Anthropic logo. No settings gear icon.** ST avatar at very bottom.

## Expanded State (w-64 = 256px)

```
[≡] Claude              → [≡] collapses, "Claude" = <Link href="/new">
─────────────────────
[◉] New chat            → coral dot (w-6 h-6 rounded-full bg-[#C96A4A]) + text
    Chats               → chat bubble icon + text → /recents
    Projects [Upgrade]  → grayed text-[#6B6B6B]/50 disabled, teal badge
    Artifacts           → 2×2 grid icon + text → #
─────────────────────
Starred                 → section label (NOT uppercase)
  Indian Meal
  Business Management Guide
─────────────────────
Recents                 → section label
  Creative Project Kickoff
  Assessment Questions...
─────────────────────
[ST] Sarah Tyler ↓      → opens account menu popup
     Free plan
```

**"New chat" is a nav item ROW** (coral dot + text), NOT a full-width button.
Section labels: `text-xs font-medium text-[#6B6B6B] mb-1 px-2 py-1` — not uppercase.

## Key Classes

| Element | Class |
|---------|-------|
| Projects badge | `bg-[#E8F4F8] text-[#3B82A0] px-2 py-0.5 rounded-full text-xs font-medium` |
| Active item | `bg-black/8 text-gray-900 font-medium` |
| Inactive item | `text-[#6B6B6B] hover:bg-black/5 hover:text-gray-900 transition-colors duration-200` |
| User bottom block | `flex items-center gap-3 px-2 py-2 rounded-lg hover:bg-black/5 cursor-pointer` |

## Account Menu Popup

Position: `fixed bottom-16 left-3 w-60 bg-white border border-[#E0E0E0] rounded-xl shadow-lg py-1 z-50`

```
tylersarah508@gmail.com     ← text-xs text-[#6B6B6B], border-b border-[#E0E0E0]
─────────────────────────
[ST] Personal        ✓      ← workspace + checkmark SVG (w-4 h-4 text-gray-500)
     Free plan
─────────────────────────
Settings                    ← Link href="/settings"
Language            ›       ← hasArrow: ChevronRight w-4 h-4
Get help
Upgrade plan
Learn more          ›
─────────────────────────
Log out
```

Trigger: click ST avatar (collapsed) or bottom user block (expanded).
Dismiss: `fixed inset-0 z-40` transparent overlay on click.
