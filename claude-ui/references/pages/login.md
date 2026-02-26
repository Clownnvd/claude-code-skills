# Login & Onboarding

## Login Page (/)

Split layout — left: form, right: demo preview.

```tsx
<div className="min-h-screen grid grid-cols-1 md:grid-cols-2">
  {/* Left: form panel */}
  <div className="bg-[#F9F6F0] flex flex-col items-center justify-center px-8 py-12">
    <AnthropicMark className="w-8 h-8 text-[#C96A4A] mb-8" />
    <h1 style={{ fontFamily: "Georgia,'Times New Roman',serif" }}
      className="text-3xl font-bold text-gray-900 text-center mb-2">
      Your ideas, amplified
    </h1>
    <p className="text-[#6B6B6B] text-sm text-center mb-8">
      Privacy-first AI that helps you create in confidence.
    </p>
    {/* Google */}
    <button className="w-full max-w-sm border border-[#E0E0E0] bg-white rounded-lg py-3 flex items-center justify-center gap-3 text-sm text-gray-700 hover:bg-gray-50 cursor-pointer mb-4">
      <GoogleIcon /> Continue with Google
    </button>
    {/* OR divider */}
    <div className="flex items-center gap-4 max-w-sm w-full my-2">
      <div className="flex-1 h-px bg-[#E0E0E0]" />
      <span className="text-xs text-[#6B6B6B]">OR</span>
      <div className="flex-1 h-px bg-[#E0E0E0]" />
    </div>
    {/* Email */}
    <input type="email" placeholder="Enter your personal or work email"
      className="w-full max-w-sm border border-[#E0E0E0] rounded-lg px-4 py-3 text-sm mb-3 focus:outline-none focus:ring-2 focus:ring-[#C96A4A]/30 focus:border-[#C96A4A]" />
    <Link href="/new"
      className="w-full max-w-sm block bg-black text-white text-sm font-medium text-center rounded-lg py-3 hover:bg-gray-800 cursor-pointer">
      Continue with email
    </Link>
    <p className="text-xs text-[#6B6B6B] mt-4">Terms of Service · Privacy Policy</p>
  </div>
  {/* Right: demo preview */}
  <div className="hidden md:flex bg-[#EDE9E1] items-center justify-center px-12">
    <DemoChatPreview /> {/* static chat bubbles */}
  </div>
</div>
```

## Onboarding Flow (5 screens)

All screens: `bg-[#F9F6F0] min-h-screen flex flex-col items-center justify-center`
No sidebar. Logo only: `[✳] Claude` top-center.

**Screen 1: Terms**
"Data, safety, and you" → 3 bullet points → checkbox → `[Continue →]` (bg-black rounded-xl w-full)

**Screen 2: Select Plan**
Same as billing page — 3 columns: Free / Pro / Max. "Stay on Free plan" pre-selected.

**Screen 3: Enter Name**
```
Before we get started, what should I call you?
┌───────────────────────────────────────[→]┐
│ Enter your name                          │
└──────────────────────────────────────────┘
```
`flex border border-[#E0E0E0] rounded-xl overflow-hidden` — input + inline arrow button
Arrow button: `bg-black text-white px-4 flex-shrink-0`, `autoFocus`, `Enter` → next screen

**Screen 4: Topic Picker**
```
What are you into, {firstName}? Pick three topics.

[Coding & developing] [Learning & studying] [Writing & content creation]
[Business & strategy] [Design & creativity] [Life stuff] [Claude's choice]

                                        [Let's go]  ← disabled until 3 selected
```
Unselected pill: `border border-[#E0E0E0] text-[#6B6B6B] rounded-full px-5 py-2.5 text-sm`
Selected pill: `border-gray-900 bg-gray-100 font-medium`
CTA: `bg-gray-800 text-white rounded-full px-8 py-2.5` (enabled when 3 selected)

**Screen 5: AI-generated suggestions**
```
All set! Here are a few ideas to get you started.
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│  Debug code    │  │  Draft a blog  │  │  Explain topic │
└────────────────┘  └────────────────┘  └────────────────┘
Or tell me what you'd like to explore: [input + send]
```
Cards: `border border-[#E0E0E0] rounded-xl p-4 cursor-pointer hover:border-gray-400`
