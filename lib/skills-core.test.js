import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { extractFrontmatter, findSkillsInDir, stripFrontmatter } from './skills-core.js';
import fs from 'fs';
import path from 'path';
import os from 'os';

describe('extractFrontmatter', () => {
  it('parses name and description from SKILL.md frontmatter', () => {
    const skillDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-'));
    const skillFile = path.join(skillDir, 'SKILL.md');
    fs.writeFileSync(skillFile, `---
name: test-skill
description: Use when testing
---

# Test Skill

Body content here.
`);

    const result = extractFrontmatter(skillFile);
    assert.equal(result.name, 'test-skill');
    assert.equal(result.description, 'Use when testing');

    fs.rmSync(skillDir, { recursive: true });
  });

  it('returns empty strings for file without frontmatter', () => {
    const skillDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-'));
    const skillFile = path.join(skillDir, 'SKILL.md');
    fs.writeFileSync(skillFile, '# No Frontmatter\n\nJust content.');

    const result = extractFrontmatter(skillFile);
    assert.equal(result.name, '');
    assert.equal(result.description, '');

    fs.rmSync(skillDir, { recursive: true });
  });

  it('returns empty strings for nonexistent file', () => {
    const result = extractFrontmatter('/tmp/does-not-exist-skill.md');
    assert.equal(result.name, '');
    assert.equal(result.description, '');
  });
});

describe('findSkillsInDir', () => {
  it('finds SKILL.md files recursively', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skills-'));
    const skill1Dir = path.join(tmpDir, 'skill-a');
    const skill2Dir = path.join(tmpDir, 'skill-b');
    fs.mkdirSync(skill1Dir);
    fs.mkdirSync(skill2Dir);
    fs.writeFileSync(path.join(skill1Dir, 'SKILL.md'), '---\nname: skill-a\ndescription: First skill\n---\n');
    fs.writeFileSync(path.join(skill2Dir, 'SKILL.md'), '---\nname: skill-b\ndescription: Second skill\n---\n');

    const skills = findSkillsInDir(tmpDir, 'test');
    assert.equal(skills.length, 2);

    const names = skills.map(s => s.name).sort();
    assert.deepEqual(names, ['skill-a', 'skill-b']);
    assert.equal(skills[0].sourceType, 'test');

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('returns empty array for nonexistent directory', () => {
    const skills = findSkillsInDir('/tmp/does-not-exist-dir', 'test');
    assert.deepEqual(skills, []);
  });

  it('uses directory name when frontmatter has no name', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skills-'));
    const skillDir = path.join(tmpDir, 'my-unnamed-skill');
    fs.mkdirSync(skillDir);
    fs.writeFileSync(path.join(skillDir, 'SKILL.md'), '# Just content\n');

    const skills = findSkillsInDir(tmpDir, 'test');
    assert.equal(skills.length, 1);
    assert.equal(skills[0].name, 'my-unnamed-skill');

    fs.rmSync(tmpDir, { recursive: true });
  });
});

describe('stripFrontmatter', () => {
  it('strips YAML frontmatter and returns body', () => {
    const content = `---
name: test
description: A test
---

# Body

Content here.`;

    const result = stripFrontmatter(content);
    assert.equal(result, '# Body\n\nContent here.');
  });

  it('returns content unchanged when no frontmatter', () => {
    const content = '# No Frontmatter\n\nJust content.';
    const result = stripFrontmatter(content);
    assert.equal(result, content);
  });
});
