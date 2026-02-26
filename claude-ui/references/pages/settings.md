# Settings Page (/settings)

**File:** `src/app/(chat)/settings/page.tsx`
Tabs: `["Profile", "Appearance", "Account", "Privacy", "Billing", "Connectors"]`

## Layout

```tsx
<div className="flex h-full">
  <aside className="w-48 flex-shrink-0 border-r border-[#E0E0E0] py-6 px-4">
    <h1 className="text-base font-semibold text-gray-900 mb-4">Settings</h1>
    {tabs.map(tab => (
      <button key={tab} onClick={() => setActiveTab(tab)}
        className={`w-full text-left px-3 py-2 rounded-lg text-sm mb-0.5 cursor-pointer transition-colors duration-200 ${
          activeTab === tab ? "bg-black/8 text-gray-900 font-medium" : "text-[#6B6B6B] hover:bg-black/5"
        }`}>
        {tab}
      </button>
    ))}
  </aside>
  <main className="flex-1 overflow-y-auto p-8 max-w-3xl">{/* tab content */}</main>
</div>
```

## Profile Tab

Side-by-side 2-column grid for top two fields:

| Field | Type | Value |
|-------|------|-------|
| Full name | text | "Sarah Tyler" |
| What should we call you? | text | "Sarah" |
| What best describes your work? | select | "Design" |
| Personal preferences BETA | textarea | "Keep explanations brief..." |

"Learn about preferences" link inline with the BETA label.
Section wrapped in `border border-[#E0E0E0] rounded-xl p-6`.

## Appearance Tab

**Color mode** — 3 cards: Light / Match system / Dark

```tsx
<div className="grid grid-cols-3 gap-4">
  {["Light", "Match system", "Dark"].map(mode => (
    <label key={mode} className={`border-2 rounded-xl p-4 cursor-pointer transition-colors ${
      colorMode === mode ? "border-blue-500" : "border-[#E0E0E0]"
    }`}>
      <ModePreview mode={mode} />   {/* mini chat preview thumbnail */}
      <p className="text-sm text-center mt-2 font-medium">{mode}</p>
    </label>
  ))}
</div>
```

Selected = `border-2 border-blue-500` (NOT gray/black).

**Chat font** — 3 cards: Default / Match system / Dyslexic friendly

Each card: large `Aa` text in respective font. Same `border-2 border-blue-500` when selected.

## Account Tab

- Email row + Plan info: `divide-y divide-[#E0E0E0]` layout
- "Log out all devices" — `border border-[#E0E0E0] rounded-lg px-4 py-2`
- "Delete account" — red bordered section, triggers Delete Account modal

## Privacy Tab

```tsx
// Toggle rows
[
  { label: "Improve Claude for everyone", sublabel: "...", key: "improve" },
  { label: "Conversation history", sublabel: "...", key: "history" },
].map(item => (
  <div className="flex items-center justify-between py-4 border-b border-[#E0E0E0]">
    <div>
      <p className="text-sm font-medium text-gray-900">{item.label}</p>
      <p className="text-xs text-[#6B6B6B] mt-0.5">{item.sublabel}</p>
    </div>
    <ToggleSwitch />
  </div>
))
// Export data
<button className="bg-black text-white rounded-lg px-4 py-2 text-sm">Export data</button>
```

## Toggle Switch Component

```tsx
function ToggleSwitch({ checked, onChange }: { checked: boolean; onChange: () => void }) {
  return (
    <button role="switch" aria-checked={checked} onClick={onChange}
      className={`relative w-10 h-6 rounded-full transition-colors duration-200 cursor-pointer flex-shrink-0 ${
        checked ? "bg-gray-900" : "bg-gray-200"
      }`}>
      <span className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full shadow-sm transition-transform duration-200 ${
        checked ? "translate-x-4" : ""
      }`} />
    </button>
  );
}
```

## Billing Tab

→ See `references/pages/billing.md` for full plan card spec.
