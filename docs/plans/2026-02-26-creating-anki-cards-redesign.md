# Creating Anki Cards Skill Redesign

## Motivation

Incorporate principles from [Effective Spaced Repetition](https://borretti.me/article/effective-spaced-repetition) into the creating-anki-cards skill. The current skill is course-material-focused and discourages redundancy. The blog makes a strong case for selective redundancy (two-way cards, multiple formulations) and introduces structured card patterns (cloze deletions, hierarchies) that the current skill lacks.

## Design Decisions

- **Selective redundancy**: Two-way cards and multiple formulations are encouraged, but card count guardrails remain to keep review sustainable.
- **Broadened scope**: Principles apply to any learning material (books, docs, articles), not just course slides/assignments.
- **Key patterns only**: Two-way cards, cloze deletions, and hierarchies. Concept graphs and exhaustive sequence patterns are omitted (too abstract for a skill doc).
- **Tooling**: fastanki remains the primary toolchain. Card design principles are stated independently of tooling.
- **Full restructure**: Principles-first information architecture rather than patching the existing course-focused structure.

## Structure

```
1. Metadata (name, broadened description)
2. Overview (reframed around core principles)
3. When to Use (broadened triggers)
4. Workflow (unchanged diagram)
5. Foundational Principles (NEW)
   - Atomic cards
   - Selective redundancy
   - Test the tricky part
6. Card Patterns (NEW)
   - Two-way cards
   - Cloze deletions
   - Hierarchies
7. Question Design (updated: +multiple formulations, +cache insights)
8. Answer Formatting (unchanged)
9. Extraction Guidelines (expanded)
   - From Course Slides (20-35 cards)
   - From Assignments (10-20 cards)
   - From Books/Docs/Articles (NEW, 10-25 cards)
10. Project Setup (unchanged)
11. Common Mistakes (updated table)
```

## Section Details

### 1. Metadata

```yaml
name: creating-anki-cards
description: Use when creating Anki flashcards from any learning material — course slides, PDFs, books, documentation, articles, or assignments. Use when user mentions Anki, flashcards, spaced repetition, or studying.
```

### 2. Overview

Generate high-quality Anki flashcards from learning materials using fastanki. Core principle: **create atomic, interconnected cards that test concepts from multiple angles.** Good cards are small, honest to grade, and build a web of retrieval paths — not isolated facts.

### 3. When to Use

- User wants flashcards from any learning material (slides, docs, books, articles)
- User completed an assignment and wants cards for tricky spots
- User mentions Anki, spaced repetition, or studying

### 4. Workflow

Unchanged from current skill.

### 5. Foundational Principles

1. **Atomic cards** — Each card tests exactly one concept. The answer should be scannable in 5 seconds. If a card needs partial credit to grade, it's too big — split it.
2. **Selective redundancy** — Create two-way cards and multiple formulations of important concepts to build multiple retrieval paths. Stay within card count targets per source type (see Extraction Guidelines).
3. **Test the tricky part** — Focus on gotchas, surprising behaviors, and easy-to-confuse pairs. Skip obvious definitions unless the definition itself is counterintuitive.

### 6. Card Patterns

**Two-Way Cards**: For any term/concept pair, create cards in both directions. Forward: "What does X mean?" / Backward: "What term describes Y?" Not every card needs a reverse — use for terminology, notation, and definitions.

**Cloze Deletions**: Hide a key part of a statement and ask the learner to fill it in. Useful for formulas, syntax patterns, sequences, and key phrases in definitions. Works well with atomicity.

**Hierarchies**: For category/member relationships, ask both directions. Prefer bottom-up cards ("What category does Y belong to?"). If a top-down card lists more than 3-4 items, split it or use cloze deletions.

### 7. Question Design

- Ask about the tricky part, not the obvious part
- Use code in the question when testing syntax recall
- Frame as "what happens when..." for gotcha cards
- Ask the same concept multiple ways — formal definition, informal intuition, code example, "what's the difference between X and Y?"
- Avoid "list N things" — split into separate cards, or use cloze deletions
- Cache your insights — if reading sparks an inference beyond what's stated, verify it and make a card
- Definition test: "Would someone who read this once already know this?" If yes, skip it.

### 8. Answer Formatting

Unchanged from current skill.

### 9. Extraction Guidelines

**From Course Slides** (20-35 cards per lecture): Read slides, check for overlap with existing scripts, focus on code examples with non-obvious behavior, comparisons, gotchas. For PDFs with annotations, prioritize highlighted passages.

**From Assignments** (10-20 cards): Focus on tricky implementation spots. What would someone get wrong? What's the non-obvious constraint? What's the edge case?

**From Books / Documentation / Articles** (10-25 cards per chapter/section): Prioritize counterintuitive facts, precise technical distinctions, common pitfalls. Use two-way cards for terminology. Use cloze for formulas and sequences. Cache insights. Skip background context and content you already know.

### 10. Project Setup

Unchanged from current skill.

### 11. Common Mistakes

| Mistake | Fix |
|---------|-----|
| Cards with 10+ line code answers | Split into concept cards; test the insight, not the implementation |
| "What is X?" for every topic | Only create definition cards when the definition is surprising |
| Pasting full solutions | Isolate the gotcha — what would someone get wrong? |
| Only single-direction cards for terminology | Add reverse cards for important terms and notation |
| Missing cloze cards for sequences/formulas | Use cloze deletions when testing ordered or fill-in-the-blank knowledge |
| Duplicating earlier material | Check existing card scripts before creating new ones |
| Missing tags | Always tag by topic for filtered study sessions |
| 40+ cards for one source | Be more selective — focus on gotchas, use card count targets |

## What Changed from Current Skill

- **Added**: Foundational Principles section, Card Patterns section (two-way, cloze, hierarchies), books/docs/articles extraction guidelines
- **Removed**: "Merge overlapping cards" anti-pattern (conflicts with selective redundancy)
- **Updated**: Overview (reframed), description (broadened), question design (+multiple formulations, +cache insights), common mistakes table (new rows for two-way and cloze anti-patterns)
- **Unchanged**: Workflow diagram, answer formatting, project setup, code examples
