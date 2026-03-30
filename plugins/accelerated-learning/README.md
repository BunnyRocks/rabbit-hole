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
# accelerated-learning

Skills for accelerated learning

**Creating Anki Cards** is a plugin that generates high-quality, atomic flashcards from any learning material—course slides, PDFs, books, documentation, articles, or assignments—organized as YAML files for seamless import into Anki. It identifies card-worthy concepts, focuses on tricky points, and builds interconnected retrieval paths by supporting two-way cards, cloze deletions, and hierarchy-based questions. The plugin enforces best practices: concise cards, selective redundancy, robust tagging, and avoidance of content duplication, ensuring cards are honest to grade and easy to review. Integration tools preview, export, and deduplicate card imports into Anki, making the process efficient and reliable for spaced repetition study.

**Studying Course Materials** parses course content (PDF slides, markdown notes, or website links) into structured markdown notes and enriches them with simulated lecture-style interactive Q&A. Users can request clarification or ask questions about material, with answers formatted as Obsidian callouts—question, example, info, or warning—contextually placed for later review or easy conversion to Anki cards. The plugin supports hierarchical note structuring, provides supplementary context, and helps users bridge gaps left by passive reading, yielding narrative notes ideal for both studying and card extraction.

**Translate to Chinese** is a document translation plugin for converting any Markdown text into fluent, readable Chinese while meticulously preserving original meaning, technical terms, and structure. It cleans up formatting issues (like footnotes and line breaks), performs a complete, word-for-word translation, and adds technical terms in both languages for clarity. All frontmatter fields are retained, "Translations" is added to tags, and the plugin appends the translated filename (in Chinese with kebab-case) to the source folder. A link back to the original document and an editing attribution footnote are included for provenance and traceability.

## Skills

### creating-anki-cards

Use when creating Anki flashcards from any learning material — course slides, PDFs, books, documentation, articles, or assignments. Use when user mentions Anki, flashcards, spaced repetition, or studying.

### studying-course-materials

Use when studying course materials (PDF slides, markdown notes, or website links) without access to lectures. Use when user provides course material and wants structured notes, interactive Q&A on the content, or Obsidian callouts from discussion.

### translate-to-chinese

Use when translate a document into Chinese

## Info

- **Author:** BunnyRocks
- **License:** MIT
- **Keywords:** learning, anki, flashcards, translation, course, study, notes, obsidian
<!--[[[end]]]-->
