# rabbit-hole

A plugin marketplace for AI coding assistants.

Supports Claude Code, Codex, and OpenCode.

## Installation

### Claude Code

```shell
/plugin marketplace add BunnyRocks/rabbit-hole
/plugin install accelerated-learning@rabbit-hole
/plugin install burrow-keeper@rabbit-hole
```

### Codex

Tell Codex:

```
Fetch and follow instructions from https://raw.githubusercontent.com/BunnyRocks/rabbit-hole/refs/heads/main/.codex/INSTALL.md
```

**Detailed docs:** [.codex/INSTALL.md](.codex/INSTALL.md).

### OpenCode

Tell OpenCode:

```
Fetch and follow instructions from https://raw.githubusercontent.com/BunnyRocks/rabbit-hole/refs/heads/main/.opencode/INSTALL.md
```

**Detailed docs:** [.opencode/INSTALL.md](.opencode/INSTALL.md).



<!--[[[cog
import readme_gen

marketplace = readme_gen.load_marketplace()
repo_url = readme_gen.github_repo_url()

print(f"## Plugins ({len(marketplace['plugins'])} available)\n")

for plugin in marketplace["plugins"]:
    name = plugin["name"]
    plugin_dir = f"plugins/{name}"
    meta = readme_gen.load_plugin_meta(plugin_dir)
    skills = readme_gen.discover_skills(plugin_dir)
    summary = readme_gen.get_or_create_summary(plugin_dir)

    print(f"### [{name}]({repo_url}/tree/main/{plugin_dir}#readme)\n")
    print(f"{summary}\n")
    print("| Skill | Description |")
    print("| ----- | ----------- |")
    for skill in skills:
        print(f"| `{skill['name']}` | {skill['description']} |")
    print()
]]]-->
## Plugins (2 available)

### [accelerated-learning](https://github.com/BunnyRocks/rabbit-hole/tree/main/plugins/accelerated-learning#readme)

This plugin collects study and knowledge-work workflows for turning source material into durable notes, flashcards, annotations, and practice artifacts. It covers Anki card generation and `.apkg` inspection, structured course-material study, Chinese translation, academic-paper and article reading, note drafting and review, and interview preparation for coding and system design challenges. Its skills emphasize source-grounded understanding, concise retrieval practice, workspace-native annotation formats, local organization conventions, and follow-up artifacts such as retrospectives and Anki cards.

| Skill | Description |
| ----- | ----------- |
| `creating-anki-cards` | Use when creating Anki flashcards from any learning material — course slides, PDFs, books, documentation, articles, or assignments. Use when user mentions Anki, flashcards, spaced repetition, or studying. |
| `drafting-notes` | Use when the user wants to create a new note in a note workspace — short write-ups, tips, how-tos, or original content. Also use when user says "create a note about...", "write up...", or "I want to jot down...". |
| `extracting-apkg` | Use when needing to read, extract, inspect, or convert Anki .apkg deck files — triggered by .apkg file paths, "Anki deck", "flashcard export", or requests to view card content |
| `reading-papers` | Use when studying academic papers from a note workspace or source document, discussing them through Keshav's three-pass framework with LLM assistance, and adding study annotations. Also use when organizing paper notes into topic files. |
| `reviewing-notes` | Use when reviewing existing notes against source material, identifying gaps, drilling into topics via discussion, and reorganizing notes according to the workspace's structure. Also use when user wants to break up a monolithic note into topic-based files. |
| `studying-articles` | Use when studying blog posts, articles, clippings, or saved source notes in a note workspace — user asks questions, discusses ideas, and wants annotations added or extracted. |
| `studying-coding-challenges` | Use when studying coding interview problems in a note workspace — user wants to practice a challenge via mock interview, study existing solutions, or annotate a coding problem note. |
| `studying-course-materials` | Use when studying course materials (PDF slides, markdown notes, or website links) without access to lectures. Use when user provides course material and wants structured notes, interactive Q&A on the content, or Obsidian callouts from discussion. |
| `studying-system-design-challenges` | Use when studying system design interview problems in a note workspace — user wants to run a mock system design interview, study a reference design, or annotate a system design question note. |
| `translate-to-chinese` | Use when translate a document into Chinese |

### [burrow-keeper](https://github.com/BunnyRocks/rabbit-hole/tree/main/plugins/burrow-keeper#readme)

This plugin collects practical maintenance workflows for digital artifacts that benefit from precise command or format reconstruction. It provides yt-dlp guidance for archiving YouTube videos and playlists, localizes external media from notes or clippings into local assets, and supports converting rendered SVG flowcharts or Mermaid-like diagram exports back into pasteable Mermaid source. Its main strengths are compact references for error-prone syntax, asset-preserving archive workflows, and repeatable maintenance tasks where guessing creates broken output.

| Skill | Description |
| ----- | ----------- |
| `archiving-clipping-media` | Use when localizing external media (images, videos, audio) referenced by a note or clipping so they are archived as local assets. |
| `archiving-youtube` | Use when downloading or archiving YouTube videos/playlists with yt-dlp, constructing output templates, selecting formats, or troubleshooting yt-dlp commands |
| `converting-svg-to-mermaid` | Use when converting SVG flowcharts, diagram exports, or rendered Mermaid-like graphics back into Mermaid source code |

<!--[[[end]]]-->

## Contributing

Add new skills under `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` and register the plugin in `.claude-plugin/marketplace.json`.

## License

MIT
