---
name: claude-ui
description: "Full Claude.ai UI clone for Next.js 16 App Router + Tailwind v4. Covers all 19 flows, exact design tokens, every component (sidebar, chat-input, messages, settings, recents, login, onboarding, billing), animation patterns, accessibility, and known bugs. Use when: building Claude-like AI chat UI, cloning claude.ai, implementing any screen or flow of this project. Triggers: sidebar, chat input, shell, new chat, recents, settings, onboarding, login, billing, appearance, artifacts, share modal, account menu, response toolbar."
---

# Claude UI — Complete Implementation Guide

This skill is the single source of truth for recreating Claude.ai in Next.js 16 + Tailwind v4.
Source: PageFlows (July 2025 — 19 flows, 100+ screenshots).
Project root: `c:\nextjs_project\pulse-analytics`

---

## Project Structure

```
src/
  app/
    page.tsx                  # Login page (split: form left / demo preview right)
    layout.tsx                # Root layout (metadata only)
    globals.css               # Design tokens + scrollbar + focus ring
    (chat)/
      layout.tsx              # App shell: <Sidebar> + <main>
      new/page.tsx            # Home + chat conversation
      recents/page.tsx        # Chat history with search + multi-select
      settings/page.tsx       # Settings tabs (6 tabs)
  components/
    sidebar.tsx               # Collapsible sidebar (collapsed=w-12 / expanded=w-64)
    chat-input.tsx            # Textarea + toolbar (attach / style / model / send)
```

---

## Design Tokens (globals.css — Tailwind v4 @theme inline)

```css
@theme inline {
  --color-cream: #F9F6F0;        /* bg-cream — page background */
  --color-brand: #C96A4A;        /* bg-brand — coral: logo, send btn, new chat */
  --color-brand-hover: #B05A3C;  /* hover:bg-brand-hover */
  --color-surface: #FFFFFF;      /* bg-surface — cards, inputs */
  --color-text-primary: #0F0F0F; /* text-text-primary */
  --color-text-muted: #6B6B6B;   /* text-text-muted */
  --color-border: #E0E0E0;       /* border-border */
}
```

**Token usage:** IDE warns when arbitrary values are used instead of tokens — both styles work, but tokens are canonical. Acceptable to use either in this project.

---

## Color System

| Role | Token class | Hex |
|------|------------|-----|
| Page background | `bg-cream` or `bg-[#F9F6F0]` | `#F9F6F0` |
| Card / Input surface | `bg-white` | `#FFFFFF` |
| Brand accent | `bg-brand` | `#C96A4A` |
| Brand hover | `hover:bg-brand-hover` | `#B05A3C` |
| Primary text | `text-gray-900` / `text-[#0F0F0F]` | `#0F0F0F` |
| Muted text | `text-[#6B6B6B]` | `#6B6B6B` |
| Border | `border-[#E0E0E0]` | `#E0E0E0` |
| CTA button | `bg-black text-white` | `#000000` |
| Dark bg | `bg-[#1A1A1A]` | dark mode |

---

## Typography

```
Headings:   font-family: Georgia, 'Times New Roman', serif
            → apply inline: style={{ fontFamily: "Georgia, 'Times New Roman', serif" }}
Body:       system-ui (set in globals.css body)
Code:       font-mono
```

---

## App Shell Layout

```tsx
// src/app/(chat)/layout.tsx
import { Sidebar } from "@/components/sidebar";
export default function ChatLayout({ children }) {
  return (
    <div className="flex h-screen bg-[#F9F6F0] overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        {children}
      </div>
    </div>
  );
}
```

---

## Sidebar Component — Full Spec

**File:** `src/components/sidebar.tsx`

### Collapsed state (w-12 = 48px) — Verified from screenshot
```
[≡]          ← menu toggle (w-9 h-9 rounded-lg) → expands sidebar
[+]          ← new chat (rounded-full bg-[#C96A4A] text-white) → Link href="/new"
[💬]         ← chat/recents icon → /recents
[📁]         ← projects icon (text-[#6B6B6B]/40, disabled — no hover)
[⊞]          ← artifacts icon (2×2 grid squares) → href="#"
[spacer mt-auto]
[ST]         ← user avatar (w-8 h-8 rounded-full bg-gray-700) → opens account menu
```
**IMPORTANT:** No Anthropic logo in collapsed view. No settings gear icon. ST avatar at very bottom opens account menu, NOT /settings.

### Expanded state (w-64 = 256px) — Verified from screenshot
```
[≡]  Claude          ← top bar: menu collapse btn + "Claude" text (Link to /new)
─────────────────────
[◉] New chat          ← nav item: coral dot (w-6 h-6 rounded-full bg-[#C96A4A]) + "New chat" text
    Chats             ← nav item with chat bubble icon
    Projects [Upgrade]← nav item: grayed out, teal badge: bg-[#E8F4F8] text-[#3B82A0]
    Artifacts         ← nav item with 2×2 grid squares icon
─────────────────────
★ Starred             ← section header (text-xs font-medium text-[#6B6B6B])
  Indian Meal
  Business Management Guide
─────────────────────
Recents               ← section header
  Creative Project Kickoff
  Assessment Questions...
  UX design
─────────────────────
[ST] Sarah Tyler ↓    ← bottom user block with ChevronDown, opens account menu popup
     Free plan
```
**IMPORTANT:** "New chat" in expanded sidebar is a NAV ITEM ROW (coral dot + text), NOT a separate full-width button. ↓ chevron is on the user block at the bottom.

### Key rules
- Toggle button: `w-9 h-9 rounded-lg text-[#6B6B6B] hover:bg-black/5`
- New chat in collapsed: `<Link href="/new">` coral rounded-full — NEVER `window.location.href`
- New chat in expanded: nav item `flex items-center gap-3 px-3 py-2` with `w-6 h-6 rounded-full bg-[#C96A4A]` dot on left
- Projects Upgrade badge: `bg-[#E8F4F8] text-[#3B82A0] px-2 py-0.5 rounded-full text-xs font-medium` (teal, NOT blue)
- Active nav item: `bg-black/8 text-gray-900 font-medium` (black/8 is valid in Tailwind v4)
- Inactive nav item: `text-[#6B6B6B] hover:bg-black/5 hover:text-gray-900`
- All transitions: `transition-colors duration-200`
- Section headers: `text-xs font-medium text-[#6B6B6B] mb-1 px-2 py-1` (NOT uppercase)

---

## Chat Input Component — Full Spec

**File:** `src/components/chat-input.tsx`

```
┌──────────────────────────────────────────────────────┐
│ How can I help you today?                 (textarea) │
│                                                      │
│ [+] [⇄]              Claude Sonnet 4 ↓  [↑send]    │
├──────────────────────────────────────────────────────┤
│ Upgrade to connect your tools to Claude  ◉ ◉ ◉ [>] │
└──────────────────────────────────────────────────────┘
```

- Container: `border border-[#E0E0E0] rounded-xl bg-white shadow-sm overflow-hidden`
- Textarea: auto-resize via `scrollHeight`, max-height 200px, `resize: none` (set in globals.css)
- Send: `Enter` sends (not `Shift+Enter`), `Shift+Enter` = newline
- Send button enabled: `bg-[#C96A4A] text-white rounded-full w-8 h-8` with `↑` arrow icon
- Send button disabled: `bg-gray-200 text-gray-400 cursor-not-allowed`
- Left toolbar: `[+]` attach button, `[⇄]` style/tune button (sliders icon, NOT lightning bolt)
- Right toolbar: model selector + send button
- Model selector: `"Claude Sonnet 4 ↓"` plain text button `text-xs text-[#6B6B6B]`
- Upgrade notice separator: **`border-t border-[#E0E0E0]`** — NOT `border-gray-50` (too faint, bug)
- Upgrade notice row: text + 3 colored tool icons + `>` chevron link

**Style button icon (⇄) — correct SVG:**
```tsx
function StyleIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 6h13M8 12h9m-9 6h5" />
    </svg>
  );
}
```

---

## Home Screen (`/new` — empty state)

```
         Free plan · Upgrade              ← top center, small text

         [✳] How was your day, Sarah?    ← serif font, text-3xl/4xl
                                          ← first name only (NOT full name)
         ┌──────────────────────────────────────┐
         │ How can I help you today?            │
         │   [+] [⇄]       Claude Sonnet 4 ↓ [↑]│
         ├──────────────────────────────────────┤
         │ Upgrade to connect your tools  ◉◉◉ >│
         └──────────────────────────────────────┘

         [Create] [Strategize] [Write] [Learn] [Code]
```

- "Free plan · Upgrade": `text-sm text-[#6B6B6B]` centered at top — "Upgrade" is coral link
- Greeting: serif font, `text-3xl` or `text-4xl`, uses **first name only** (Sarah, not Sarah Tyler)
- Anthropic mark `✳` is coral `text-[#C96A4A]`, inline before greeting text
- Max width input: `max-w-2xl w-full`
- Quick action pills: `px-4 py-1.5 rounded-full border border-[#E0E0E0] bg-white text-sm` with icons
- Pill icons: Create (diamond), Strategize (chart), Write (pencil), Learn (graduation cap), Code (`</>`)
- Pill hover: `hover:border-gray-400 hover:text-gray-900 transition-colors duration-200`
- Top bar: NO title when empty state, no Share button

## Conversation View (`/chat/{uuid}` — messages present)

```
Header:
  [Conversation Title  ↓]                  [Share ↗]
  ← left-aligned title with chevron         right-aligned

Messages area (flex-1 overflow-y-auto px-4 py-6):
  max-w-2xl mx-auto space-y-6

  User bubble: ← LEFT-ALIGNED (confirmed from screenshots — NOT right-aligned like typical chat apps)
    flex items-start gap-3
    → ST avatar: w-7 h-7 rounded-full bg-gray-700 text-white text-xs font-medium (left side)
    → bubble: bg-white border border-[#E0E0E0] rounded-2xl rounded-tl-sm px-4 py-2.5
    → max-w-[75%] shadow-sm text-sm text-gray-900
    CRITICAL: DO NOT use flex justify-end for user messages — Claude.ai shows them left-aligned

  Assistant bubble:
    [✳]  Response text here...
         → avatar: w-7 h-7 rounded-full bg-[#C96A4A] (Anthropic mark)
         → content: text-sm leading-relaxed
         → toolbar (ALWAYS visible, not just on hover — confirmed from screenshots):
            [📋 copy] [👍] [👎] [↺ Retry ↓]
            Retry has dropdown chevron (→ regenerate / regenerate with different model)
            all: text-[#6B6B6B] hover:bg-black/5
         → below toolbar: "Claude can make mistakes. Please double-check responses."

Loading indicator:
  [✳] (Anthropic mark animated, spinning or pulsing)

Bottom input bar:
  px-4 py-4 border-t border-[#E0E0E0]
  <ChatInput placeholder="Reply to Claude..." />
  Note: placeholder changes to "Reply to Claude..." in conversation (not "How can I help...")
```

- **Topbar title**: clicking the chat name or `↓` chevron → opens Rename modal
- **Share button**: top-right with share icon + "Share" text
- **Sidebar**: stays collapsed (icon-only) during conversation

---

## Recents Page (`/recents`)

### Layout (from actual screenshot)
```
Header:
  h1 "Your chat history"            [+ New chat]  ← black pill button, right-aligned
  Search bar (full-width max-w-3xl) focused with blue border

  "You have N previous chats with Claude   Select"  ← "Select" is a coral/blue link

Chat list (NOT date-grouped in actual — just a flat list with card layout):

  Chat card (large):
    bg-white border border-[#E0E0E0] rounded-xl p-4
    Title: text-sm font-medium text-gray-900
    Subtitle: "Last message X time ago" — text-xs text-[#6B6B6B]
    → NO preview text snippet shown (unlike original implementation)
```

**Key corrections vs current codebase:**
- The current `recents/page.tsx` shows preview snippets — actual Claude does NOT show these
- Cards show only title + "Last message X ago" timestamp
- "+ New chat" button is in the **header**, top-right (black pill), not just in sidebar
- Search bar has full-width focus ring (blue, not coral)

**Navigation bug:** always use `router.push()` from `useRouter()` — never `window.location.href`.

---

## Settings Page (`/settings`)

### Layout
```tsx
<div className="flex h-full">
  <aside className="w-48 flex-shrink-0 border-r border-[#E0E0E0] py-6 px-4">
    <h1>Settings</h1>
    <nav> {tabs} </nav>
  </aside>
  <main className="flex-1 overflow-y-auto p-8">
    {activeTab content}
  </main>
</div>
```

### Tabs: Profile · Appearance · Account · Privacy · Billing · Connectors

**Active tab:** `bg-black/8 text-gray-900 font-medium rounded-lg`

### Profile tab (`/settings/profile`) — Accurate from screenshot
- **Full name** input (text): "Sarah Tyler"
- **What should we call you?** input (text): "Sarah" — this is the display/first name
- **What best describes your work?** dropdown: options like Design, Engineering, Marketing, etc.
- **What personal preferences should Claude consider in responses? BETA** — label + "Learn about preferences" link
  - Textarea below: freeform text like "Keep explanations brief and to the point"
- **Feature preview** section (below main form):
  - "Preview and provide feedback on upcoming enhancements to our platform. Note: experimental features might influence Claude's behavior and differ from the standard experience."
  - Toggle switches for each feature preview item
- Save button: `bg-black text-white rounded-lg px-4 py-2`

### Appearance tab (`/settings/appearance`) — Accurate from screenshot
- **Color mode** section:
  - 3 cards in a row: Light / Match system / Dark
  - Each card shows a mini chat preview (shows sample chat input + send button)
  - Selected card has a blue/indigo border `border-2 border-blue-500` (browser selection style)
  - Label below each card: "Light", "Match system", "Dark"
- **Chat font** section:
  - 3 cards in a row: Default / Match system / Dyslexic friendly
  - Each card shows large "Aa" text in the respective font
  - Selected card has blue border
  - Label below: "Default", "Match system", "Dyslexic friendly"

### Account tab
- Email + Plan info in bordered rows (`divide-y divide-[#E0E0E0]`)
- Log out all devices + Delete account (red border)
- Delete modal: confirm text "delete my account" required, disabled button until match

### Privacy tab
- 2 toggles: "Improve Claude for everyone" + "Conversation history"
- Export data section with CTA `bg-black text-white`

### Billing tab
- 3 plan cards: Free $0 / Pro $17/mo / Max $100+/mo
- Current plan: `border-gray-900` highlight, disabled CTA
- Others: `bg-black text-white` CTA

### ToggleSwitch component
```tsx
function ToggleSwitch() {
  const [on, setOn] = useState(false);
  return (
    <button role="switch" aria-checked={on} onClick={() => setOn(!on)}
      className={`relative w-10 h-6 rounded-full transition-colors duration-200 cursor-pointer flex-shrink-0 ${on ? "bg-gray-900" : "bg-gray-200"}`}>
      <span className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full shadow-sm transition-transform duration-200 ${on ? "translate-x-4" : ""}`} />
    </button>
  );
}
```

---

## Login Page (`/`)

```
┌───────────────────────┬──────────────────────────┐
│ [✳] Claude            │                          │
│                       │    Demo chat preview     │
│ Your ideas,           │    (3 bubbles, bg-gray)  │
│ amplified             │                          │
│                       │                          │
│ [G] Continue w Google │                          │
│ ─────── OR ──────────│                          │
│ [email input        ] │                          │
│ [Continue with email] │                          │
│ Terms · Privacy       │                          │
└───────────────────────┴──────────────────────────┘
```

- Left: `bg-[#F9F6F0]` flex col items-center justify-center px-8 py-12
- Right: `hidden md:flex bg-[#EDE9E1]` (slightly darker cream)
- Heading: serif `text-3xl font-bold`
- Google button: `border border-[#E0E0E0] bg-white rounded-lg` with inline Google SVG
- Email input: `focus:ring-2 focus:ring-[#C96A4A]/30 focus:border-[#C96A4A]`
- CTA: `bg-black text-white rounded-lg` (Continue with email → Link to /new)
- Demo preview: static chat bubbles in white cards, max-w-sm

---

## Onboarding Flow — 18 Screens (Accurate from PageFlows)

Background: `bg-[#F9F6F0]` throughout all onboarding screens.

### Screen 1 — Login (`/login`)
Split layout, two columns:
- **Left** (`bg-[#F9F6F0]`): Anthropic logo top-left, "Your ideas, amplified" (large serif), "Privacy-first AI..." tagline, [G] Continue with Google button, OR divider, email input, "Continue with email" (black button), "Terms · Privacy" footer
- **Right** (`bg-[#EDE9E1]` slightly darker cream): Demo chat preview (a conversation showing Claude generating a bar chart visualization)

### Screen 2 — Google OAuth (popup)
Standard browser OAuth popup:
- "Sign in with Google" header, Anthropic logo
- "Choose an account to continue to Anthropic"
- Account row: avatar + name + email (e.g. "Sarah Tyler / tylersarah508@gmail.com")
- "Use another account" option
- Privacy policy + terms links

### Screen 3 — Agree to Terms (`/onboarding`)
Centered, minimal chrome:
```
                    [✳ Anthropic logo]
         "Data, safety, and you"
         "How Anthropic ensures a safe AI experience"

         • [icon] bullet 1 about data
         • [icon] bullet 2 about safety
         • [icon] bullet 3 about privacy

         ☐ I agree to Anthropic's Consumer Terms and Acceptable Use
           Policy and confirm that I am at least 18 years of age

         ☐ Subscribe to occasional product update and promotional
           emails. You can opt out at any time.

         [          Continue          ]  ← black full-width button

         Email verified as user@gmail.com / Use a different email
```

### Screen 4 — Pricing in Onboarding (`/upgrade/pro`)
3-column layout (Free / Pro / Max):
```
     [flower icon]   [flower icon]   [flower icon]
     Free             Pro              Max
     Try Claude       For everyday     5-20x more usage
                      productivity     than Pro
     $0               $17              From $100
                      /month billed    /month billed
                      annually         monthly
     [Stay on Free]   [Get Pro plan]   [Get Max plan]
     ← outlined btn   ← black btn     ← black btn

     ✓ Chat on web, iOS, and Android
     ✓ Generate code and visualize data   Everything in Free, plus:   Everything in Pro, plus:
     ✓ Write, edit, and create content    ✓ More usage*               ✓ Choose 5x or 20x more
     ✓ Analyze text and images            ✓ Access Claude Code         usage than Pro*
     ✓ Ability to search the web          ✓ Unlimited Projects         ✓ Higher output limits
                                          ✓ Connect Google Workspace   ✓ Early access to advanced
                                          ✓ Remote MCP integrations     Claude features
                                          ✓ Extended thinking          ✓ Priority access at high
                                          ✓ More Claude models           traffic times
```
Footer: "Prices shown do not include applicable tax. *Usage limits apply."

### Screen 5 — Select Plan continuation
Same pricing page, accessed from `/onboarding` URL path.

### Screen 6 — Enter Name (`/onboarding`)
```
                  [✳ Anthropic mark centered]

     Before we get started, what should I call you?

     ┌────────────────────────────────────────[↑]┐
     │ Enter your name                            │
     └────────────────────────────────────────────┘
     ← single input with ↑ button INSIDE the right edge
     ← button is gray when empty, becomes active when typed
```
- Input: full-width rounded rectangle `border border-[#E0E0E0] rounded-xl`
- Submit `↑` button: inside input, right side, `rounded-lg` NOT `rounded-full`
- Button is `bg-gray-200` disabled, `bg-gray-700 text-white` when enabled

### Screen 7 — Topic Picker (`/onboarding`)
```
     What are you into, {firstName}? Pick three topics to explore.

     [</> Coding & developing   ] [📖 Learning & studying   ]
     [✏️  Writing & content creation]
     [📊 Business & strategy    ] [🎨 Design & creativity   ]
     [💙 Life stuff             ] [💡 Claude's choice       ]

                    [Let's go]  ← gray disabled, 3 must be selected
```
- Topics: pill buttons `px-4 py-2.5 border border-[#E0E0E0] rounded-full bg-white text-sm`
- Selected: `border-gray-900 bg-gray-50` or similar dark border
- Topic list: "Coding & developing", "Learning & studying", "Writing & content creation", "Business & strategy", "Design & creativity", "Life stuff", "Claude's choice"
- "Let's go": `bg-gray-400 text-white rounded-full px-6 py-2` disabled → `bg-gray-800` when 3 selected

### Screen 8 — Topics Selected (same screen, 3 selected)
Same UI but 3 topics highlighted, "Let's go" button becomes active (dark/black).

### Screen 9 — Auto-generated Chat (after "Let's go")
- Navigates to `/chat/{uuid}` with conversation title matching selected topic
- Shows AI-generated prompt sent automatically based on selected topic
- Chat interface shows: expanded prompt text in user bubble, Claude thinking

### Screen 10 — Claude Responding
- Shows the full response loading, Claude typing

### Screen 11 — Response + Artifact Split View
```
┌──── Chat (left ~50%) ─────┬──── Artifact (right ~50%) ──────┐
│ [user message bubble]     │ [◉] [↺] [copy icon]    Publish  │
│                           │                                   │
│ [✳] Perfect! I'll create  │  [Artifact Title]                │
│     an interactive habit  │  Subtitle                        │
│     tracker...            │                                   │
│     Key features:         │  <live rendered content>         │
│     • Click to complete   │                                   │


---

## Flow 14 — Style Picker (⚡) + Upload Dropdown (+)

### ⚡ Style Picker (in chat-input toolbar)

```
┌────────────────────────────┐
│ ✓ Normal                   │
│   Concise                  │
│   Explanatory              │
│   Formal                   │
│ ─────────────────────────  │
│   Custom styles ›          │
│   Create & edit styles     │
└────────────────────────────┘
```

**Implementation:**
```tsx
const [styleOpen, setStyleOpen] = useState(false);
const [activeStyle, setActiveStyle] = useState("Normal");
const styles = ["Normal", "Concise", "Explanatory", "Formal"];

// In chat-input toolbar (⇄ sliders button — NOT a bolt/lightning icon):
<div className="relative">
  <button onClick={() => setStyleOpen(!styleOpen)}
    className="w-8 h-8 flex items-center justify-center rounded-lg text-[#6B6B6B] hover:bg-gray-100 transition-colors duration-200 cursor-pointer"
    aria-label="Response style">
    <StyleIcon />  {/* d="M8 6h13M8 12h9m-9 6h5" — three lines of decreasing length */}
  </button>
  {styleOpen && (
    <>
      <div className="fixed inset-0 z-10" onClick={() => setStyleOpen(false)} />
      <div className="absolute bottom-full left-0 mb-2 w-52 bg-white border border-[#E0E0E0] rounded-xl shadow-lg py-1 z-20">
        {styles.map(style => (
          <button key={style} onClick={() => { setActiveStyle(style); setStyleOpen(false); }}
            className="w-full flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 cursor-pointer">
            <span className="w-4">{activeStyle === style ? "✓" : ""}</span>
            {style}
          </button>
        ))}
        <div className="h-px bg-[#E0E0E0] my-1" />
        <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 cursor-pointer">
          Create & edit styles
        </button>
      </div>
    </>
  )}
</div>
```

### + Upload Dropdown (in chat-input toolbar)

```
┌──────────────────────────┐
│ 📎 Upload a file         │
│ 📷 Take a screenshot     │
│ 🔗 Add from GitHub       │
└──────────────────────────┘
```

**Note:** No emojis as icons — use SVG icons (PaperClipIcon, CameraIcon, LinkIcon).

```tsx
const [uploadOpen, setUploadOpen] = useState(false);
const uploadOptions = [
  { label: "Upload a file", icon: <PaperClipIcon /> },
  { label: "Take a screenshot", icon: <CameraIcon /> },
  { label: "Add from GitHub", icon: <GitHubIcon /> },
];

// + button:
<div className="relative">
  <button onClick={() => setUploadOpen(!uploadOpen)} aria-label="Attach file">
    <PlusIcon />
  </button>
  {uploadOpen && (
    <>
      <div className="fixed inset-0 z-10" onClick={() => setUploadOpen(false)} />
      <div className="absolute bottom-full left-0 mb-2 w-48 bg-white border border-[#E0E0E0] rounded-xl shadow-lg py-1 z-20">
        {uploadOptions.map(opt => (
          <button key={opt.label}
            className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 cursor-pointer">
            <span className="text-[#6B6B6B]">{opt.icon}</span>
            {opt.label}
          </button>
        ))}
      </div>
    </>
  )}
</div>
```

---

## Flow 15 — Upgrade Page (`/upgrade`)

**Route:** `src/app/(chat)/upgrade/page.tsx`

```
┌─────────────────────────────────────────────────────────┐
│                Plans that grow with you                 │
│                                                         │
│        [Individual] [Team & Enterprise]                 │
│        [Monthly] [Annual — save 20%]                   │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Free    │  │  Pro  ★  │  │  Max     │             │
│  │  $0      │  │ $17/mo   │  │ $100+/mo │             │
│  │          │  │ billed   │  │          │             │
│  │          │  │ annually │  │          │             │
│  │[Stay Free│  │[Get Pro] │  │[Get Max] │             │
│  │          │  │ Popular  │  │          │             │
│  │ ✓ Access │  │ ✓ 5x use │  │ ✓ Highest│             │
│  │ ✓ Limited│  │ ✓ Projects│  │ ✓ API    │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
```

**Plan data:**
```tsx
const plans = [
  {
    name: "Free", price: "$0", period: "",
    description: "For personal use and exploration",
    cta: "Stay on Free plan", current: true,
    features: ["Access to Claude","Limited messages per day","Basic file uploads"],
  },
  {
    name: "Pro", price: "$17", period: "/mo",
    description: "Billed annually ($20/mo monthly)",
    cta: "Get Pro", popular: true, current: false,
    features: ["5× more usage than Free","Priority access during peak times","Projects & Artifacts","Advanced models including Sonnet"],
  },
  {
    name: "Max", price: "$100+", period: "/mo",
    description: "For professionals with high demands",
    cta: "Get Max", current: false,
    features: ["Highest usage limits","Extended thinking","API access","Custom response styles"],
  },
];
```

**Layout:**
```tsx
export default function UpgradePage() {
  const [billing, setBilling] = useState<"monthly" | "annual">("annual");
  const [tab, setTab] = useState<"individual" | "team">("individual");

  return (
    <div className="flex-1 overflow-y-auto px-6 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl text-center text-gray-900 mb-2"
          style={{ fontFamily: "Georgia,'Times New Roman',serif" }}>
          Plans that grow with you
        </h1>
        {/* Tab toggle */}
        <div className="flex justify-center gap-1 mb-6 bg-gray-100 rounded-full p-1 w-fit mx-auto">
          {["individual","team"].map(t => (
            <button key={t} onClick={() => setTab(t as any)}
              className={`px-4 py-1.5 rounded-full text-sm transition-colors duration-200 cursor-pointer capitalize ${tab === t ? "bg-white text-gray-900 shadow-sm" : "text-[#6B6B6B]"}`}>
              {t === "team" ? "Team & Enterprise" : "Individual"}
            </button>
          ))}
        </div>
        {/* Billing toggle */}
        <div className="flex justify-center gap-4 mb-8 text-sm">
          <button onClick={() => setBilling("monthly")} className={`cursor-pointer ${billing==="monthly" ? "text-gray-900 font-medium" : "text-[#6B6B6B]"}`}>Monthly</button>
          <button onClick={() => setBilling("annual")} className={`cursor-pointer ${billing==="annual" ? "text-gray-900 font-medium" : "text-[#6B6B6B]"}`}>
            Annual <span className="text-[#C96A4A] text-xs font-medium">Save 20%</span>
          </button>
        </div>
        {/* Plan cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map(plan => (
            <div key={plan.name}
              className={`border-2 rounded-2xl p-6 relative ${plan.popular ? "border-gray-900" : "border-[#E0E0E0]"}`}>
              {plan.popular && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-3 py-1 rounded-full">
                  Most popular
                </span>
              )}
              <h3 className="font-semibold text-gray-900">{plan.name}</h3>
              <p className="text-xs text-[#6B6B6B] mt-0.5 mb-4">{plan.description}</p>
              <div className="flex items-baseline gap-0.5 mb-4">
                <span className="text-3xl font-bold text-gray-900">{plan.price}</span>
                <span className="text-sm text-[#6B6B6B]">{plan.period}</span>
              </div>
              <button className={`w-full rounded-lg py-2.5 text-sm font-medium transition-colors duration-200 cursor-pointer ${
                plan.current ? "bg-gray-100 text-gray-500 cursor-default" : "bg-black text-white hover:bg-gray-800"
              }`} disabled={plan.current}>
                {plan.cta}
              </button>
              <ul className="mt-5 space-y-2.5">
                {plan.features.map(f => (
                  <li key={f} className="flex items-start gap-2 text-sm text-[#6B6B6B]">
                    <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-gray-400 flex-shrink-0 mt-0.5">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    {f}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

---

## Flow 1 — Onboarding (Full Screen Map)

**Route group:** `src/app/(onboarding)/` or as standalone pages.

### Screen 1: Agree to terms (`/onboarding`)
```
         [✳] Claude

         Data, safety, and you

         • Conversations may be reviewed to improve Claude
         • You can opt out in settings
         • We never sell your personal data

         ☑ I agree to the Terms of Service

         [Continue →]  (bg-black rounded-xl w-full)
```

### Screen 2: Select plan
→ Same as Upgrade page (3 columns), with "Stay on Free plan" highlighted/pre-selected.

### Screen 3: Enter name
```
         Before we get started, what should I call you?

         ┌─────────────────────────────┬────┐
         │ Enter your name             │ →  │
         └─────────────────────────────┴────┘
```
- Input + arrow button inline: `flex border border-[#E0E0E0] rounded-xl overflow-hidden`
- Arrow button: `bg-black text-white px-4 flex-shrink-0`
- `autoFocus` on input, `Enter` triggers next step

### Screen 4: Topic picker
```
         What are you into, Sarah? Pick three topics.

         [Coding] [Learning] [Writing] [Business]
         [Design] [Life stuff] [Claude's choice]

         [Let's go]
```
- Pills: `px-5 py-2.5 border rounded-full text-sm cursor-pointer`
- Selected: `border-gray-900 bg-gray-100 font-medium`
- Unselected: `border-[#E0E0E0] text-[#6B6B6B] hover:border-gray-400`
- CTA disabled until 3 selected: `bg-gray-800 text-white px-8 py-2.5 rounded-full`
- Progress: track `selectedTopics.size >= 3` to enable button

### Screen 5: AI-generated suggestions
```
         All set! Here are a few ideas to get you started.

         ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
         │ 🔧 Debug my code   │  │ 📝 Draft a blog     │  │ 💡 Explain a topic │
         └────────────────────┘  └────────────────────┘  └────────────────────┘

              Or tell me what you'd like to explore:
         ┌─────────────────────────────────────────────┐
         │ How can I help you today?           [↑ Send]│
         └─────────────────────────────────────────────┘
```
- Cards: `border border-[#E0E0E0] rounded-xl p-4 cursor-pointer hover:border-gray-400`
- Clicking a card: pre-fills chat input and navigates to `/new`

**General onboarding rules:**
- No sidebar during onboarding — full-screen centered layout
- `bg-[#F9F6F0] min-h-screen flex flex-col items-center justify-center`
- Logo only: `[✳] Claude` top-center, no nav
- Black `rounded-xl` for primary CTA ("Continue")

---

## Flow 4 — Artifacts Page (`/artifacts`)

**Route:** `src/app/(chat)/artifacts/page.tsx`

### List page layout
```
┌─────────────────────────────────────────────────────────┐
│ Artifacts                              [+ New artifact] │
│                                                         │
│ [Inspiration] [My artifacts]     ← tab toggle          │
│                                                         │
│ [All] [Learn] [Life hacks] [Play a game] [Be creative] │
│ [Touch grass]                     ← category filter    │
│                                                         │
│ ┌────────────────┐ ┌────────────────┐ ┌──────────────┐ │
│ │ Writing editor │ │ Flashcards     │ │ Py Lingo     │ │
│ │ [preview img]  │ │ [preview img]  │ │ [preview img]│ │
│ │ Category       │ │ Category       │ │ Category     │ │
│ └────────────────┘ └────────────────┘ └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**State:**
```tsx
const [activeTab, setActiveTab] = useState<"inspiration" | "my">("inspiration");
const [activeCategory, setActiveCategory] = useState("All");
const categories = ["All", "Learn", "Life hacks", "Play a game", "Be creative", "Touch grass"];
```

**Header:**
```tsx
<header className="flex items-center justify-between px-6 py-4 border-b border-[#E0E0E0]">
  <h1 className="text-xl font-semibold text-gray-900">Artifacts</h1>
  <button className="flex items-center gap-2 bg-black text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-gray-800 cursor-pointer">
    <PlusIcon /> New artifact
  </button>
</header>
```

**Tab toggle:**
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

**Category filter pills:**
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

**Artifact card:**
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

### Split view (artifact open)

```tsx
<div className="flex h-full">
  {/* Chat panel */}
  <div className="w-1/2 flex flex-col border-r border-[#E0E0E0]">
    <div className="flex-1 overflow-y-auto px-4 py-6">
      {messages}
    </div>
    <div className="border-t border-[#E0E0E0] p-4">
      <ChatInput />
    </div>
  </div>
  {/* Artifact panel */}
  <div className="w-1/2 flex flex-col">
    {/* Toolbar */}
    <div className="flex items-center gap-2 px-4 py-3 border-b border-[#E0E0E0]">
      <button className="text-sm font-medium text-gray-900 border-b-2 border-gray-900 pb-1">Preview</button>
      <button className="text-sm text-[#6B6B6B] hover:text-gray-900 ml-2">Code</button>
      <div className="ml-auto flex items-center gap-2">
        <button aria-label="Refresh" className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 cursor-pointer"><RefreshIcon /></button>
        <button aria-label="Download" className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 cursor-pointer"><DownloadIcon /></button>
        <button aria-label="Share" className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 cursor-pointer"><ShareIcon /></button>
        <button className="bg-black text-white text-xs font-medium px-3 py-1.5 rounded-lg hover:bg-gray-800 cursor-pointer">Publish</button>
      </div>
    </div>
    {/* Live preview */}
    <div className="flex-1 bg-white overflow-auto p-4">
      <iframe title="Artifact preview" className="w-full h-full border-0" />
    </div>
  </div>
</div>
```

---

## Common Bugs & Fixes

| Bug | Fix |
|-----|-----|
| `window.location.href = "/new"` in onClick | Use `<Link href="/new">` or `router.push("/new")` |
| `border-t border-gray-50` (invisible border) | Use `border-[#E0E0E0]` |
| AnthropicMark defined in multiple files | Extract to `src/components/icons.tsx` |
| `bg-black/8` Tailwind warning | Valid in v4 — ignore, or use `bg-black/[0.08]` |
| Textarea not auto-resizing | Set `height = scrollHeight` in onInput handler |
| Modal not dismissing on outside click | Add `fixed inset-0 z-0 onClick={close}` underlay |
| Sidebar not scroll when many chats | Add `overflow-y-auto` to expanded nav container |

---

## Navigation Rules

- **Always use Next.js navigation** — never `window.location.href` in any component
- For `<button>` that navigates: replace with `<Link href="...">` from `next/link`
- For programmatic navigation in event handlers: use `useRouter().push()` from `next/navigation`
- Both `Link` and `useRouter` do client-side navigation (no full page reload)

---

## Accessibility Checklist

- [ ] All icon buttons have `aria-label`
- [ ] SVG icons have `aria-hidden="true"`
- [ ] Toggle switches have `role="switch"` + `aria-checked`
- [ ] Form inputs paired with `<label htmlFor>` or `aria-label`
- [ ] Focus ring: defined in globals.css as `outline: 2px solid #C96A4A`
- [ ] Min touch target: 44×44px (or 36×36 with larger clickable parent)
- [ ] Transitions respect `prefers-reduced-motion` (add if needed)

---

## Tailwind v4 Notes for This Project

- `@theme inline` in globals.css defines design tokens as utility classes
- `bg-black/8` is valid (arbitrary opacity) — IDE warns but it compiles correctly
- `@import "tailwindcss"` replaces the old `@tailwind base/components/utilities`
- Custom tokens: `bg-cream`, `bg-brand`, `bg-brand-hover`, `border-border`, `text-text-muted`
- IDE may warn "use `border-border` instead of `border-[#E0E0E0]`" — both work

---

## When to Use This Skill vs ultimateuiux

| Task | Use |
|------|-----|
| Building any screen of this Claude clone project | **claude-ui** |
| Designing a new AI product from scratch | **ultimateuiux** |
| Need color palettes / font pairings for a different product | **ultimateuiux** |
| Need Claude.ai exact flows, tokens, component specs | **claude-ui** |
| Debugging sidebar / chat-input / settings in this project | **claude-ui** |
