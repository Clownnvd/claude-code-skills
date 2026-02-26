# Billing / Upgrade Page

**File:** `src/app/(chat)/upgrade/page.tsx`
**Route:** `/upgrade` — accessible from sidebar "Upgrade plan" in account menu

## Layout

```tsx
<div className="flex-1 overflow-y-auto px-6 py-12">
  <div className="max-w-4xl mx-auto">
    <h1 className="text-3xl text-center text-gray-900 mb-2"
      style={{ fontFamily: "Georgia,'Times New Roman',serif" }}>
      Plans that grow with you
    </h1>
    <TabToggle />
    <BillingToggle />
    <PlanCards />
  </div>
</div>
```

## Tab Toggle (Individual / Team)

```tsx
const [tab, setTab] = useState<"individual" | "team">("individual");

<div className="flex justify-center gap-1 mb-6 bg-gray-100 rounded-full p-1 w-fit mx-auto">
  {["individual","team"].map(t => (
    <button key={t} onClick={() => setTab(t as any)}
      className={`px-4 py-1.5 rounded-full text-sm transition-colors duration-200 cursor-pointer capitalize ${
        tab === t ? "bg-white text-gray-900 shadow-sm" : "text-[#6B6B6B]"
      }`}>
      {t === "team" ? "Team & Enterprise" : "Individual"}
    </button>
  ))}
</div>
```

## Billing Toggle (Monthly / Annual)

```tsx
const [billing, setBilling] = useState<"monthly" | "annual">("annual");

<div className="flex justify-center gap-4 mb-8 text-sm">
  <button onClick={() => setBilling("monthly")}
    className={`cursor-pointer ${billing === "monthly" ? "text-gray-900 font-medium" : "text-[#6B6B6B]"}`}>
    Monthly
  </button>
  <button onClick={() => setBilling("annual")}
    className={`cursor-pointer ${billing === "annual" ? "text-gray-900 font-medium" : "text-[#6B6B6B]"}`}>
    Annual <span className="text-[#C96A4A] text-xs font-medium">Save 20%</span>
  </button>
</div>
```

## Plan Data

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

## Plan Card

```tsx
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
      <button disabled={plan.current}
        className={`w-full rounded-lg py-2.5 text-sm font-medium transition-colors duration-200 cursor-pointer ${
          plan.current ? "bg-gray-100 text-gray-500 cursor-default" : "bg-black text-white hover:bg-gray-800"
        }`}>
        {plan.cta}
      </button>
      <ul className="mt-5 space-y-2.5">
        {plan.features.map(f => (
          <li key={f} className="flex items-start gap-2 text-sm text-[#6B6B6B]">
            <CheckIcon className="w-4 h-4 text-gray-400 flex-shrink-0 mt-0.5" />
            {f}
          </li>
        ))}
      </ul>
    </div>
  ))}
</div>
```

**Key details:**
- Pro card: `border-2 border-gray-900` (highlighted) + "Most popular" pill `absolute -top-3`
- Free/Max: `border-2 border-[#E0E0E0]`
- Current plan CTA: `bg-gray-100 text-gray-500 cursor-default disabled`
- Billing tab also appears in Settings → Billing tab (same plan cards, embedded)
