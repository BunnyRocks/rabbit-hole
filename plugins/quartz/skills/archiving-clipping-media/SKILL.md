---
name: archiving-clipping-media
description: Use when localizing external media (images, videos, audio) in a private clipping to archive them as local assets. Triggers when user wants to download, archive, or localize media from content/private/clippers/ files.
---

# Archiving Clipping Media

## Overview

Download external images, videos, and audio from a private clipping into `content/private/assets/`, replacing external URLs with local relative paths. Preserves content for offline studying without publishing third-party media.

## Workflow

1. Read the clipping file
2. Scan for all external media links (see Detection below)
3. For each link: download, save with proper filename, replace URL
4. Verify all downloads succeeded

## Media Detection

Scan for these patterns — handle ALL of them:

| Pattern                | Example                                                    |
| ---------------------- | ---------------------------------------------------------- |
| Markdown images        | `![alt](https://example.com/img.png)`                      |
| HTML video/source tags | `<video controls=""><source src="https://...mp4"></video>` |
| HTML audio tags        | `<audio src="https://...mp3"></audio>`                     |
| YouTube/Vimeo embeds   | `![](https://www.youtube.com/watch?v=...)`                 |

**Skip:** wikilinks (`![[...]]`), text hyperlinks, already-local paths (`../assets/...`), `data:` URLs.

## Download Commands

**Images/direct files:**

```bash
curl -L --fail -o "content/private/assets/{filename}" "{url}"
```

**YouTube/Vimeo:**

```bash
# Get the actual video title first for the filename
yt-dlp --get-title "{url}"
yt-dlp --merge-output-format mp4 -o "content/private/assets/{filename}" "{url}"
```

**CDN URLs** — try stripped URL first, fall back to original if it 404s:

- Economist: remove `cdn-cgi/image/width=...,quality=...,format=.../` prefix
- General: strip query params like `?w=600&quality=80`
- If the stripped URL fails (404/403), retry with the original CDN URL

## Filename Convention

**Pattern:** `{article-slug}-{descriptive-name}.{ext}`

- **article-slug:** kebab-case, first few meaningful words of the title
- **descriptive-name:** from the URL's last path segment or alt text
- **ext:** preserve original extension; use `.mp4` for yt-dlp downloads
- Check `content/private/assets/` for collisions before saving

Examples from existing assets: `ane-m4-hero.jpeg`, `ane-software-stack.png`, `rodney-terminal-demo.jpg`

## Replacement Format

**CRITICAL:** Use standard markdown with relative paths. Do NOT use Obsidian wikilink embeds.

**Images** — preserve any alt text:

```markdown
![alt text](../assets/article-slug-name.png)
```

**HTML video tags** — replace entire tag with markdown:

```markdown
![](../assets/article-slug-video.mp4)
```

**HTML audio tags** — replace entire tag with markdown:

```markdown
![](../assets/article-slug-audio.mp3)
```

**YouTube embeds** — same pattern after yt-dlp download:

```markdown
![](../assets/article-slug-video-title.mp4)
```

## Error Handling

- **404/failed download:** report and leave original link intact
- **Large files (>50MB):** report size, ask user before keeping
- **Duplicate URLs:** download once, replace all occurrences

## Post-Download

1. `ls -lh` each downloaded file to verify non-empty
2. Read modified clipping to confirm replacements
3. Report summary: downloaded count, failed count, total size

## Common Mistakes

| Mistake                             | Fix                                                                |
| ----------------------------------- | ------------------------------------------------------------------ |
| Using `![[wikilink]]` embeds        | Use `![](../assets/...)` relative paths                            |
| Downloading YouTube with curl       | Use `yt-dlp` for YouTube/Vimeo                                     |
| Keeping CDN params in URL           | Strip transformation params for full quality                       |
| Missing `<video>` or `<audio>` tags | Scan for markdown `![]()`, HTML `<video>`, AND `<audio>` tags      |
| Guessing YouTube video filename     | Run `yt-dlp --get-title` first, then derive slug from actual title |
| CDN-stripped URL 404s               | Try stripped URL first, fall back to original CDN URL              |
| Generic filenames                   | Prefix with article slug for namespacing                           |
