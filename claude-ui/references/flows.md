# 19 Flows Quick Reference

Source: PageFlows (July 2025). Screenshots saved in `screenshots/flows/`.

| # | Flow | Key screens / entry point |
|---|------|--------------------------|
| 1 | Onboarding | Login → Terms → Plan → Name → Topics → Chat |
| 2 | Update profile | /settings → Profile tab |
| 3 | Chat bot | /new → messages → streaming → response toolbar |
| 4 | Creating artifacts | Chat → artifact split view → Publish modal |
| 5 | Giving feedback | 👍/👎 → Feedback modal |
| 6 | Rename conversation | Topbar title ↓ → Rename modal |
| 7 | Appearance settings | /settings → Appearance tab |
| 8 | Export data | /settings → Privacy tab → Export |
| 9 | Disconnect devices | /settings → Account tab |
| 10 | Help center | Account menu → Get help |
| 11 | Log out | Account menu → Log out |
| 12 | Log in | / split layout → Google / email |
| 13 | Settings | /settings/* → 6 tabs |
| 14 | General browsing | Sidebar, style picker, account menu |
| 15 | Upgrade account | /upgrade → 3 plan cards |
| 16 | Add to favorites | Chat ⋮ → "Add to favorites" → Starred section |
| 17 | Search | /recents → search bar → filtered results |
| 18 | Share | Topbar "Share" → Share modal |
| 19 | Delete account | /settings → Account → confirm modal |

## Navigation Rules

Always use Next.js navigation — never `window.location.href`:
- Links: `<Link href="...">` from `next/link`
- Programmatic: `router.push("...")` from `next/navigation`

## Project Structure

```
src/
  app/
    page.tsx                # Login page (/)
    layout.tsx              # Root layout
    globals.css             # Design tokens (@theme inline)
    (chat)/
      layout.tsx            # App shell: <Sidebar> + <main>
      new/page.tsx          # Home + conversation (/new)
      recents/page.tsx      # Chat history (/recents)
      settings/page.tsx     # Settings 6 tabs (/settings)
  components/
    sidebar.tsx             # Collapsible sidebar
    chat-input.tsx          # Chat input component
```
