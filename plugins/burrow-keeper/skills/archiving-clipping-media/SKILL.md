---
name: archiving-clipping-media
description: Use when localizing external media (images, videos, audio) referenced by a note or clipping so they are archived as local assets.
---

# Archiving Clipping Media

## Overview

Download external images, videos, and audio referenced by a note into the workspace's local asset directory, replacing external URLs with local paths. Preserve offline access while following the workspace's existing asset and embed conventions.

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

**Skip:** existing local embeds/paths, text hyperlinks, already-local asset paths, `data:` URLs.

## Download Commands

**Images/direct files:**

```bash
curl -L --fail -o "{asset_dir}/{filename}" "{url}"
```

**YouTube/Vimeo:**

```bash
# Get the actual video title first for the filename
yt-dlp --get-title "{url}"
yt-dlp --merge-output-format mp4 -o "{asset_dir}/{filename}" "{url}"
```

Set `{asset_dir}` to the workspace-configured asset directory. If no asset directory exists, ask before creating one.

**CDN URLs** — try stripped URL first, fall back to original if it 404s:

- Strip known CDN transformation path segments when safe, such as `cdn-cgi/image/width=...,quality=...,format=.../`
- Strip query params like `?w=600&quality=80`
- If the stripped URL fails (404/403), retry with the original CDN URL

## Filename Convention

**Pattern:** `{source-slug}-{descriptive-name}.{ext}`

- **source-slug:** kebab-case, first few meaningful words of the note/source title
- **descriptive-name:** from the URL's last path segment or alt text
- **ext:** preserve original extension; use `.mp4` for yt-dlp downloads
- Check `{asset_dir}` for collisions before saving

Neutral examples: `source-title-hero.jpeg`, `source-title-diagram.png`, `source-title-demo.mp4`

## Replacement Format

Preserve the workspace's existing embed style. Default to standard Markdown with a relative path computed from the note file to the saved asset when no convention is obvious.

**Images** — preserve any alt text:

```markdown
![alt text]({relative_asset_path})
```

**HTML video tags** — preserve the workspace's video embed convention. If none exists, use HTML:

```markdown
<video controls src="{relative_asset_path}"></video>
```

**HTML audio tags** — preserve the workspace's audio embed convention. If none exists, use HTML:

```markdown
<audio controls src="{relative_asset_path}"></audio>
```

**YouTube embeds** — same pattern after yt-dlp download:

```markdown
![]({relative_asset_path})
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
| Forcing one embed style             | Preserve the workspace convention; default to Markdown relative paths |
| Downloading YouTube with curl       | Use `yt-dlp` for YouTube/Vimeo                                     |
| Keeping CDN params in URL           | Strip transformation params for full quality                       |
| Missing `<video>` or `<audio>` tags | Scan for markdown `![]()`, HTML `<video>`, AND `<audio>` tags      |
| Guessing YouTube video filename     | Run `yt-dlp --get-title` first, then derive slug from actual title |
| CDN-stripped URL 404s               | Try stripped URL first, fall back to original CDN URL              |
| Generic filenames                   | Prefix with source slug for namespacing                            |
