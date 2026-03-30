# Auto-Generated READMEs via Cogapp + LLM

## Problem

READMEs go stale when plugins and skills are added or changed. The current root README still only lists `accelerated-learning` despite `burrow-keeper` being added. Manually updating README prose across multiple files doesn't scale.

## Solution

Use [cogapp](https://nedbatchelder.com/code/cog/) to embed Python code blocks in README files that auto-generate content from existing metadata (`marketplace.json`, `plugin.json`, SKILL.md frontmatter). Use the `llm` CLI to generate cached one-paragraph plugin summaries. A GitHub Action runs cog on every push to `main` and commits the results.

This mirrors the pattern used in the [research repo](https://github.com/ziyunli/research).

## Scope

- **Root `README.md`** — auto-generated plugin index with skill tables and LLM summaries
- **Per-plugin `plugins/<name>/README.md`** — auto-generated plugin detail page (new files)
- **No per-skill READMEs** — SKILL.md is already the source of truth at that level

## File Layout

```
lib/readme_gen.py                         # Shared helpers
.github/workflows/update-readme.yml       # CI: cog on push to main
README.md                                 # Root README with cog blocks
plugins/<name>/README.md                  # Per-plugin READMEs with cog blocks
plugins/<name>/_summary.md                # LLM-generated summaries (cached)
```

## `lib/readme_gen.py` — Shared Helpers

A Python module imported by cog blocks in each README. Functions:

- **`load_marketplace()`** — reads `.claude-plugin/marketplace.json`, returns parsed JSON
- **`load_plugin_meta(plugin_dir)`** — reads `plugins/<name>/.claude-plugin/plugin.json`, returns parsed JSON
- **`discover_skills(plugin_dir)`** — finds all `SKILL.md` files under `plugins/<name>/skills/*/`, extracts YAML frontmatter (`name`, `description`), returns list of dicts
- **`get_or_create_summary(plugin_dir, model="github/gpt-4.1")`** — returns cached `_summary.md` content if it exists; otherwise concatenates all SKILL.md files in the plugin, pipes to `llm -m <model>` with a summary prompt, writes result to `_summary.md`, returns it
- **`github_repo_url()`** — derives GitHub URL from `git remote get-url origin`
- **`repo_root()`** — finds the repo root by walking up to locate `.git`; all other functions resolve paths relative to this
- **`this_plugin_dir(cog_infile)`** — resolves a cog input file path (via `cog.inFile`) to its plugin directory relative to the repo root

### LLM Summary Prompt

```
Summarize this plugin for a marketplace README. Write 1 paragraph (3-5 sentences)
describing what the plugin does and its key skills. Be specific and brief. No emoji.
```

### Summary Caching

- Summaries are written to `plugins/<name>/_summary.md`
- Cached files are git-tracked (committed by the GitHub Action)
- To regenerate: delete the `_summary.md` file and re-run cog
- LLM is only invoked on cache miss

## Cog Blocks

### Root `README.md`

The cog block replaces the current manually-maintained "Plugins" section. Everything outside the cog block (intro, installation, contributing, license) stays static.

```markdown
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
<!--[[[end]]]-->
```

### Per-Plugin `plugins/<name>/README.md`

Each plugin gets a README that surfaces its metadata, summary, and skill list.

```markdown
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
<!--[[[end]]]-->
```

## GitHub Actions Workflow

Triggered on push to `main`. Runs cog on all READMEs and commits changes.

```yaml
name: Update READMEs with cogapp

on:
  push:
    branches: [main]

permissions:
  contents: write
  models: read

jobs:
  update-readmes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - uses: astral-sh/setup-uv@v6

      - name: Install tools
        run: |
          uv tool install cogapp
          uv tool install llm
          uv run --with llm-github-models -- python -c "import llm_github_models"

      - name: Run cog on all READMEs
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          cog -r -P -I lib README.md
          for dir in plugins/*/; do
            if [ -f "$dir/README.md" ]; then
              cog -r -P -I lib "$dir/README.md"
            fi
          done

      - name: Commit if changed
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add README.md
          git add plugins/*/README.md 2>/dev/null || true
          git add plugins/*/_summary.md 2>/dev/null || true
          if git diff --staged --quiet; then
            echo "No changes to commit"
          else
            git commit -m "Auto-update READMEs [skip ci]"
            git push
          fi
```

Note: The `uv tool install` / `uv run --with` invocations for `llm` and `llm-github-models` need verification — the exact incantation depends on how `llm` plugins are registered. The implementation should test this and adjust.

## Local Usage

```bash
uv tool install cogapp
cog -r -P -I lib README.md
for dir in plugins/*/; do [ -f "$dir/README.md" ] && cog -r -P -I lib "$dir/README.md"; done
```

To regenerate a plugin summary: delete `plugins/<name>/_summary.md` and re-run.

## Dependencies

All managed via `uv`:

- `cogapp` — cog templating engine
- `llm` — CLI for LLM inference
- `llm-github-models` — GitHub Models plugin for `llm`

No `requirements.txt` — tools are installed via `uv tool install`.

## What Stays Manual

- Root README intro paragraph, installation section, contributing section, license
- SKILL.md content (the actual skill documentation)
- Plugin metadata in `plugin.json` and `marketplace.json`

## Testing

- Run `cog -r -P -I lib README.md` locally and verify the generated output matches expectations
- Verify `_summary.md` caching: run twice, confirm LLM is only called on first run
- Verify new plugin pickup: add a plugin to `marketplace.json`, run cog, confirm it appears
