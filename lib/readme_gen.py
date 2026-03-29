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
