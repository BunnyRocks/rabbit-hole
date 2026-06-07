<!--[[[cog
import readme_gen

plugin_dir = readme_gen.this_plugin_dir(cog.inFile)
meta = readme_gen.load_plugin_meta(plugin_dir)
skills = readme_gen.discover_skills(plugin_dir)
summary = readme_gen.get_or_create_summary(plugin_dir)

print(f"# {meta['name']}\n")
print(f"{meta['description']}\n")
print(f"{summary}\n")
print("## Skills\n")
for skill in skills:
    print(f"### {skill['name']}\n")
    print(f"{skill['description']}\n")

print("## Info\n")
print(f"- **Author:** {meta['author']['name']}")
print(f"- **License:** {meta['license']}")
if meta.get('keywords'):
    print(f"- **Keywords:** {', '.join(meta['keywords'])}")
]]]-->
# quartz

Skills for Obsidian and Quartz knowledge workflows

This plugin collects Obsidian and Quartz vault workflows for turning reading, interview practice, clippings, and original notes into durable knowledge artifacts. It supports drafting notes in the user's voice, studying articles and academic papers with callout annotations, reviewing and reorganizing notes into PARA structures, and practicing coding or system design challenges with retrospectives and Anki follow-up. It also includes practical vault maintenance workflows for extracting Anki `.apkg` decks and localizing media from private clippings into local assets.

## Skills

### archiving-clipping-media

Use when localizing external media (images, videos, audio) in a private clipping to archive them as local assets. Triggers when user wants to download, archive, or localize media from content/private/clippers/ files.

### drafting-notes

Use when the user wants to create a new note in the Obsidian vault — short write-ups, tips, how-tos, or any original content. Also use when user says "create a note about...", "write up...", or "I want to jot down...".

### extracting-apkg

Use when needing to read, extract, inspect, or convert Anki .apkg deck files — triggered by .apkg file paths, "Anki deck", "flashcard export", or requests to view card content

### reading-papers

Use when studying academic papers in the Obsidian vault — user reads a converted markdown paper under private/papers/, discusses it through Keshav's three-pass framework with LLM assistance, and wants annotations added as callouts. Also use when organizing paper notes into PARA topic files.

### reviewing-notes

Use when reviewing existing notes against their source material, identifying gaps, drilling into topics via discussion, and reorganizing notes into PARA model structure. Also use when user wants to break up a monolithic note into topic-based files.

### studying-articles

Use when studying blog posts, articles, or clippings in the Obsidian vault — user asks questions, discusses ideas, and wants annotations added as callouts. Also use when publishing private clipping discussions as public blogmarks.

### studying-coding-challenges

Use when studying coding interview problems in the Obsidian vault — user wants to practice a challenge via mock interview, study existing solutions, or annotate a coding problem note with learning callouts.

### studying-system-design-challenges

Use when studying system design interview problems in the Obsidian vault — user wants to run a mock system design interview, study a reference design, or annotate a system design question note with learning callouts.

## Info

- **Author:** BunnyRocks
- **License:** MIT
- **Keywords:** quartz, obsidian, notes, papers, articles, clippings, anki, study, interviews, media
<!--[[[end]]]-->
