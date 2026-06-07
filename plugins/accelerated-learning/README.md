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

This plugin collects study and knowledge-work workflows for turning source material into durable notes, flashcards, annotations, and practice artifacts. It covers Anki card generation and `.apkg` inspection, structured course-material study, Chinese translation, academic-paper and article reading, note drafting and review, and interview preparation for coding and system design challenges. Its skills emphasize source-grounded understanding, concise retrieval practice, workspace-native annotation formats, local organization conventions, and follow-up artifacts such as retrospectives and Anki cards.

## Skills

### creating-anki-cards

Use when creating Anki flashcards from any learning material — course slides, PDFs, books, documentation, articles, or assignments. Use when user mentions Anki, flashcards, spaced repetition, or studying.

### drafting-notes

Use when the user wants to create a new note in a note workspace — short write-ups, tips, how-tos, or original content. Also use when user says "create a note about...", "write up...", or "I want to jot down...".

### extracting-apkg

Use when needing to read, extract, inspect, or convert Anki .apkg deck files — triggered by .apkg file paths, "Anki deck", "flashcard export", or requests to view card content

### reading-papers

Use when studying academic papers from a note workspace or source document, discussing them through Keshav's three-pass framework with LLM assistance, and adding study annotations. Also use when organizing paper notes into topic files.

### reviewing-notes

Use when reviewing existing notes against source material, identifying gaps, drilling into topics via discussion, and reorganizing notes according to the workspace's structure. Also use when user wants to break up a monolithic note into topic-based files.

### studying-articles

Use when studying blog posts, articles, clippings, or saved source notes in a note workspace — user asks questions, discusses ideas, and wants annotations added or extracted.

### studying-coding-challenges

Use when studying coding interview problems in a note workspace — user wants to practice a challenge via mock interview, study existing solutions, or annotate a coding problem note.

### studying-course-materials

Use when studying course materials (PDF slides, markdown notes, or website links) without access to lectures. Use when user provides course material and wants structured notes, interactive Q&A on the content, or Obsidian callouts from discussion.

### studying-system-design-challenges

Use when studying system design interview problems in a note workspace — user wants to run a mock system design interview, study a reference design, or annotate a system design question note.

### translate-to-chinese

Use when translate a document into Chinese

## Info

- **Author:** BunnyRocks
- **License:** MIT
- **Keywords:** learning, anki, flashcards, translation, course, papers, articles, interviews, coding, system-design, study, notes, obsidian
<!--[[[end]]]-->
