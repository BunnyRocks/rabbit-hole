# rabbit-hole

A plugin marketplace for AI coding assistants.

Supports Claude Code, Codex, and OpenCode.

## Installation

### Claude Code

```shell
/plugin marketplace add BunnyRocks/rabbit-hole
/plugin install accelerated-learning@rabbit-hole
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
Fetch and follow instructions from https://raw.githubusercontent.com/BunnyRocks/rabbit-hole/refs/heads/main/.codex/INSTALL.md
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

**Creating Anki Cards** is a plugin that generates high-quality, atomic flashcards from any learning material—course slides, PDFs, books, documentation, articles, or assignments—organized as YAML files for seamless import into Anki. It identifies card-worthy concepts, focuses on tricky points, and builds interconnected retrieval paths by supporting two-way cards, cloze deletions, and hierarchy-based questions. The plugin enforces best practices: concise cards, selective redundancy, robust tagging, and avoidance of content duplication, ensuring cards are honest to grade and easy to review. Integration tools preview, export, and deduplicate card imports into Anki, making the process efficient and reliable for spaced repetition study.

**Studying Course Materials** parses course content (PDF slides, markdown notes, or website links) into structured markdown notes and enriches them with simulated lecture-style interactive Q&A. Users can request clarification or ask questions about material, with answers formatted as Obsidian callouts—question, example, info, or warning—contextually placed for later review or easy conversion to Anki cards. The plugin supports hierarchical note structuring, provides supplementary context, and helps users bridge gaps left by passive reading, yielding narrative notes ideal for both studying and card extraction.

**Translate to Chinese** is a document translation plugin for converting any Markdown text into fluent, readable Chinese while meticulously preserving original meaning, technical terms, and structure. It cleans up formatting issues (like footnotes and line breaks), performs a complete, word-for-word translation, and adds technical terms in both languages for clarity. All frontmatter fields are retained, "Translations" is added to tags, and the plugin appends the translated filename (in Chinese with kebab-case) to the source folder. A link back to the original document and an editing attribution footnote are included for provenance and traceability.

| Skill | Description |
| ----- | ----------- |
| `creating-anki-cards` | Use when creating Anki flashcards from any learning material — course slides, PDFs, books, documentation, articles, or assignments. Use when user mentions Anki, flashcards, spaced repetition, or studying. |
| `studying-course-materials` | Use when studying course materials (PDF slides, markdown notes, or website links) without access to lectures. Use when user provides course material and wants structured notes, interactive Q&A on the content, or Obsidian callouts from discussion. |
| `translate-to-chinese` | Use when translate a document into Chinese |

### [burrow-keeper](https://github.com/BunnyRocks/rabbit-hole/tree/main/plugins/burrow-keeper#readme)

This plugin provides comprehensive guidance for archiving YouTube videos and playlists using yt-dlp, focusing on constructing accurate output templates and selecting optimal download formats. It covers key yt-dlp command patterns, template syntax, variable usage, common flags, and error-prone areas specific to output template construction and playlist handling. Designed as a troubleshooting and reference tool, the plugin helps users avoid common mistakes, supports advanced filename logic, playlist variable handling, and format selection, and provides concise examples for practical archiving workflows. Its main strengths are precise output template documentation, format selection guidance, and detailed flag explanations for efficient YouTube archiving.

| Skill | Description |
| ----- | ----------- |
| `archiving-youtube` | Use when downloading or archiving YouTube videos/playlists with yt-dlp, constructing output templates, selecting formats, or troubleshooting yt-dlp commands |

<!--[[[end]]]-->

## Contributing

Add new skills under `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` and register the plugin in `.claude-plugin/marketplace.json`.

## License

MIT
