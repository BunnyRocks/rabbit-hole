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


def add_to_anki(cards, profile="User 1"):
    """Add cards to Anki with deduplication. (Not yet implemented.)"""
    print("Error: --add not yet implemented", file=sys.stderr)
    sys.exit(1)


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
