# Anki YAML Card Pipeline

## Problem

The creating-anki-cards skill generates Python scripts that depend on `anki_generator` via hardcoded local paths. Cards exist only as code, not as reviewable data. Failed/retried generation creates duplicates in Anki.

## Solution

Separate card **data** (YAML, checked into project repos) from card **import** (a standalone script bundled with the skill).

## Architecture

```
Project repo (e.g., cis1902/)          rabbit-hole plugin
anki/                                  skills/creating-anki-cards/
  lecture_1_basics.yaml                  SKILL.md
  lecture_2_pythonic.yaml                import_cards.py
```

## YAML Card Format

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

## Import Script (`import_cards.py`)

Standalone Python file with inline `uv` script metadata. Lives at `plugins/accelerated-learning/skills/creating-anki-cards/import_cards.py`.

Dependencies: `fastanki`, `pyyaml`.

### Usage

```bash
uv run /path/to/import_cards.py anki/*.yaml              # preview
uv run /path/to/import_cards.py anki/*.yaml --add         # import to Anki
uv run /path/to/import_cards.py anki/*.yaml --tsv         # export TSV
```

### Deduplication (--add mode)

- Opens the Anki collection
- Queries existing notes' question fields
- Skips cards whose question already exists
- Reports skipped duplicates to stdout

## SKILL.md Changes

- Claude generates YAML files instead of Python scripts
- References `import_cards.py` by skill-relative path
- Adds instruction to check existing YAML files in `anki/` before generating
- Same card quality guidelines (atomicity, patterns, extraction rules)

## Not Changing

- Card quality principles, patterns, and extraction guidelines
- HTML formatting conventions
- `fastanki` as the underlying Anki integration
