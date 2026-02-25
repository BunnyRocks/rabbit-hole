# rabbit-hole Marketplace Design

## Purpose

A Claude Code plugin marketplace for sharing skills across machines and AI coding assistant providers. Hosted at `github.com/BunnyRocks/rabbit-hole`.

## Goals

1. Package existing learning skills into a distributable Claude Code plugin marketplace
2. Support Claude Code, Codex, and OpenCode from day one
3. Enable easy sharing across machines via git clone + marketplace install

## Repository Structure

```
rabbit-hole/
├── .claude-plugin/
│   └── marketplace.json
├── .codex/
│   └── INSTALL.md
├── .opencode/
│   ├── INSTALL.md
│   └── plugins/
│       └── rabbit-hole.js
├── plugins/
│   └── accelerated-learning/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           ├── creating-anki-cards/
│           │   └── SKILL.md
│           └── translate-to-chinese/
│               └── SKILL.md
├── lib/
│   └── skills-core.js
├── LICENSE
└── README.md
```

Plugin-per-directory layout using `pluginRoot: "./plugins"` in the marketplace manifest. Each plugin is self-contained, ready for additional plugins in the future.

## Marketplace Manifest

```json
{
  "name": "rabbit-hole",
  "owner": {
    "name": "BunnyRocks"
  },
  "metadata": {
    "description": "Skills for going deeper down the rabbit hole",
    "version": "0.1.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "accelerated-learning",
      "source": "accelerated-learning",
      "description": "Skills for accelerated learning — Anki cards, translation, research",
      "version": "0.1.0",
      "keywords": ["learning", "anki", "flashcards", "translation"],
      "category": "education"
    }
  ]
}
```

## Plugin: accelerated-learning

### Skills

- **creating-anki-cards** — Generate Anki flashcards from course materials (slides, PDFs, lecture notes) using fastanki
- **translate-to-chinese** — Translate documents into Chinese with proper technical term handling

### plugin.json

```json
{
  "name": "accelerated-learning",
  "description": "Skills for accelerated learning",
  "version": "0.1.0"
}
```

Skills are auto-discovered from the `skills/` directory. No hooks or session bootstrap needed — these are on-demand skills, not ambient context.

## Multi-Provider Support

### Claude Code

Standard plugin marketplace integration:

```shell
/plugin marketplace add BunnyRocks/rabbit-hole
/plugin install accelerated-learning@rabbit-hole
```

Skills auto-discovered via directory structure.

### Codex

Codex natively reads SKILL.md files. Integration is symlink-based (no adapter code):

```bash
git clone https://github.com/BunnyRocks/rabbit-hole.git ~/.codex/rabbit-hole
mkdir -p ~/.agents/skills
ln -s ~/.codex/rabbit-hole/plugins/accelerated-learning/skills ~/.agents/skills/accelerated-learning
```

### OpenCode

OpenCode requires a JS plugin (`.opencode/plugins/rabbit-hole.js`) that:

1. Exports an async plugin function via OpenCode's plugin API
2. Uses `experimental.chat.system.transform` to inject skill discovery context
3. Appends tool mapping table (Claude Code tool names to OpenCode equivalents)

```bash
git clone https://github.com/BunnyRocks/rabbit-hole.git ~/.config/opencode/rabbit-hole
ln -s ~/.config/opencode/rabbit-hole/.opencode/plugins/rabbit-hole.js ~/.config/opencode/plugins/rabbit-hole.js
ln -s ~/.config/opencode/rabbit-hole/plugins/accelerated-learning/skills ~/.config/opencode/skills/accelerated-learning
```

### Shared Utility: lib/skills-core.js

ES module providing:
- `extractFrontmatter(filePath)` — parse YAML frontmatter
- `findSkillsInDir(dir)` — recursive SKILL.md discovery
- `stripFrontmatter(content)` — body without YAML header

Used by the OpenCode plugin for runtime skill discovery.

## Scope

### v0.1.0 (In Scope)

- Marketplace manifest with `accelerated-learning` plugin
- Two skills: `creating-anki-cards`, `translate-to-chinese`
- Claude Code plugin.json + auto-discovery
- Codex INSTALL.md with symlink instructions
- OpenCode JS plugin + INSTALL.md
- `lib/skills-core.js`
- README.md with per-provider usage instructions

### Future

- Gemini / Pi provider support
- `comprehensive-research` skill
- Additional plugins
- CI/CD pipeline

## Testing

- **Claude Code:** Install from local path, verify skills show up and are invocable
- **Codex:** Follow INSTALL.md, verify skills appear in Codex
- **OpenCode:** Follow INSTALL.md, verify plugin loads and skills are discoverable
- **Validation:** `claude plugin validate .`
