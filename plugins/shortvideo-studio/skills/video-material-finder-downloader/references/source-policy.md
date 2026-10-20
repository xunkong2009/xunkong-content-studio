# Source and rights policy

## Source priority

1. Stock footage with explicit download and reuse terms for generic B-roll.
2. Openly licensed or public-domain material whose individual item page documents the license.
3. Original uploads from official institutions, universities, conferences, companies, media organizations, eyewitnesses, or named creators.
4. UGC for which the original creator granted direct written permission without a fee.
5. Ordinary uploads and reposts only when provenance and reuse permission are clear.

## Content exclusion

- Exclude third-party reviews, product evaluations, taste tests, unboxings, reactions, commentary channels, street-interview opinions, influencer recommendations, and similar opinion-led footage.
- Do not treat reviewer ownership of a video as sufficient relevance for a script asset.
- If an excluded video is the only result for a named product, use official footage, free licensed generic stock, or an existing generated visual instead.

## Rights labels

Assign one primary label to every candidate:

- `free-stock-license`: The free item license covers the intended edited video use.
- `open-license`: The individual item has a reusable license; preserve required attribution.
- `public-domain-claimed`: The item page claims public-domain status; record source and jurisdiction caveats.
- `official-original-rights-unclear`: The official or original source is verified, but republication permission is not established.
- `creator-permission-required`: Contact the original recorder before reuse; keep only no-fee written permission candidates.
- `repost-avoid`: Ownership or provenance is unclear; do not download as a deliverable.

There is no universal safe number of seconds. A 3–15 second edit recommendation controls package size and editorial usefulness, not copyright permission.

## Delivery status

- `automatic-download`: Public, supported source plus confirmed user entitlement; download and verify during the task.
- `official-download`: Use the source site's visible download control or documented media endpoint.
- `manual-login`: The user must sign in to a free platform. Keep the exact public post and do not request passwords.
- `link-only-awaiting-free-permission`: Retain the original source and creator contact; do not download for editing until no-fee written permission is confirmed.

## Required manifest fields

- `source_url`
- `source_platform`
- `title`
- `uploader` when available
- `script_beat`
- `suggested_range`
- `downloaded_range`
- `local_file`
- `rights_note`
- `subtitle_overlay_note`
- `source_class`
- `delivery_status`
- `downloaded_at`

## Platform notes

- **YouTube:** A watch page is not proof of reuse permission. Do not return extracted CDN URLs. Download only when the user is entitled to do so. Label news, broadcast, and third-party creator footage separately.
- **Bilibili:** Retain the canonical `/video/BV...` page and uploader. Treat “未经作者授权，禁止转载” and similar labels as a strong no-reuse signal. Do not assume that a public player permits downloading or republication.
- **Weibo:** Retain the exact post or video page and account name. Distinguish an original post from a repost or clipped news segment. A visible public post is not proof of reuse permission.
- **Douyin:** Retain the expanded public post, account, and original/repost assessment. Watermarks, public playback, and share links do not grant republication rights.
- **Xiaohongshu:** Retain the exact note and author. Treat seeding posts, reposts, visible brand placements, music, faces, and private locations as additional rights signals.
- **X:** Retain the exact status and author; distinguish attached original media from quoted or embedded media. Public visibility is not permission.
- **TikTok:** Retain the original post and creator. Record watermark, caption, music, and whether the post is a repost or duet/stitch using third-party media.
- **Reddit:** Retain the exact post, uploader, and credited recorder. A Reddit upload or cross-post does not prove the uploader owns the footage.
- **Pexels:** Retain the video detail page and current license terms. Prefer the visible original download control or its verified `/download/video/<id>/` route.
- **Pixabay:** Retain the media detail page and current license information. Do not redistribute an unmodified asset as a standalone product.
- **Mixkit:** Retain the clip detail page and check whether that clip uses the Free License or Restricted License.

## Official and archival source notes

- **Official media centers:** A press download can still carry use restrictions. Preserve the terms and do not infer unrestricted reuse from an official source.
- **Wikimedia Commons, Internet Archive, Prelinger:** Check the individual item's license and attribution; do not generalize one collection item's status to the whole repository.

## Paid-source exclusion

- Do not search or shortlist paid news archives, paid UGC libraries, paid stock libraries, subscription libraries, paid asset packs, or creator permissions that require a fee.
- If a free search result redirects to a paid license or subscription, discard it and continue with a free official, open-license, public-domain, or generated alternative.

## Subtitle language

“No subtitles” means do not request separate or automatic subtitle tracks. It cannot remove text or subtitles burned into video pixels. Screen likely overlays before download when the user explicitly requires clean footage.

## Failure handling

- If a stock site blocks automated download or requires an interactive quality choice, return the verified detail page and mark manual download required; use a visible browser download control when available.
- If a public-platform extractor fails, confirm that the page remains public and that the installed `yt-dlp` lists a matching extractor before updating from its official channel or changing supported arguments.
- Never invent unsupported extractor flags or bypass access controls.
