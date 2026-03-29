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
