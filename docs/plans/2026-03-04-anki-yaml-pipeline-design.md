# Anki YAML Card Pipeline — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace Python-script-based Anki card generation with YAML data files and a self-contained import script with deduplication.

**Architecture:** Cards are stored as YAML files (one per source) in project repos. A standalone `import_cards.py` script bundled with the skill parses YAML, deduplicates against the Anki collection, and imports. The SKILL.md is updated so Claude generates YAML instead of Python scripts.

**Tech Stack:** Python, PyYAML, fastanki (wraps anki Collection API), uv inline script metadata

---

## Design

### YAML Card Format

```yaml
deck: "CIS 1902::Python"
source: lecture_1_basics
tags: [cis1902, lecture1, python-basics]

cards:
  - q: "What is Python's null value?"
    a: "<code>None</code> — type is <code>NoneType</code>"
    tags: [types]
  - q: "{} creates a dict or a set?"
    a: "A <b>dict</b>. Use <code>set()</code> for empty sets."
    tags: [sets, gotcha]
```

- File-level `tags` merged with per-card `tags`
- `q`/`a` keys for token efficiency
- HTML formatting in answers (same as current)
- One file per source material

### Import Script Usage

```bash
uv run import_cards.py anki/*.yaml              # preview
uv run import_cards.py anki/*.yaml --add        # import to Anki (deduplicates)
uv run import_cards.py anki/*.yaml --tsv        # export TSV
```

### Deduplication (--add mode)

- Opens the Anki collection via `Collection.open(profile)`
- Loads all existing notes in the target deck via `col.find_notes(f"deck:{deck}")`
- Builds a set of existing question texts (the `Front` field)
- Skips cards whose question already exists
- Reports skipped duplicates to stdout

---

## Task 1: Create `import_cards.py` — YAML parsing and preview

**Files:**
- Create: `plugins/accelerated-learning/skills/creating-anki-cards/import_cards.py`

**Step 1: Create the script with YAML parsing and preview mode**

The script uses inline `uv` script metadata for dependencies. Preview is the default mode (no flags).

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Import Anki flashcards from YAML files.

Usage:
    uv run import_cards.py anki/*.yaml              # preview cards
    uv run import_cards.py anki/*.yaml --tsv        # export TSV
    uv run import_cards.py anki/*.yaml --add        # add to Anki (deduplicates)
"""

import argparse
import csv
import sys
from pathlib import Path

import yaml


def load_cards(paths):
    """Load cards from YAML files, merging file-level and card-level tags."""
    cards = []
    for path in paths:
        with open(path) as f:
            data = yaml.safe_load(f)
        deck = data["deck"]
        base_tags = data.get("tags", [])
        for card in data["cards"]:
            tags = base_tags + card.get("tags", [])
            cards.append({"q": card["q"], "a": card["a"], "tags": tags, "deck": deck})
    return cards


def preview(cards):
    """Print cards to stdout for review."""
    for i, c in enumerate(cards, 1):
        print(f"--- Card {i} [{c['deck']}] ---")
        print(f"Q: {c['q']}")
        print(f"A: {c['a']}")
        print(f"Tags: {', '.join(c['tags'])}")
        print()
    print(f"Total: {len(cards)} cards")


def export_tsv(cards, output=sys.stdout):
    """Export cards as TSV (question, answer, tags)."""
    writer = csv.writer(output, delimiter="\t")
    for c in cards:
        writer.writerow([c["q"], c["a"], " ".join(c["tags"])])


def main():
    parser = argparse.ArgumentParser(description="Import Anki cards from YAML")
    parser.add_argument("files", nargs="+", type=Path, help="YAML card files")
    parser.add_argument("--tsv", action="store_true", help="Export as TSV")
    parser.add_argument("--add", action="store_true", help="Add to Anki (must be closed)")
    parser.add_argument("--profile", default="User 1", help="Anki profile name")
    args = parser.parse_args()

    cards = load_cards(args.files)

    if args.tsv:
        export_tsv(cards)
    elif args.add:
        add_to_anki(cards, args.profile)
    else:
        preview(cards)


if __name__ == "__main__":
    main()
```

**Step 2: Test preview manually with a sample YAML file**

Create a temporary test file and run:
```bash
cat > /tmp/test_cards.yaml << 'EOF'
deck: "Test::Deck"
source: test
tags: [test, sample]

cards:
  - q: "What is 1+1?"
    a: "<code>2</code>"
    tags: [math]
  - q: "What color is the sky?"
    a: "Blue"
EOF

uv run plugins/accelerated-learning/skills/creating-anki-cards/import_cards.py /tmp/test_cards.yaml
```

Expected output: 2 cards printed with merged tags `[test, sample, math]` and `[test, sample]`.

**Step 3: Test TSV export**

```bash
uv run plugins/accelerated-learning/skills/creating-anki-cards/import_cards.py /tmp/test_cards.yaml --tsv
```

Expected: tab-separated output with 2 rows.

**Step 4: Commit**

```bash
git add plugins/accelerated-learning/skills/creating-anki-cards/import_cards.py
git commit -m "feat: add import_cards.py with YAML parsing, preview, and TSV export"
```

---

## Task 2: Add Anki import with deduplication

**Files:**
- Modify: `plugins/accelerated-learning/skills/creating-anki-cards/import_cards.py`

**Step 1: Add the `add_to_anki` function**

Add this function before `main()` and update the inline script dependencies to include `fastanki`:

Update the script metadata block:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml", "fastanki"]
# ///
```

Add the import and function:
```python
def add_to_anki(cards, profile="User 1"):
    """Add cards to Anki, skipping duplicates based on question text."""
    from anki.collection import Collection
    from fastanki.core import data_path
    import anki._backend

    # Suppress latency warnings
    anki._backend.main_thread = lambda: None

    path = data_path() / profile / "collection.anki2"
    if not path.exists():
        print(f"Error: Anki profile '{profile}' not found at {path}", file=sys.stderr)
        sys.exit(1)

    if not hasattr(Collection, '_backend'):
        Collection._backend = anki._backend.RustBackend()
    try:
        Collection._backend.close_collection(downgrade_to_schema11=False)
    except Exception:
        pass
    col = Collection(str(path), backend=Collection._backend)

    try:
        # Collect existing questions across all target decks
        decks_seen = set()
        existing_questions = set()
        for c in cards:
            if c["deck"] not in decks_seen:
                decks_seen.add(c["deck"])
                note_ids = col.find_notes(f'deck:"{c["deck"]}"')
                for nid in note_ids:
                    note = col.get_note(nid)
                    existing_questions.add(note["Front"])

        added = 0
        skipped = 0
        for c in cards:
            if c["q"] in existing_questions:
                print(f"  SKIP (duplicate): {c['q'][:60]}")
                skipped += 1
                continue

            col.add_deck(c["deck"])
            note = col.new_note(col.models.by_name("Basic"))
            note["Front"] = c["q"]
            note["Back"] = c["a"]
            note.tags = c["tags"]
            col.add_note(note, col.decks.id_for_name(c["deck"]))
            existing_questions.add(c["q"])
            added += 1

        col.save()
        print(f"\nAdded: {added}, Skipped (duplicates): {skipped}")
    finally:
        col.close()
```

**Step 2: Test with --add against a real Anki profile (Anki must be closed)**

```bash
uv run plugins/accelerated-learning/skills/creating-anki-cards/import_cards.py /tmp/test_cards.yaml --add
```

Expected: Cards added to Anki. Running again should show all cards skipped as duplicates.

**Step 3: Commit**

```bash
git add plugins/accelerated-learning/skills/creating-anki-cards/import_cards.py
git commit -m "feat: add Anki import with deduplication to import_cards.py"
```

---

## Task 3: Update SKILL.md for YAML workflow

**Files:**
- Modify: `plugins/accelerated-learning/skills/creating-anki-cards/SKILL.md`

**Step 1: Rewrite the Workflow, Project Setup, and Running sections**

Replace the workflow diagram to reflect YAML generation instead of Python script creation. The key changes:

1. **Workflow** — "Create YAML card file" replaces "Create new card script". Preview uses `import_cards.py`. No more `anki_generator.py` check.

2. **Project Setup** section becomes simpler:
   - First time: create `anki/` directory in the project
   - Subsequent: add new YAML files to `anki/`
   - No Python scaffolding, no `pyproject.toml`, no `uv add`

3. **Running** section references `import_cards.py`:
   ```bash
   uv run <path-to-skill>/import_cards.py anki/*.yaml          # preview
   uv run <path-to-skill>/import_cards.py anki/*.yaml --tsv    # export TSV
   uv run <path-to-skill>/import_cards.py anki/*.yaml --add    # add to Anki (must be CLOSED, deduplicates)
   ```

4. **YAML format** section replaces Python `Card()` examples with YAML examples:
   ```yaml
   deck: "CIS 1902::Python"
   source: lecture_1_basics
   tags: [cis1902, lecture1, python-basics]

   cards:
     - q: "What is Python's null value?"
       a: "<code>None</code> — type is <code>NoneType</code>"
       tags: [types]
   ```

5. **Atomicity example** — update from Python `Card()` syntax to YAML:
   ```yaml
   # BAD: Code dump as answer
   - q: "Implement BSTree __contains__ iteratively."
     a: "<pre>def __contains__(self, element):..."

   # GOOD: Tests the key insight
   - q: "BSTree <code>__contains__</code>: where should <code>return False</code> go?"
     a: "<b>After</b> the while loop, not inside it."
     tags: [bstree, gotcha]
   ```

6. **Add deduplication note** — mention that `--add` automatically skips cards already in Anki, so retrying is safe.

7. **Add instruction** for Claude to check existing YAML files in `anki/` before generating new ones to avoid file-level duplication.

8. **Common Mistakes** table — update "Forgetting `make_tags()` helper" to "Missing file-level tags" and remove Python-specific entries.

**Key content to preserve unchanged:**
- Foundational Principles section (atomic cards, selective redundancy, test the tricky part)
- Card Patterns section (two-way cards, cloze deletions, hierarchies)
- Question Design section
- Answer Formatting section
- Extracting from Source Materials section (course slides, assignments, books targets)
- Common Mistakes table (update Python-specific entries only)

**Step 2: Commit**

```bash
git add plugins/accelerated-learning/skills/creating-anki-cards/SKILL.md
git commit -m "refactor: update SKILL.md for YAML card workflow"
```

---

## Task 4: Clean up old artifacts

**Files:**
- Delete: `plugins/accelerated-learning/skills/creating-anki-cards/__pycache__/` (contains stale `anki_generator.cpython-313.pyc`)

**Step 1: Remove the stale pycache**

```bash
rm -rf plugins/accelerated-learning/skills/creating-anki-cards/__pycache__
```

**Step 2: Add `__pycache__` to `.gitignore` if not already present**

Check if `__pycache__` is in `.gitignore`. If not, add it.

**Step 3: Commit**

```bash
git add -u plugins/accelerated-learning/skills/creating-anki-cards/__pycache__
git commit -m "chore: remove stale anki_generator pycache"
```

---

## Task 5: Convert existing cis1902 card scripts to YAML (validation)

**Files:**
- Create: `/Users/ziyunli/codebase/cis1902/anki/lecture_1_basics.yaml`
- Create: `/Users/ziyunli/codebase/cis1902/anki/lecture_2_pythonic.yaml`

This task validates the full pipeline by converting the existing Python card scripts to YAML format and testing preview, TSV export, and import.

**Step 1: Convert `lecture_1_basics.py` to YAML format**

Translate all `Card(q, a, make_tags(...))` calls to YAML entries. File-level tags are `[cis1902, lecture1, python-basics]`, per-card tags are the extra args from `make_tags()`.

**Step 2: Convert `lecture_2_pythonic.py` to YAML format**

Same process with tags `[cis1902, lecture2, pythonic-programming]`.

**Step 3: Test preview**

```bash
uv run /Users/ziyunli/codebase/rabbit-hole/plugins/accelerated-learning/skills/creating-anki-cards/import_cards.py anki/*.yaml
```

Expected: All cards from both files printed with correct merged tags.

**Step 4: Test dedup against existing Anki cards**

```bash
uv run /Users/ziyunli/codebase/rabbit-hole/plugins/accelerated-learning/skills/creating-anki-cards/import_cards.py anki/*.yaml --add
```

Expected: All cards skipped as duplicates (since they were already imported via the old Python scripts).

**Step 5: Commit in cis1902 repo**

```bash
cd /Users/ziyunli/codebase/cis1902
git add anki/
git commit -m "feat: convert Anki card scripts to YAML format"
```
