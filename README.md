# rabbit-hole

A plugin marketplace for AI coding assistants. Currently hosts the **accelerated-learning** plugin with skills for Anki flashcard creation and document translation.

Supports Claude Code, Codex, and OpenCode.

## Installation

### Claude Code

```shell
/plugin marketplace add BunnyRocks/rabbit-hole
/plugin install accelerated-learning@rabbit-hole
```

### Codex

See [.codex/INSTALL.md](.codex/INSTALL.md).

### OpenCode

See [.opencode/INSTALL.md](.opencode/INSTALL.md).

## Plugins

### accelerated-learning

Skills for accelerated learning workflows.

| Skill | Description |
|-------|-------------|
| `creating-anki-cards` | Generate Anki flashcards from course materials (slides, PDFs, lecture notes) |
| `translate-to-chinese` | Translate documents into Chinese with proper technical term handling |

## Contributing

Add new skills under `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` and register the plugin in `.claude-plugin/marketplace.json`.

## License

MIT
