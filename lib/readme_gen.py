"""Shared helpers for cogapp-based README generation."""

import json
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
