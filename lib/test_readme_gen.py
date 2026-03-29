import json
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
