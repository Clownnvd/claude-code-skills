# Artifacts Page

**File:** `src/app/(chat)/artifacts/page.tsx`
**Route:** `/artifacts` — nav icon in sidebar (2×2 grid squares)

## List Page Layout

```
┌─────────────────────────────────────────────────────────┐
│ Artifacts                              [+ New artifact] │
│                                                         │
│ [Inspiration] [My artifacts]     ← underline tab toggle │
│                                                         │
│ [All] [Learn] [Life hacks] [Play a game] [Be creative]  │
│ [Touch grass]                     ← category filter     │
│                                                         │
│ ┌────────────────┐ ┌────────────────┐ ┌──────────────┐  │
│ │ [preview img]  │ │ [preview img]  │ │ [preview img]│  │
│ │ Writing editor │ │ Flashcards     │ │ Py Lingo     │  │
│ │ Category       │ │ Category       │ │ Category     │  │
│ └────────────────┘ └────────────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## State

```tsx
const [activeTab, setActiveTab] = useState<"inspiration" | "my">("inspiration");
const [activeCategory, setActiveCategory] = useState("All");
const categories = ["All", "Learn", "Life hacks", "Play a game", "Be creative", "Touch grass"];
```

## Header

```tsx
<header className="flex items-center justify-between px-6 py-4 border-b border-[#E0E0E0]">
  <h1 className="text-xl font-semibold text-gray-900">Artifacts</h1>
  <button className="flex items-center gap-2 bg-black text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-gray-800 cursor-pointer">
    <PlusIcon className="w-4 h-4" /> New artifact
  </button>
</header>
```

## Tab Toggle (underline style)

```tsx
<div className="flex border-b border-[#E0E0E0] px-6">
  {(["inspiration","my"] as const).map(tab => (
    <button key={tab} onClick={() => setActiveTab(tab)}
      className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors duration-200 cursor-pointer ${
        activeTab === tab ? "border-gray-900 text-gray-900" : "border-transparent text-[#6B6B6B] hover:text-gray-900"
      }`}>
      {tab === "inspiration" ? "Inspiration" : "My artifacts"}
    </button>
  ))}
</div>
```

## Category Filter Pills

```tsx
<div className="flex gap-2 px-6 py-3 overflow-x-auto">
  {categories.map(cat => (
    <button key={cat} onClick={() => setActiveCategory(cat)}
      className={`px-4 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors duration-200 cursor-pointer flex-shrink-0 ${
        activeCategory === cat ? "bg-gray-900 text-white" : "bg-white border border-[#E0E0E0] text-[#6B6B6B] hover:border-gray-400"
      }`}>
      {cat}
    </button>
  ))}
</div>
```

## Artifact Card

```tsx
<div className="border border-[#E0E0E0] rounded-xl overflow-hidden hover:border-gray-400 cursor-pointer transition-colors duration-200 bg-white">
  <div className="aspect-video bg-gray-50 border-b border-[#E0E0E0]">
    {/* Preview thumbnail */}
  </div>
  <div className="p-4">
    <p className="text-sm font-medium text-gray-900">{artifact.title}</p>
    <p className="text-xs text-[#6B6B6B] mt-1">{artifact.category}</p>
  </div>
</div>
```

Card grid: `grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-6`

## Split View (artifact open)

```tsx
<div className="flex h-full">
  {/* Chat panel — left 50% */}
  <div className="w-1/2 flex flex-col border-r border-[#E0E0E0]">
    <div className="flex-1 overflow-y-auto px-4 py-6">{messages}</div>
    <div className="border-t border-[#E0E0E0] p-4"><ChatInput /></div>
  </div>
  {/* Artifact panel — right 50% */}
  <div className="w-1/2 flex flex-col">
    {/* Toolbar */}
    <div className="flex items-center gap-2 px-4 py-3 border-b border-[#E0E0E0]">
      <button className="text-sm font-medium text-gray-900 border-b-2 border-gray-900 pb-1">Preview</button>
      <button className="text-sm text-[#6B6B6B] hover:text-gray-900 ml-2">Code</button>
      <div className="ml-auto flex items-center gap-2">
        <button aria-label="Refresh" className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 cursor-pointer">
          <RefreshIcon />
        </button>
        <button aria-label="Download" className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 cursor-pointer">
          <DownloadIcon />
        </button>
        <button aria-label="Share" className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 cursor-pointer">
          <ShareIcon />
        </button>
        <button className="bg-black text-white text-xs font-medium px-3 py-1.5 rounded-lg hover:bg-gray-800 cursor-pointer">
          Publish
        </button>
      </div>
    </div>
    {/* Live preview */}
    <div className="flex-1 bg-white overflow-auto p-4">
      <iframe title="Artifact preview" className="w-full h-full border-0" />
    </div>
  </div>
</div>
```

**Toolbar tabs:** Preview (active = underline `border-b-2 border-gray-900`) / Code (inactive)
**Toolbar actions:** Refresh · Download · Share (icon buttons, 32×32) · Publish (black pill)
