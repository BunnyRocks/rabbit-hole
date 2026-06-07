---
name: extracting-apkg
description: Use when needing to read, extract, inspect, or convert Anki .apkg deck files — triggered by .apkg file paths, "Anki deck", "flashcard export", or requests to view card content
---

# Extracting Anki .apkg Content

## Overview

An `.apkg` file is a **ZIP archive** containing a SQLite database and optional media. This skill extracts card content efficiently in ~3 tool calls instead of iterative discovery.

## File Format

```
.apkg (ZIP)
├── collection.anki2    # SQLite database (cards, notes, metadata)
└── media               # JSON map: {"0": "image.jpg", ...} or {}
```

**Key tables:**

- `col` — collection metadata; `models` JSON has field names, `decks` JSON has deck names
- `notes` — card content in `flds` column, fields separated by `\x1f` (ASCII unit separator)
- `cards` — links notes to decks with scheduling data

## Extraction Steps

### 1. Unzip + Extract in One Shot

Use this Python script — handles unzip, SQLite query, HTML stripping, and metadata extraction in a single tool call:

```python
import sqlite3, html, re, json, tempfile, zipfile, sys, os

apkg_path = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) > 2 else None

with tempfile.TemporaryDirectory() as tmpdir:
    with zipfile.ZipFile(apkg_path, 'r') as z:
        z.extractall(tmpdir)

    db_name = 'collection.anki21' if os.path.exists(os.path.join(tmpdir, 'collection.anki21')) else 'collection.anki2'
    conn = sqlite3.connect(os.path.join(tmpdir, db_name))

    # Get deck name and field names from metadata
    col = conn.execute('SELECT models, decks FROM col').fetchone()
    models = json.loads(col[0])
    decks = json.loads(col[1])
    deck_name = next((d['name'] for d in decks.values() if d['name'] != 'Default'), 'Unknown')
    # Build model lookup: model_id -> field names
    models_by_id = {mid: [f['name'] for f in m['flds']] for mid, m in models.items()}

    # Extract notes with their model IDs
    rows = conn.execute('SELECT mid, flds FROM notes').fetchall()
    conn.close()

    # Check for media
    media_path = os.path.join(tmpdir, 'media')
    has_media = False
    if os.path.exists(media_path):
        with open(media_path) as f:
            media_map = json.loads(f.read())
            has_media = bool(media_map)

def strip_html(text):
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<div[^>]*>', '\n', text)
    text = re.sub(r'</div>', '', text)
    text = re.sub(r'<p[^>]*>', '\n', text)
    text = re.sub(r'</p>', '', text)
    text = re.sub(r'<li[^>]*>', '\n- ', text)
    text = re.sub(r'</li>', '', text)
    text = re.sub(r'<h[1-6][^>]*>', '\n', text)
    text = re.sub(r'</h[1-6]>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    lines = [' '.join(l.split()) for l in text.split('\n')]
    return '\n'.join(l for l in lines if l.strip())

output = []
output.append(f'Deck: {deck_name}')
output.append(f'Cards: {len(rows)}')
if has_media:
    output.append(f'Media files: {len(media_map)}')
output.append('')

for i, (mid, flds) in enumerate(rows, 1):
    parts = flds.split('\x1f')
    field_names = models_by_id.get(str(mid), ['Front', 'Back'])
    output.append('=' * 60)
    output.append(f'Card {i}')
    output.append('=' * 60)
    for j, name in enumerate(field_names):
        content = strip_html(parts[j]) if j < len(parts) else '(empty)'
        output.append(f'[{name}]')
        output.append(content)
        output.append('')

result = '\n'.join(output)
if output_path:
    with open(output_path, 'w') as f:
        f.write(result)
    print(f'Saved {len(rows)} cards to {output_path}')
else:
    print(result)
```

### 2. Run It

```bash
# Print to stdout
python3 extract_apkg.py "/path/to/deck.apkg"

# Save to file
python3 extract_apkg.py "/path/to/deck.apkg" "/path/to/output.txt"
```

You can also run the script inline via `python3 -c "..."` with the apkg path hardcoded — no temp file needed.

## Edge Cases

- **`collection.anki21` vs `collection.anki2`**: Newer Anki versions use `.anki21`. Script checks both.
- **Media files**: The `media` JSON maps numeric keys to filenames. Media files are stored in the ZIP with numeric names (e.g., `0`, `1`). If media exists, note it in output and offer to extract.
- **Multiple models**: Some decks mix card types (Basic, Cloze, etc.). Each model has different field names. For multi-model decks, group output by model.
- **Cloze deletions**: Content may contain `{{c1::answer::hint}}` syntax. Preserve as-is in extraction — the user can decide how to render.
- **HTML content**: Cards from web clippers or Jupyter notebooks often contain heavy HTML. The `strip_html` function handles `<br>`, `<div>`, and nested tags. For cards with images, note `[image: filename]` placeholders.

## Common Mistakes

| Mistake                         | Fix                                                                 |
| ------------------------------- | ------------------------------------------------------------------- |
| Using `\n` as field separator   | Fields use `\x1f` (unit separator), not newline                     |
| Forgetting HTML in card content | Always strip HTML — even "plain" cards have `<br>` tags             |
| Ignoring `collection.anki21`    | Check for both `.anki2` and `.anki21` variants                      |
| Not reading `col.models`        | Field names come from models metadata, not hardcoded "Front"/"Back" |
