# Videos

> Source: https://nextjs.org/docs/app/guides/videos (v16.1.6)

How to use and optimize videos in Next.js applications.

## Embedding Methods

| Method | Use Case | Control Level |
|---|---|---|
| `<video>` tag | Self-hosted / direct files | Full (playback, appearance) |
| `<iframe>` tag | External platforms (YouTube, Vimeo) | Limited (platform controls) |

## Self-Hosted Video (`<video>`)

```tsx
export function Video() {
  return (
    <video width="320" height="240" controls preload="none">
      <source src="/path/to/video.mp4" type="video/mp4" />
      <track src="/path/to/captions.vtt" kind="subtitles" srcLang="en" label="English" />
      Your browser does not support the video tag.
    </video>
  )
}
```

### Common `<video>` Attributes

| Attribute | Description |
|---|---|
| `src` | Video file source |
| `width` / `height` | Player dimensions |
| `controls` | Show default playback controls |
| `autoPlay` | Auto-start (pair with `muted` + `playsInline`) |
| `loop` | Loop playback |
| `muted` | Mute audio (required for autoplay in most browsers) |
| `preload` | `none` / `metadata` / `auto` |
| `playsInline` | Inline playback on iOS (required for autoplay on iOS Safari) |

### Best Practices

- Include fallback text inside `<video>` for unsupported browsers
- Add subtitles/captions via `<track>` for accessibility
- Use standard HTML5 controls for keyboard/screen reader compatibility
- For advanced players: `react-player` or `video.js`

## External Video Embed (`<iframe>`)

```tsx
export default function Page() {
  return <iframe src="https://www.youtube.com/embed/19g66ezsKAg" allowFullScreen />
}
```

### Common `<iframe>` Attributes

| Attribute | Description |
|---|---|
| `src` | URL of embedded page |
| `width` / `height` | Iframe dimensions |
| `allowFullScreen` | Enable full-screen |
| `sandbox` | Extra content restrictions |
| `loading` | `lazy` for deferred loading |
| `title` | Accessible title |

## Streaming with Suspense

Use Server Components + React Suspense for external video embeds:

```tsx
// app/ui/video-component.tsx
export default async function VideoComponent() {
  const src = await getVideoSrc()
  return <iframe src={src} allowFullScreen />
}

// app/page.tsx
import { Suspense } from 'react'
import VideoComponent from '../ui/video-component'

export default function Page() {
  return (
    <Suspense fallback={<p>Loading video...</p>}>
      <VideoComponent />
    </Suspense>
  )
}
```

Use a skeleton component as fallback for better UX.

## Vercel Blob Hosting

```tsx
import { Suspense } from 'react'
import { list } from '@vercel/blob'

async function VideoComponent({ fileName }: { fileName: string }) {
  const { blobs } = await list({ prefix: fileName, limit: 1 })
  const { url } = blobs[0]
  return (
    <video controls preload="none" aria-label="Video player">
      <source src={url} type="video/mp4" />
    </video>
  )
}

export default function Page() {
  return (
    <Suspense fallback={<p>Loading video...</p>}>
      <VideoComponent fileName="my-video.mp4" />
    </Suspense>
  )
}
```

## Third-Party Integrations

| Platform | Key Feature |
|---|---|
| `next-video` | `<Video>` component; works with Vercel Blob, S3, Mux |
| Cloudinary | `<CldVideoPlayer>` with adaptive bitrate |
| Mux | Video API + starter template for Next.js |
| Fastly | VOD and streaming media |
| ImageKit | `<IKVideo>` component |

## Quick Reference

| Task | Approach |
|---|---|
| Self-hosted video | `<video>` tag with `<source>` and `<track>` |
| YouTube/Vimeo embed | `<iframe>` with `loading="lazy"` |
| Non-blocking load | Wrap in `<Suspense>` with fallback |
| Autoplay | `autoPlay muted playsInline` (all three) |
| Accessibility | `<track>` for captions, `controls` attribute, `aria-label` |
| Cloud hosting | Vercel Blob, Cloudinary, Mux, or S3 |
| Responsive embed | CSS to make iframe/video adapt to screen size |
