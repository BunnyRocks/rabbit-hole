# rabbit-hole

Plugin marketplace for AI coding assistants (Claude Code, Codex, OpenCode).

## Structure

- `.claude-plugin/marketplace.json` — marketplace manifest
- `plugins/<name>/` — each plugin is self-contained with `.claude-plugin/plugin.json` and `skills/`
- `lib/skills-core.js` — shared utility for SKILL.md parsing (JS)
- `lib/readme_gen.py` — shared helpers for cogapp-based README generation (Python)
- `.opencode/plugins/rabbit-hole.js` — OpenCode integration plugin
- `.codex/INSTALL.md`, `.opencode/INSTALL.md` — provider install guides

## Commands

- `node --test lib/skills-core.test.js` — run tests (Node built-in runner, ES modules)
- `claude plugin validate .` — validate marketplace manifest (run after any manifest change)
- `uv run --with pytest pytest lib/test_readme_gen.py -v` — run Python tests
- `uvx --from cogapp cog -r -P -I lib README.md` — regenerate root README (requires `llm` with `llm-github-models`)
- `for dir in plugins/*/; do uvx --from cogapp cog -r -P -I lib "$dir/README.md"; done` — regenerate plugin READMEs

## Gotchas

- Marketplace `source` paths MUST start with `./` and are relative to the marketplace root
- Global `~/.gitignore_global` ignores `lib/` — project `.gitignore` has `!lib/` override
- Skills are auto-discovered by directory structure (SKILL.md files in `plugins/*/skills/*/`)
