---
name: archiving-youtube
description: Use when downloading or archiving YouTube videos/playlists with yt-dlp, constructing output templates, selecting formats, or troubleshooting yt-dlp commands
---

# Archiving YouTube with yt-dlp

Reference for yt-dlp commands, output templates, and archiving workflows. **Output template syntax is the primary hallucination zone** — always consult this reference rather than guessing.

## Output Template Syntax

The `-o` flag accepts Python-style format strings: `%(FIELD)[flags][width][.precision][length]TYPE`

### Conversion Types

| Type | Meaning | `#` flag | `+` flag |
|------|---------|----------|----------|
| `s` | String | — | — |
| `d` | Integer | — | — |
| `B` | Bytes (truncates to precision bytes) | — | — |
| `S` | Sanitize as filename | Restricted sanitize | — |
| `j` | JSON | Pretty-print | Unicode |
| `h` | HTML escaped | — | — |
| `l` | Comma-separated list | Newline-separated | — |
| `q` | Terminal-quoted string | Split list to args | — |
| `D` | Decimal suffixes (10M) | Use 1024 factor | — |
| `U` | Unicode NFC normalize | NFD | NFKC/NFKD |

**WARNING:** `l` is comma-separated list, NOT lowercase. `S` is filename sanitization, NOT truncation-with-ellipsis. There is no `R` or `L` conversion type.

### Formatting Operations

```
%(title).100s              # Truncate to 100 characters
%(title).100B              # Truncate to 100 bytes
%(title)+.100U             # NFKC normalize, 100 char precision
%(playlist_index)03d       # Zero-pad integer to 3 digits
%(playlist_index+10)03d    # Arithmetic: add 10, then zero-pad
%(n_entries+1-playlist_index)d  # Arithmetic expression

%(upload_date>%Y-%m-%d)s   # Date formatting via strftime
%(duration>%H-%M-%S)s      # Duration formatting

%(release_date>%Y,upload_date>%Y|Unknown)s  # Alternatives with ','
%(uploader|Unknown)s       # Default value with '|'
%(chapters&has chapters|no chapters)s       # Replacement with '&'

%(tags.0)s                 # Object traversal with '.'
%(subtitles.en.-1.ext)s    # Nested traversal
%(formats.:.format_id)s    # Slice all, get field
%(id.3:7)s                 # String slicing
```

### Output Template Types

Prefix with type and colon to control auxiliary file naming:

`subtitle:`, `thumbnail:`, `description:`, `infojson:`, `link:`, `chapter:`, `pl_thumbnail:`, `pl_description:`, `pl_infojson:`, `pl_video:`

```bash
-o "%(title)s.%(ext)s" -o "thumbnail:%(title)s/%(title)s.%(ext)s"
```

### Playlist Template Variables

| Variable | Description |
|----------|-------------|
| `playlist` | Playlist title, falls back to ID |
| `playlist_id` | Playlist identifier |
| `playlist_title` | Playlist title |
| `playlist_count` | Total items in playlist |
| `playlist_index` | Video position in playlist (zero-padded) |
| `playlist_autonumber` | Position in download queue (zero-padded) |
| `n_entries` | Total *extracted* items (may differ from `playlist_count`) |

**NOTE:** `playlist_uploader` and `playlist_uploader_id` do NOT exist as template variables.

### Common Video Template Variables

| Variable | Description |
|----------|-------------|
| `id` | Video identifier |
| `title` | Video title |
| `ext` | Filename extension |
| `channel` | Channel name |
| `channel_id` | Channel ID |
| `uploader` | Uploader name |
| `upload_date` | Upload date (YYYYMMDD) |
| `release_date` | Release date (YYYYMMDD) |
| `duration` | Length in seconds |
| `duration_string` | Length as HH:mm:ss |
| `view_count` | View count |
| `like_count` | Like count |
| `description` | Video description |
| `age_limit` | Age restriction in years |
| `autonumber` | Incremental counter (padded to 5) |

## Common Command Patterns

### Archive a Playlist

```bash
yt-dlp \
  -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b" \
  --merge-output-format mp4 \
  -o "%(playlist_title)s/%(playlist_index)03d - %(title).150B [%(id)s].%(ext)s" \
  --download-archive archive.txt \
  --cookies-from-browser brave \
  --write-subs --write-auto-subs --sub-langs "en.*,ja.*" --embed-subs \
  --embed-metadata --embed-thumbnail \
  --sleep-interval 3 --max-sleep-interval 10 \
  "https://www.youtube.com/playlist?list=PLXXXXXXX"
```

### Key Flags Quick Reference

| Flag | Purpose |
|------|---------|
| `-f FORMAT` | Format selection (see below) |
| `--merge-output-format mp4` | Force merged output to mp4 |
| `-o TEMPLATE` | Output filename template |
| `-P DIR` | Output directory path |
| `--download-archive FILE` | Skip already-downloaded (stores `youtube VIDEO_ID`) |
| `--cookies-from-browser BROWSER[:PROFILE]` | Use browser cookies (brave, chrome, firefox, etc.) |
| `--cookies FILE` | Use Netscape-format cookie file |
| `--write-subs` | Download manual subtitles |
| `--write-auto-subs` | Download auto-generated subtitles |
| `--sub-langs LANGS` | Subtitle languages (`en.*,ja.*`, or `all`) |
| `--embed-subs` | Embed subtitles in video file |
| `--embed-metadata` | Embed metadata tags |
| `--embed-thumbnail` | Embed thumbnail as cover art |
| `--write-info-json` | Save metadata as .info.json |
| `--write-thumbnail` | Save thumbnail as separate file |
| `--sleep-interval N` | Min seconds between downloads |
| `--max-sleep-interval N` | Max seconds (random between min-max) |
| `--sleep-requests N` | Seconds between HTTP requests |
| `-r RATE` | Bandwidth throttle (e.g., `5M`) |
| `--no-overwrites` | Don't overwrite existing files |
| `--output-na-placeholder TEXT` | Replace unavailable fields (default: `NA`) |
| `-I ITEM_SPEC` | Playlist range: `5:15` (items 5-15), `::2` (every 2nd), `::-1` (reverse) |
| `-t mp4` | Preset: mp4 with h264+aac, sensible defaults |
| `-t sleep` | Preset: conservative sleep intervals |

### Format Selection

```bash
# Modern syntax (preferred)
-f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b"

# Legacy syntax (still works)
-f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

# bv* = best video (may include audio)
# ba  = best audio only
# b   = best single file
# Filters: [ext=mp4], [height<=720], [vcodec^=avc]
```

### Presets (yt-dlp 2025+)

```bash
-t mp4    # --merge-output-format mp4 --remux-video mp4 -S vcodec:h264,...
-t aac    # Best AAC audio, extract
-t mp3    # Best MP3 audio, extract
-t mkv    # Merge to MKV
-t sleep  # --sleep-subtitles 5 --sleep-requests 0.75 --sleep-interval 10 --max-sleep-interval 20
```

Presets expand to flags, so they combine freely: `-t mp4 -t sleep` works.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `%(playlist_uploader)s` | Does not exist; use `%(channel)s` or `%(uploader)s` |
| Thinking `l` type = lowercase | `l` = comma-separated list |
| Thinking `S` type = truncation | `S` = filename sanitization |
| Using `R` or `L` conversion types | These don't exist |
| Confusing `playlist_count` and `n_entries` | `playlist_count` = total items; `n_entries` = total *extracted* |
| Forgetting `--merge-output-format mp4` | Without it, merged output may be .mkv |
| Not escaping `?` in playlist URLs | Quote the URL or escape: `\?` |

## macOS Notes

- Chrome/Brave cookie extraction may need Keychain access; Firefox is more reliable
- Thumbnail embedding in mp4 needs ffmpeg (preferred) or AtomicParsley
