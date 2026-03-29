# Auto-Generated READMEs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Auto-generate marketplace and per-plugin READMEs from existing metadata using cogapp + LLM summaries.

**Architecture:** A shared Python module (`lib/readme_gen.py`) provides helpers that cog blocks in README files call to generate content from `marketplace.json`, `plugin.json`, and SKILL.md frontmatter. An LLM generates cached plugin summaries. A GitHub Action runs cog on push to `main` and commits changes.

**Tech Stack:** Python 3.11+, cogapp, llm CLI (with llm-github-models plugin), uv, GitHub Actions

---

### Task 1: Create `lib/readme_gen.py` with `repo_root()` and `extract_frontmatter()`

**Files:**
- Create: `lib/readme_gen.py`
- Create: `lib/test_readme_gen.py`

- [ ] **Step 1: Write failing tests for `repo_root()` and `extract_frontmatter()`**

```python
# lib/test_readme_gen.py
import readme_gen
from pathlib import Path


def test_repo_root_returns_parent_of_lib():
    root = readme_gen.repo_root()
    assert root.is_dir()
    assert (root / "lib" / "readme_gen.py").exists()


def test_extract_frontmatter_parses_name_and_description():
    content = "---\nname: my-skill\ndescription: Does a thing\n---\n\n# Body\n"
    result = readme_gen.extract_frontmatter(content)
    assert result == {"name": "my-skill", "description": "Does a thing"}


def test_extract_frontmatter_returns_empty_without_frontmatter():
    content = "# No Frontmatter\n\nJust content."
    result = readme_gen.extract_frontmatter(content)
    assert result == {"name": "", "description": ""}


def test_extract_frontmatter_returns_empty_for_empty_string():
    result = readme_gen.extract_frontmatter("")
    assert result == {"name": "", "description": ""}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: FAIL — `readme_gen` module has no functions yet

- [ ] **Step 3: Implement `repo_root()` and `extract_frontmatter()`**

```python
# lib/readme_gen.py
"""Shared helpers for cogapp-based README generation."""

import json
import subprocess
from pathlib import Path


def repo_root():
    """Return the repo root directory (parent of lib/)."""
    return Path(__file__).resolve().parent.parent


def extract_frontmatter(content):
    """Extract name and description from YAML frontmatter in SKILL.md content.

    Returns dict with 'name' and 'description' keys (empty strings if missing).
    """
    lines = content.split("\n")
    in_frontmatter = False
    name = ""
    description = ""

    for line in lines:
        if line.strip() == "---":
            if in_frontmatter:
                break
            in_frontmatter = True
            continue

        if in_frontmatter:
            if line.startswith("name:"):
                name = line[len("name:"):].strip()
            elif line.startswith("description:"):
                description = line[len("description:"):].strip()

    return {"name": name, "description": description}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: All 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add lib/readme_gen.py lib/test_readme_gen.py
git commit -m "Add readme_gen module with repo_root() and extract_frontmatter()"
```

---

### Task 2: Add `load_marketplace()` and `load_plugin_meta()`

**Files:**
- Modify: `lib/readme_gen.py`
- Modify: `lib/test_readme_gen.py`

- [ ] **Step 1: Write failing tests**

Append to `lib/test_readme_gen.py`:

```python
def test_load_marketplace_reads_plugins(tmp_path, monkeypatch):
    monkeypatch.setattr(readme_gen, "repo_root", lambda: tmp_path)
    manifest_dir = tmp_path / ".claude-plugin"
    manifest_dir.mkdir()
    (manifest_dir / "marketplace.json").write_text(json.dumps({
        "plugins": [
            {"name": "test-plugin", "source": "./plugins/test-plugin"}
        ]
    }))

    result = readme_gen.load_marketplace()
    assert len(result["plugins"]) == 1
    assert result["plugins"][0]["name"] == "test-plugin"


def test_load_plugin_meta_reads_plugin_json(tmp_path, monkeypatch):
    monkeypatch.setattr(readme_gen, "repo_root", lambda: tmp_path)
    plugin_dir = tmp_path / "plugins" / "my-plugin" / ".claude-plugin"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / "plugin.json").write_text(json.dumps({
        "name": "my-plugin",
        "description": "A test plugin",
        "author": {"name": "Tester"},
        "license": "MIT",
        "keywords": ["test"]
    }))

    result = readme_gen.load_plugin_meta("plugins/my-plugin")
    assert result["name"] == "my-plugin"
    assert result["author"]["name"] == "Tester"
```

Add `import json` to the test file imports.

- [ ] **Step 2: Run tests to verify new tests fail**

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: 2 new tests FAIL — functions not defined

- [ ] **Step 3: Implement `load_marketplace()` and `load_plugin_meta()`**

Append to `lib/readme_gen.py`:

```python
def load_marketplace():
    """Read .claude-plugin/marketplace.json and return parsed JSON."""
    path = repo_root() / ".claude-plugin" / "marketplace.json"
    return json.loads(path.read_text())


def load_plugin_meta(plugin_dir):
    """Read plugins/<name>/.claude-plugin/plugin.json and return parsed JSON.

    plugin_dir is relative to repo root (e.g. 'plugins/accelerated-learning').
    """
    path = repo_root() / plugin_dir / ".claude-plugin" / "plugin.json"
    return json.loads(path.read_text())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add lib/readme_gen.py lib/test_readme_gen.py
git commit -m "Add load_marketplace() and load_plugin_meta()"
```

---

### Task 3: Add `discover_skills()`

**Files:**
- Modify: `lib/readme_gen.py`
- Modify: `lib/test_readme_gen.py`

- [ ] **Step 1: Write failing tests**

Append to `lib/test_readme_gen.py`:

```python
def test_discover_skills_finds_skill_files(tmp_path, monkeypatch):
    monkeypatch.setattr(readme_gen, "repo_root", lambda: tmp_path)

    # Create two skills
    skill_a = tmp_path / "plugins" / "my-plugin" / "skills" / "skill-a"
    skill_a.mkdir(parents=True)
    (skill_a / "SKILL.md").write_text("---\nname: skill-a\ndescription: First\n---\n")

    skill_b = tmp_path / "plugins" / "my-plugin" / "skills" / "skill-b"
    skill_b.mkdir(parents=True)
    (skill_b / "SKILL.md").write_text("---\nname: skill-b\ndescription: Second\n---\n")

    skills = readme_gen.discover_skills("plugins/my-plugin")
    assert len(skills) == 2
    names = [s["name"] for s in skills]
    assert names == ["skill-a", "skill-b"]  # sorted alphabetically


def test_discover_skills_uses_dir_name_when_no_frontmatter(tmp_path, monkeypatch):
    monkeypatch.setattr(readme_gen, "repo_root", lambda: tmp_path)

    skill_dir = tmp_path / "plugins" / "my-plugin" / "skills" / "unnamed-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Just content\n")

    skills = readme_gen.discover_skills("plugins/my-plugin")
    assert len(skills) == 1
    assert skills[0]["name"] == "unnamed-skill"
    assert skills[0]["description"] == ""


def test_discover_skills_returns_empty_when_no_skills(tmp_path, monkeypatch):
    monkeypatch.setattr(readme_gen, "repo_root", lambda: tmp_path)
    plugin_dir = tmp_path / "plugins" / "empty-plugin" / "skills"
    plugin_dir.mkdir(parents=True)

    skills = readme_gen.discover_skills("plugins/empty-plugin")
    assert skills == []
```

- [ ] **Step 2: Run tests to verify new tests fail**

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: 3 new tests FAIL

- [ ] **Step 3: Implement `discover_skills()`**

Append to `lib/readme_gen.py`:

```python
def discover_skills(plugin_dir):
    """Find all SKILL.md files under plugins/<name>/skills/*/.

    Returns list of dicts with 'name' and 'description', sorted by name.
    plugin_dir is relative to repo root.
    """
    skills_dir = repo_root() / plugin_dir / "skills"
    if not skills_dir.is_dir():
        return []

    skills = []
    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir():
            continue
        skill_file = entry / "SKILL.md"
        if not skill_file.exists():
            continue
        meta = extract_frontmatter(skill_file.read_text())
        skills.append({
            "name": meta["name"] or entry.name,
            "description": meta["description"],
        })

    return skills
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: All 9 tests PASS

- [ ] **Step 5: Commit**

```bash
git add lib/readme_gen.py lib/test_readme_gen.py
git commit -m "Add discover_skills()"
```

---

### Task 4: Add `this_plugin_dir()` and `github_repo_url()`

**Files:**
- Modify: `lib/readme_gen.py`
- Modify: `lib/test_readme_gen.py`

- [ ] **Step 1: Write failing tests**

Append to `lib/test_readme_gen.py`:

```python
def test_this_plugin_dir_from_relative_path(tmp_path, monkeypatch):
    monkeypatch.setattr(readme_gen, "repo_root", lambda: tmp_path)
    plugin_readme = tmp_path / "plugins" / "my-plugin" / "README.md"
    plugin_readme.parent.mkdir(parents=True)
    plugin_readme.touch()

    result = readme_gen.this_plugin_dir(str(plugin_readme))
    assert result == "plugins/my-plugin"


def test_this_plugin_dir_from_absolute_path(tmp_path, monkeypatch):
    monkeypatch.setattr(readme_gen, "repo_root", lambda: tmp_path)
    plugin_readme = tmp_path / "plugins" / "deep-plugin" / "README.md"
    plugin_readme.parent.mkdir(parents=True)
    plugin_readme.touch()

    result = readme_gen.this_plugin_dir(str(plugin_readme.resolve()))
    assert result == "plugins/deep-plugin"


def test_github_repo_url():
    # Test against the real repo — this runs inside the rabbit-hole repo
    url = readme_gen.github_repo_url()
    assert "github.com" in url
    assert "rabbit-hole" in url
    assert not url.endswith(".git")
```

- [ ] **Step 2: Run tests to verify new tests fail**

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: 3 new tests FAIL

- [ ] **Step 3: Implement `this_plugin_dir()` and `github_repo_url()`**

Append to `lib/readme_gen.py`:

```python
def this_plugin_dir(cog_infile):
    """Resolve a cog input file path to its plugin directory relative to repo root.

    cog_infile is the value of cog.inFile (e.g. 'plugins/my-plugin/README.md'
    or an absolute path).
    """
    filepath = Path(cog_infile).resolve()
    root = repo_root()
    relative = filepath.relative_to(root)
    # Plugin dir is the first two components: plugins/<name>
    return str(Path(relative.parts[0]) / relative.parts[1])


def github_repo_url():
    """Derive the GitHub repo URL from git remote origin."""
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True, text=True, timeout=5,
    )
    if result.returncode != 0:
        return ""
    origin = result.stdout.strip()
    if origin.startswith("git@github.com:"):
        origin = origin.replace("git@github.com:", "https://github.com/")
    if origin.endswith(".git"):
        origin = origin[:-4]
    return origin
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: All 12 tests PASS

- [ ] **Step 5: Commit**

```bash
git add lib/readme_gen.py lib/test_readme_gen.py
git commit -m "Add this_plugin_dir() and github_repo_url()"
```

---

### Task 5: Add `get_or_create_summary()`

**Files:**
- Modify: `lib/readme_gen.py`
- Modify: `lib/test_readme_gen.py`

- [ ] **Step 1: Write failing test for cache hit path**

Append to `lib/test_readme_gen.py`:

```python
def test_get_or_create_summary_returns_cached(tmp_path, monkeypatch):
    monkeypatch.setattr(readme_gen, "repo_root", lambda: tmp_path)
    plugin_dir = tmp_path / "plugins" / "cached-plugin"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / "_summary.md").write_text("Cached summary paragraph.\n")

    result = readme_gen.get_or_create_summary("plugins/cached-plugin")
    assert result == "Cached summary paragraph."


def test_get_or_create_summary_calls_llm_on_miss(tmp_path, monkeypatch):
    monkeypatch.setattr(readme_gen, "repo_root", lambda: tmp_path)

    # Create a plugin with a skill but no _summary.md
    skill_dir = tmp_path / "plugins" / "new-plugin" / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ndescription: A skill\n---\n\n# Content\n")

    # Mock subprocess.run to fake the llm call
    original_run = subprocess.run

    def mock_run(cmd, **kwargs):
        if cmd[0] == "llm":
            class FakeResult:
                returncode = 0
                stdout = "Generated summary.\n"
                stderr = ""
            return FakeResult()
        return original_run(cmd, **kwargs)

    monkeypatch.setattr(subprocess, "run", mock_run)

    result = readme_gen.get_or_create_summary("plugins/new-plugin")
    assert result == "Generated summary."

    # Verify it was cached
    cache_file = tmp_path / "plugins" / "new-plugin" / "_summary.md"
    assert cache_file.exists()
    assert cache_file.read_text() == "Generated summary.\n"
```

Add `import subprocess` to the test file imports.

- [ ] **Step 2: Run tests to verify new tests fail**

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: 2 new tests FAIL

- [ ] **Step 3: Implement `get_or_create_summary()`**

Append to `lib/readme_gen.py`:

```python
_SUMMARY_PROMPT = (
    "Summarize this plugin for a marketplace README. "
    "Write 1 paragraph (3-5 sentences) describing what the plugin does "
    "and its key skills. Be specific and brief. No emoji."
)


def get_or_create_summary(plugin_dir, model="github/gpt-4.1"):
    """Return the plugin summary, generating via LLM if not cached.

    Checks for _summary.md in the plugin directory. On cache miss,
    concatenates all SKILL.md content, pipes to llm CLI, caches result.
    plugin_dir is relative to repo root.
    """
    root = repo_root()
    cache_path = root / plugin_dir / "_summary.md"

    if cache_path.exists():
        return cache_path.read_text().strip()

    # Concatenate all SKILL.md content
    skills_content = []
    skills_dir = root / plugin_dir / "skills"
    if skills_dir.is_dir():
        for entry in sorted(skills_dir.iterdir()):
            skill_file = entry / "SKILL.md"
            if skill_file.exists():
                skills_content.append(skill_file.read_text())

    if not skills_content:
        summary = "No skills found."
        cache_path.write_text(summary + "\n")
        return summary

    combined = "\n\n---\n\n".join(skills_content)

    result = subprocess.run(
        ["llm", "-m", model, "-s", _SUMMARY_PROMPT],
        input=combined,
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        error_msg = f"llm failed for {plugin_dir} (exit {result.returncode})"
        if result.stderr:
            error_msg += f"\n{result.stderr}"
        raise RuntimeError(error_msg)
    if not result.stdout.strip():
        raise RuntimeError(f"llm returned no output for {plugin_dir}")

    summary = result.stdout.strip()
    cache_path.write_text(summary + "\n")
    return summary
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: All 14 tests PASS

- [ ] **Step 5: Commit**

```bash
git add lib/readme_gen.py lib/test_readme_gen.py
git commit -m "Add get_or_create_summary() with LLM integration and caching"
```

---

### Task 6: Add cog block to root `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the Plugins section with a cog block**

The current `README.md` has a manually-maintained `## Plugins` section (lines 38-48). Replace it with a cog block. Keep all other sections (intro, installation, contributing, license) unchanged.

Replace this content in `README.md`:

```markdown
## Plugins

### accelerated-learning

Skills for accelerated learning workflows.

| Skill                  | Description                                                                  |
| ---------------------- | ---------------------------------------------------------------------------- |
| `creating-anki-cards`  | Generate Anki flashcards from course materials (slides, PDFs, lecture notes) |
| `translate-to-chinese` | Translate documents into Chinese with proper technical term handling         |

## Contributing
```

With:

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

## Contributing
```

- [ ] **Step 2: Run cog to generate the content**

Run: `cog -r -P -I lib README.md`

(Install cog first if needed: `uv tool install cogapp`)

This will populate the region between `[[[cog` and `[[[end]]]` with generated content. It will also trigger LLM calls to generate `_summary.md` files for each plugin that doesn't have one.

- [ ] **Step 3: Verify the generated README**

Read `README.md` and verify:
- The `## Plugins (2 available)` heading is present
- Both `accelerated-learning` and `burrow-keeper` are listed
- Each plugin has a summary paragraph
- Each plugin has a skills table with correct entries
- The installation section above and contributing/license sections below are unchanged

Also verify `plugins/accelerated-learning/_summary.md` and `plugins/burrow-keeper/_summary.md` were created.

- [ ] **Step 4: Commit**

```bash
git add README.md plugins/accelerated-learning/_summary.md plugins/burrow-keeper/_summary.md
git commit -m "Add cogapp block to root README for auto-generated plugin index"
```

---

### Task 7: Create per-plugin `README.md` files with cog blocks

**Files:**
- Create: `plugins/accelerated-learning/README.md`
- Create: `plugins/burrow-keeper/README.md`

- [ ] **Step 1: Create `plugins/accelerated-learning/README.md`**

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

- [ ] **Step 2: Create `plugins/burrow-keeper/README.md`**

Same content as Step 1 — identical template (cog resolves the plugin dir from `cog.inFile`):

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

- [ ] **Step 3: Run cog on both plugin READMEs**

```bash
for dir in plugins/*/; do cog -r -P -I lib "$dir/README.md"; done
```

- [ ] **Step 4: Verify generated output**

Read both plugin READMEs and verify:
- `plugins/accelerated-learning/README.md` has the correct title, description, summary, 3 skills (creating-anki-cards, studying-course-materials, translate-to-chinese), and metadata
- `plugins/burrow-keeper/README.md` has the correct title, description, summary, 1 skill (archiving-youtube), and metadata

- [ ] **Step 5: Commit**

```bash
git add plugins/accelerated-learning/README.md plugins/burrow-keeper/README.md
git commit -m "Add cogapp-generated per-plugin READMEs"
```

---

### Task 8: Create GitHub Actions workflow

**Files:**
- Create: `.github/workflows/update-readme.yml`

- [ ] **Step 1: Create the workflow file**

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
          uv tool install llm --with llm-github-models

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

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/update-readme.yml
git commit -m "Add GitHub Actions workflow for auto-updating READMEs"
```

---

### Task 9: Update `CLAUDE.md` and end-to-end verification

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add cog command to CLAUDE.md**

Add to the `## Commands` section in `CLAUDE.md`:

```markdown
- `cog -r -P -I lib README.md` — regenerate root README (requires `uv tool install cogapp`)
- `for dir in plugins/*/; do cog -r -P -I lib "$dir/README.md"; done` — regenerate plugin READMEs
```

- [ ] **Step 2: Run full regeneration and verify**

```bash
cog -r -P -I lib README.md
for dir in plugins/*/; do cog -r -P -I lib "$dir/README.md"; done
```

Verify:
- Root README lists both plugins with summaries and skill tables
- Each plugin README has title, description, summary, skills, and metadata
- `_summary.md` files exist for both plugins
- Running cog a second time produces no changes (idempotent)

- [ ] **Step 3: Run existing tests to ensure nothing is broken**

Run: `node --test lib/skills-core.test.js`
Expected: All existing JS tests PASS

Run: `uv run --with pytest pytest lib/test_readme_gen.py -v`
Expected: All Python tests PASS

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "Document cog commands in CLAUDE.md"
```
