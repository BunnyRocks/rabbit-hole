# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml", "fastanki"]
# ///
"""Import Anki flashcards from YAML files.

Usage:
    uv run import_cards.py anki/*.yaml              # preview cards
    uv run import_cards.py anki/*.yaml --tsv        # export TSV
    uv run import_cards.py anki/*.yaml --add        # add to Anki (deduplicates)
"""

import argparse
import csv
import os
import platform
import sys
from pathlib import Path

import yaml


def load_cards(paths):
    """Load cards from YAML files, merging file-level and card-level tags."""
    cards = []
    for path in paths:
        with open(path) as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            print(f"Error: {path} is empty or not a valid YAML mapping", file=sys.stderr)
            sys.exit(1)
        for key in ("deck", "cards"):
            if key not in data:
                print(f"Error: {path} is missing required key '{key}'", file=sys.stderr)
                sys.exit(1)
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


def _anki_data_path():
    """Return the default Anki data folder for this OS."""
    syst = platform.system()
    if syst == "Windows":
        return Path(os.environ["APPDATA"]) / "Anki2"
    elif syst == "Linux":
        return Path.home() / ".local" / "share" / "Anki2"
    else:  # macOS
        return Path.home() / "Library" / "Application Support" / "Anki2"


def add_to_anki(cards, profile="User 1"):
    """Add cards to Anki, skipping duplicates based on question text."""
    import anki._backend
    from anki.collection import Collection

    # Suppress latency warnings
    anki._backend.main_thread = lambda: None

    col_path = _anki_data_path() / profile / "collection.anki2"
    if not col_path.exists():
        print(f"Error: Anki profile '{profile}' not found at {col_path}", file=sys.stderr)
        sys.exit(1)

    if not hasattr(Collection, '_backend'):
        Collection._backend = anki._backend.RustBackend()
    try:
        Collection._backend.close_collection(downgrade_to_schema11=False)
    except Exception:
        pass
    col = Collection(str(col_path), backend=Collection._backend)

    try:
        # Collect existing questions across all target decks
        decks_seen = set()
        existing_questions = set()
        for c in cards:
            if c["deck"] not in decks_seen:
                decks_seen.add(c["deck"])
                col.add_deck(c["deck"])
                note_ids = col.find_notes(f'deck:"{c["deck"]}"')
                for nid in note_ids:
                    note = col.get_note(nid)
                    existing_questions.add(note["Front"])

        model = col.models.by_name("Basic")
        if model is None:
            print("Error: 'Basic' note type not found in Anki", file=sys.stderr)
            sys.exit(1)

        added = 0
        skipped = 0
        for c in cards:
            if c["q"] in existing_questions:
                print(f"  SKIP (duplicate): {c['q'][:60]}")
                skipped += 1
                continue

            note = col.new_note(model)
            note["Front"] = c["q"]
            note["Back"] = c["a"]
            note.tags = c["tags"]
            deck_id = col.decks.id_for_name(c["deck"])
            col.add_note(note, deck_id)
            existing_questions.add(c["q"])
            added += 1

        col.save()
        print(f"\nAdded: {added}, Skipped (duplicates): {skipped}")
    finally:
        col.close()


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
