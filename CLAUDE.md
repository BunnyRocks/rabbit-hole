# rabbit-hole

Plugin marketplace for AI coding assistants (Claude Code, Codex, OpenCode).

## Structure

- `.claude-plugin/marketplace.json` — marketplace manifest (uses `pluginRoot: "./plugins"`)
- `plugins/<name>/` — each plugin is self-contained with `.claude-plugin/plugin.json` and `skills/`
- `lib/skills-core.js` — shared utility for SKILL.md parsing
- `.opencode/plugins/rabbit-hole.js` — OpenCode integration plugin
- `.codex/INSTALL.md`, `.opencode/INSTALL.md` — provider install guides

## Commands

- `node --test lib/skills-core.test.js` — run tests (Node built-in runner, ES modules)
- `claude plugin validate .` — validate marketplace manifest (run after any manifest change)

## Gotchas

- Marketplace `source` paths MUST start with `./` even when `pluginRoot` is set
- Global `~/.gitignore_global` ignores `lib/` — project `.gitignore` has `!lib/` override
- Skills are auto-discovered by directory structure (SKILL.md files in `plugins/*/skills/*/`)
