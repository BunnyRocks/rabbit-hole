---
name: reviewing-notes
description: Use when reviewing existing notes against source material, identifying gaps, drilling into topics via discussion, and reorganizing notes according to the workspace's structure. Also use when user wants to break up a monolithic note into topic-based files.
---

# Reviewing and Organizing Notes

## Overview

Review existing notes against source material, discuss and annotate topics, then reorganize into topic files that match the workspace's structure. Complements studying-articles (which starts from new source notes); this skill starts from **existing notes** that need refinement.

## Workflow

```dot
digraph review_flow {
  "Read source + existing notes" -> "Gap analysis";
  "Gap analysis" -> "User picks topics";
  "User picks topics" -> "Discuss and annotate";
  "Discuss and annotate" -> "More topics?" [label="add callouts"];
  "More topics?" -> "User picks topics" [label="yes"];
  "More topics?" -> "Reorganize into sections" [label="done"];
  "Reorganize into sections" -> "User requests topic split?";
  "User requests topic split?" -> "Split into topic files" [label="yes"];
  "User requests topic split?" -> "Done" [label="no"];
  "Split into topic files" -> "Delete or slim original";
}
```

## Phase 1: Gap Analysis

1. Read the source material (transcript, article, clipping)
2. Read the existing notes
3. Present a comparison:
   - **Well-captured:** topics the notes already cover well
   - **Missing:** rich material from the source not yet in the notes
4. Let the user decide which gaps to explore

**Do NOT** add content without user direction. Present options and let them choose.

## Phase 2: Discuss and Annotate

Use the workspace's existing annotation convention. In Obsidian-style workspaces, use callouts:

| Type          | Use for                 |
| ------------- | ----------------------- |
| `[!question]` | Q&A about concepts      |
| `[!example]`  | Concrete examples       |
| `[!info]`     | Supplementary context   |
| `[!warning]`  | Misconceptions, gotchas |

**Rules:**

- Place annotations contextually after relevant content, not grouped at end
- One concept per annotation, self-contained
- Use the workspace's highlight syntax for key takeaways; otherwise use bold or bullet points
- No tables inside callouts when using Obsidian callouts
- Match the language the user is writing in

If the workspace does not support callouts, use plain Markdown headings, blockquotes, or bullet sections.

## Phase 3: Reorganize into Sections

When the user is done drilling into topics:

1. Identify natural topic groupings across all content (quotes + commentary)
2. Propose section headers — present to user before applying
3. Move content into sections, keeping quotes with their commentary
4. Content that doesn't fit neatly into one section stays closest to its primary topic

**Naming sections:** Use the user's language and framing. If notes are in Chinese, headers should be in Chinese (with English term in parentheses if helpful).

## Phase 4: Topic Split

When the user requests breaking into separate notes:

1. **Propose file mapping** — show a table of: topic → proposed file path → rationale
2. **Wait for user confirmation** before creating files
3. **Placement guide:** Use the workspace's existing folder taxonomy. If it uses PARA, map projects, areas, resources, and archive accordingly. If it uses another structure, follow that structure. If none is obvious, propose destination paths and ask the user to confirm.
4. **Each new file gets:**
   - Metadata inherited from the original note when the workspace uses metadata
   - AI disclosure in the workspace's normal format if required by user or publishing policy
   - Source link to the original article/podcast
   - Only the content relevant to its topic
5. **Handle the original note** per user preference:
   - Delete it (if fully split)
   - Slim it to an index linking to the new topic notes
   - Keep as-is (if split was partial)

**Before deleting the original**, confirm with the user.

## Common Mistakes

| Mistake                                        | Fix                                                                                              |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Adding content without user direction          | Present gaps, let user choose what to explore                                                    |
| Reorganizing before discussion is done         | Complete annotation phase first                                                                  |
| Creating files without showing the plan        | Always propose file mapping and wait for confirmation                                            |
| Forcing content into a taxonomy when user didn't ask | Reorganizing into sections and splitting into topic files are separate steps              |
| Mixing languages inconsistently                | Match the user's language in commentary and headers                                              |
| Forgetting AI disclosure policy                | Follow the workspace's AI disclosure convention when notes are substantially AI-assisted         |
