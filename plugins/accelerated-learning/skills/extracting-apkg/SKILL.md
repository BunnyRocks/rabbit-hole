---
name: extracting-apkg
description: Use when needing to read, extract, or inspect Anki .apkg deck files — triggered by .apkg file paths, "Anki deck", "flashcard export", or requests to view card content
---

# Extracting Anki .apkg Content

## Overview

An `.apkg` file is a **ZIP archive** containing a SQLite database and optional media. This skill extracts card content efficiently in ~3 tool calls instead of iterative discovery.

## File Format

```
.apkg (ZIP)
├── collection.anki21   # SQLite database in newer exports, when present
├── collection.anki2    # SQLite database in older exports, when present
└── media               # JSON map: {"0": "image.jpg", ...} or {}
```

**Key tables:**

- `col` — collection metadata; legacy `models` JSON has field names, legacy `decks` JSON has deck names
- `notes` — card content in `flds` column, fields separated by `\x1f` (ASCII unit separator)
- `cards` — links notes to decks with scheduling data

## Extraction Steps

### 1. Unzip + Extract in One Shot

Use this Python script — handles unzip, SQLite query, HTML stripping, and metadata extraction in a single tool call:

```python
import sqlite3, html, re, json, tempfile, zipfile, sys, os

if len(sys.argv) < 2:
    print('Usage: python3 extract_apkg.py /path/to/deck.apkg [output.txt]', file=sys.stderr)
    sys.exit(2)

apkg_path = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) > 2 else None

def find_collection_db(tmpdir):
    for db_name in ('collection.anki21', 'collection.anki2'):
        db_path = os.path.join(tmpdir, db_name)
        if os.path.exists(db_path):
            return db_name, db_path
    raise RuntimeError('No collection.anki21 or collection.anki2 found in .apkg')

def load_required_json(value, label):
    data = json.loads(value or '{}')
    if not data:
        raise RuntimeError(
            f'Unsupported Anki schema: col.{label} is empty. '
            'This quick extractor supports legacy .apkg metadata stored in col.models/col.decks. '
            'Modern exports may store this data in separate tables; re-export with legacy support or extend the script for that schema.'
        )
    return data

with tempfile.TemporaryDirectory() as tmpdir:
    with zipfile.ZipFile(apkg_path, 'r') as z:
        z.extractall(tmpdir)

    db_name, db_path = find_collection_db(tmpdir)
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)

    # Get deck name and field names from metadata
    col = conn.execute('SELECT models, decks FROM col').fetchone()
    if not col:
        raise RuntimeError('Collection metadata row not found in col table')
    models = load_required_json(col[0], 'models')
    decks = load_required_json(col[1], 'decks')
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
    field_names = models_by_id.get(str(mid))
    if not field_names:
        raise RuntimeError(f'Missing field metadata for note model {mid}')
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

- **`collection.anki21` vs `collection.anki2`**: Newer Anki versions may use `.anki21`. Script checks both filenames.
- **Modern schema exports**: Some `.anki21` exports store note type and deck metadata outside `col.models` / `col.decks`. This quick extractor detects that case and fails loudly instead of labeling every card as `Front` / `Back`.
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
| Assuming every `.anki21` has legacy metadata | Fail loudly when `col.models` / `col.decks` are empty instead of guessing field names |
| Not reading `col.models`        | Field names come from models metadata, not hardcoded "Front"/"Back" |
