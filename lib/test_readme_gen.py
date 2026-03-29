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
