# Third-Party Libraries (@next/third-parties)

> Source: https://nextjs.org/docs/app/guides/third-party-libraries (v16.1.6)

`@next/third-parties` provides optimized components for popular third-party services. Currently **experimental**.

## Installation

```bash
pnpm add @next/third-parties@latest next@latest
```

## Google Tag Manager

```tsx
// app/layout.tsx (all routes)
import { GoogleTagManager } from '@next/third-parties/google'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <GoogleTagManager gtmId="GTM-XYZ" />
      <body>{children}</body>
    </html>
  )
}
```

**Send events:**
```tsx
'use client'
import { sendGTMEvent } from '@next/third-parties/google'

<button onClick={() => sendGTMEvent({ event: 'buttonClicked', value: 'xyz' })}>Click</button>
```

| Prop | Type | Description |
|---|---|---|
| `gtmId` | Required* | GTM container ID (`GTM-...`) |
| `gtmScriptUrl` | Optional* | Custom GTM script URL |
| `dataLayer` | Optional | Initial data layer object |
| `dataLayerName` | Optional | Data layer name (default: `dataLayer`) |
| `auth` | Optional | `gtm_auth` for environment snippets |
| `preview` | Optional | `gtm_preview` for environment snippets |

*`gtmId` can be omitted when `gtmScriptUrl` is provided.

## Google Analytics

```tsx
// app/layout.tsx
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
      <GoogleAnalytics gaId="G-XYZ" />
    </html>
  )
}
```

**Send events:**
```tsx
'use client'
import { sendGAEvent } from '@next/third-parties/google'

<button onClick={() => sendGAEvent('event', 'buttonClicked', { value: 'xyz' })}>Click</button>
```

| Prop | Type | Description |
|---|---|---|
| `gaId` | Required | Measurement ID (`G-...`) |
| `dataLayerName` | Optional | Data layer name (default: `dataLayer`) |
| `nonce` | Optional | CSP nonce |

Pageviews are tracked automatically via browser history changes. Enable "Enhanced Measurement" in GA Admin.

## Google Maps Embed

```tsx
import { GoogleMapsEmbed } from '@next/third-parties/google'

<GoogleMapsEmbed apiKey="XYZ" height={200} width="100%" mode="place" q="Brooklyn+Bridge,New+York,NY" />
```

| Prop | Type | Description |
|---|---|---|
| `apiKey` | Required | Google Maps API key |
| `mode` | Required | Map mode (`place`, `view`, `directions`, `streetview`, `search`) |
| `height` / `width` | Optional | Dimensions (default: `auto`) |
| `q` | Optional | Marker location (required for some modes) |
| `center` / `zoom` / `maptype` | Optional | Map view settings |
| `loading` | Optional | Default: `lazy` |
| `language` / `region` | Optional | Localization |

## YouTube Embed

Uses `lite-youtube-embed` for fast loading.

```tsx
import { YouTubeEmbed } from '@next/third-parties/google'

<YouTubeEmbed videoid="ogfYd705cRs" height={400} params="controls=0" />
```

| Prop | Type | Description |
|---|---|---|
| `videoid` | Required | YouTube video ID |
| `width` / `height` | Optional | Container dimensions (default: `auto`) |
| `playlabel` | Optional | Accessible play button label |
| `params` | Optional | Player params as query string (e.g., `"controls=0&start=10"`) |
| `style` | Optional | Container styles |

## Quick Reference

| Component | Import | Key Prop |
|---|---|---|
| `GoogleTagManager` | `@next/third-parties/google` | `gtmId="GTM-..."` |
| `GoogleAnalytics` | `@next/third-parties/google` | `gaId="G-..."` |
| `GoogleMapsEmbed` | `@next/third-parties/google` | `apiKey`, `mode` |
| `YouTubeEmbed` | `@next/third-parties/google` | `videoid` |
| `sendGTMEvent` | `@next/third-parties/google` | `{ event, value }` |
| `sendGAEvent` | `@next/third-parties/google` | `('event', name, params)` |
