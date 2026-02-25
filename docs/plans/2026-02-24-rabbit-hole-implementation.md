# rabbit-hole Marketplace Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a multi-provider Claude Code plugin marketplace hosting an "accelerated-learning" plugin with Anki flashcard and translation skills.

**Architecture:** Monorepo with plugin-per-directory layout. Marketplace manifest at root, one plugin under `plugins/accelerated-learning/`. Thin per-provider integrations for Claude Code (native plugin system), Codex (symlinks), and OpenCode (JS plugin + symlinks).

**Tech Stack:** JSON manifests, Markdown skills, JavaScript (ES modules) for OpenCode plugin and shared utils. Node.js for testing.

---

### Task 1: Project scaffolding — .gitignore and directory structure

**Files:**
- Create: `.gitignore`
- Create: `plugins/accelerated-learning/skills/.gitkeep` (placeholder to establish directory)

**Step 1: Create .gitignore**

```
node_modules/
.DS_Store
*.log
```

**Step 2: Create directory structure**

```bash
mkdir -p plugins/accelerated-learning/.claude-plugin
mkdir -p plugins/accelerated-learning/skills/creating-anki-cards
mkdir -p plugins/accelerated-learning/skills/translate-to-chinese
mkdir -p .claude-plugin
mkdir -p .codex
mkdir -p .opencode/plugins
mkdir -p lib
```

**Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: add .gitignore"
```

---

### Task 2: Marketplace manifest and plugin.json

**Files:**
- Create: `.claude-plugin/marketplace.json`
- Create: `plugins/accelerated-learning/.claude-plugin/plugin.json`

**Step 1: Create marketplace.json**

```json
{
  "name": "rabbit-hole",
  "owner": {
    "name": "BunnyRocks"
  },
  "metadata": {
    "description": "Skills for going deeper down the rabbit hole",
    "version": "0.1.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "accelerated-learning",
      "source": "accelerated-learning",
      "description": "Skills for accelerated learning — Anki cards, translation, research",
      "version": "0.1.0",
      "keywords": ["learning", "anki", "flashcards", "translation"],
      "category": "education"
    }
  ]
}
```

**Step 2: Create plugin.json**

```json
{
  "name": "accelerated-learning",
  "description": "Skills for accelerated learning",
  "version": "0.1.0",
  "author": {
    "name": "BunnyRocks"
  },
  "homepage": "https://github.com/BunnyRocks/rabbit-hole",
  "repository": "https://github.com/BunnyRocks/rabbit-hole",
  "license": "MIT",
  "keywords": ["learning", "anki", "flashcards", "translation"]
}
```

**Step 3: Validate the marketplace**

Run: `claude plugin validate .`
Expected: No errors (warnings about missing skills OK at this stage)

**Step 4: Commit**

```bash
git add .claude-plugin/marketplace.json plugins/accelerated-learning/.claude-plugin/plugin.json
git commit -m "feat: add marketplace manifest and plugin.json"
```

---

### Task 3: Copy skills into plugin

**Files:**
- Create: `plugins/accelerated-learning/skills/creating-anki-cards/SKILL.md`
- Create: `plugins/accelerated-learning/skills/translate-to-chinese/SKILL.md`

**Step 1: Copy creating-anki-cards skill**

Copy the full content of `~/.claude/skills/creating-anki-cards/SKILL.md` to `plugins/accelerated-learning/skills/creating-anki-cards/SKILL.md`. The content is preserved exactly — same frontmatter, same body.

**Step 2: Copy translate-to-chinese skill**

Copy the full content of `~/.claude/skills/translate-to-chinese/SKILL.md` to `plugins/accelerated-learning/skills/translate-to-chinese/SKILL.md`. Preserved exactly.

**Step 3: Validate**

Run: `claude plugin validate .`
Expected: Pass with no errors. Skills should be detected.

**Step 4: Commit**

```bash
git add plugins/accelerated-learning/skills/
git commit -m "feat: add creating-anki-cards and translate-to-chinese skills"
```

---

### Task 4: Shared utility — lib/skills-core.js

**Files:**
- Create: `lib/skills-core.js`
- Create: `lib/skills-core.test.js`
- Create: `package.json` (root, for running tests)

**Step 1: Create package.json**

```json
{
  "name": "rabbit-hole",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "node --test lib/skills-core.test.js"
  }
}
```

**Step 2: Write the failing tests**

`lib/skills-core.test.js`:
```javascript
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
```

**Step 3: Run tests to verify they fail**

Run: `node --test lib/skills-core.test.js`
Expected: FAIL — module `./skills-core.js` not found

**Step 4: Write skills-core.js**

`lib/skills-core.js`:
```javascript
import fs from 'fs';
import path from 'path';

/**
 * Extract YAML frontmatter from a skill file.
 * @param {string} filePath - Path to SKILL.md file
 * @returns {{name: string, description: string}}
 */
function extractFrontmatter(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');

    let inFrontmatter = false;
    let name = '';
    let description = '';

    for (const line of lines) {
      if (line.trim() === '---') {
        if (inFrontmatter) break;
        inFrontmatter = true;
        continue;
      }

      if (inFrontmatter) {
        const match = line.match(/^(\w+):\s*(.*)$/);
        if (match) {
          const [, key, value] = match;
          if (key === 'name') name = value.trim();
          if (key === 'description') description = value.trim();
        }
      }
    }

    return { name, description };
  } catch {
    return { name: '', description: '' };
  }
}

/**
 * Find all SKILL.md files in a directory recursively.
 * @param {string} dir - Directory to search
 * @param {string} sourceType - Label for namespacing (e.g., 'rabbit-hole')
 * @param {number} maxDepth - Maximum recursion depth (default: 3)
 * @returns {Array<{path: string, skillFile: string, name: string, description: string, sourceType: string}>}
 */
function findSkillsInDir(dir, sourceType, maxDepth = 3) {
  const skills = [];
  if (!fs.existsSync(dir)) return skills;

  function recurse(currentDir, depth) {
    if (depth > maxDepth) return;
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        const skillFile = path.join(fullPath, 'SKILL.md');
        if (fs.existsSync(skillFile)) {
          const { name, description } = extractFrontmatter(skillFile);
          skills.push({
            path: fullPath,
            skillFile,
            name: name || entry.name,
            description: description || '',
            sourceType,
          });
        }
        recurse(fullPath, depth + 1);
      }
    }
  }

  recurse(dir, 0);
  return skills;
}

/**
 * Strip YAML frontmatter from content, returning just the body.
 * @param {string} content - Full content including frontmatter
 * @returns {string}
 */
function stripFrontmatter(content) {
  const lines = content.split('\n');
  let inFrontmatter = false;
  let frontmatterEnded = false;
  const contentLines = [];

  for (const line of lines) {
    if (line.trim() === '---') {
      if (inFrontmatter) {
        frontmatterEnded = true;
        continue;
      }
      inFrontmatter = true;
      continue;
    }
    if (frontmatterEnded || !inFrontmatter) {
      contentLines.push(line);
    }
  }

  return contentLines.join('\n').trim();
}

export { extractFrontmatter, findSkillsInDir, stripFrontmatter };
```

**Step 5: Run tests to verify they pass**

Run: `node --test lib/skills-core.test.js`
Expected: All tests PASS

**Step 6: Commit**

```bash
git add package.json lib/skills-core.js lib/skills-core.test.js
git commit -m "feat: add skills-core.js shared utility with tests"
```

---

### Task 5: OpenCode plugin

**Files:**
- Create: `.opencode/plugins/rabbit-hole.js`
- Create: `.opencode/INSTALL.md`

**Step 1: Create rabbit-hole.js**

`.opencode/plugins/rabbit-hole.js` — follows the same pattern as superpowers' plugin but adapted for our marketplace structure:

```javascript
/**
 * rabbit-hole plugin for OpenCode.ai
 *
 * Lists available skills from the accelerated-learning plugin
 * and injects discovery context via system prompt transform.
 */

import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Inline frontmatter parser (avoid dependency on lib/skills-core for bootstrap)
const extractAndStripFrontmatter = (content) => {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { frontmatter: {}, content };

  const frontmatterStr = match[1];
  const body = match[2];
  const frontmatter = {};

  for (const line of frontmatterStr.split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx > 0) {
      const key = line.slice(0, colonIdx).trim();
      const value = line.slice(colonIdx + 1).trim().replace(/^["']|["']$/g, '');
      frontmatter[key] = value;
    }
  }

  return { frontmatter, content: body };
};

// Discover all skills in our plugins directory
const discoverSkills = (pluginsDir) => {
  const skills = [];
  if (!fs.existsSync(pluginsDir)) return skills;

  const walkPluginSkills = (skillsDir) => {
    if (!fs.existsSync(skillsDir)) return;
    for (const entry of fs.readdirSync(skillsDir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const skillFile = path.join(skillsDir, entry.name, 'SKILL.md');
      if (!fs.existsSync(skillFile)) continue;
      const content = fs.readFileSync(skillFile, 'utf8');
      const { frontmatter } = extractAndStripFrontmatter(content);
      skills.push({
        name: frontmatter.name || entry.name,
        description: frontmatter.description || '',
      });
    }
  };

  // Walk each plugin's skills/ directory
  for (const plugin of fs.readdirSync(pluginsDir, { withFileTypes: true })) {
    if (!plugin.isDirectory()) continue;
    walkPluginSkills(path.join(pluginsDir, plugin.name, 'skills'));
  }

  return skills;
};

export const RabbitHolePlugin = async ({ client, directory }) => {
  const pluginsDir = path.resolve(__dirname, '../../plugins');

  const getBootstrapContent = () => {
    const skills = discoverSkills(pluginsDir);
    if (skills.length === 0) return null;

    const skillList = skills
      .map((s) => `- **${s.name}**: ${s.description}`)
      .join('\n');

    return `**rabbit-hole skills available:**
${skillList}

**Tool Mapping for OpenCode:**
When skills reference tools you don't have, substitute OpenCode equivalents:
- \`TodoWrite\` → \`update_plan\`
- \`Task\` tool with subagents → Use OpenCode's subagent system (@mention)
- \`Skill\` tool → OpenCode's native \`skill\` tool
- \`Read\`, \`Write\`, \`Edit\`, \`Bash\` → Your native tools`;
  };

  return {
    'experimental.chat.system.transform': async (_input, output) => {
      const bootstrap = getBootstrapContent();
      if (bootstrap) {
        (output.system ||= []).push(bootstrap);
      }
    },
  };
};
```

**Step 2: Create .opencode/INSTALL.md**

```markdown
# Installing rabbit-hole for OpenCode

## Prerequisites

- OpenCode.ai installed
- Git installed

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BunnyRocks/rabbit-hole.git ~/.config/opencode/rabbit-hole
   ```

2. **Register the plugin:**
   ```bash
   mkdir -p ~/.config/opencode/plugins
   ln -s ~/.config/opencode/rabbit-hole/.opencode/plugins/rabbit-hole.js ~/.config/opencode/plugins/rabbit-hole.js
   ```

3. **Symlink skills:**
   ```bash
   mkdir -p ~/.config/opencode/skills
   ln -s ~/.config/opencode/rabbit-hole/plugins/accelerated-learning/skills ~/.config/opencode/skills/accelerated-learning
   ```

4. **Restart OpenCode.**

## Updating

```bash
cd ~/.config/opencode/rabbit-hole && git pull
```

## Uninstalling

```bash
rm ~/.config/opencode/plugins/rabbit-hole.js
rm ~/.config/opencode/skills/accelerated-learning
rm -rf ~/.config/opencode/rabbit-hole
```
```

**Step 3: Commit**

```bash
git add .opencode/
git commit -m "feat: add OpenCode plugin and install instructions"
```

---

### Task 6: Codex install instructions

**Files:**
- Create: `.codex/INSTALL.md`

**Step 1: Create .codex/INSTALL.md**

```markdown
# Installing rabbit-hole for Codex

Codex natively reads SKILL.md files. Just clone and symlink.

## Prerequisites

- Git installed

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BunnyRocks/rabbit-hole.git ~/.codex/rabbit-hole
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/rabbit-hole/plugins/accelerated-learning/skills ~/.agents/skills/accelerated-learning
   ```

3. **Restart Codex** to discover the skills.

## Updating

```bash
cd ~/.codex/rabbit-hole && git pull
```

## Uninstalling

```bash
rm ~/.agents/skills/accelerated-learning
rm -rf ~/.codex/rabbit-hole
```
```

**Step 2: Commit**

```bash
git add .codex/
git commit -m "feat: add Codex install instructions"
```

---

### Task 7: README and LICENSE

**Files:**
- Create: `README.md`
- Create: `LICENSE`

**Step 1: Create README.md**

```markdown
# rabbit-hole

A plugin marketplace for AI coding assistants. Currently hosts the **accelerated-learning** plugin with skills for Anki flashcard creation and document translation.

Supports Claude Code, Codex, and OpenCode.

## Installation

### Claude Code

```shell
/plugin marketplace add BunnyRocks/rabbit-hole
/plugin install accelerated-learning@rabbit-hole
```

### Codex

See [.codex/INSTALL.md](.codex/INSTALL.md).

### OpenCode

See [.opencode/INSTALL.md](.opencode/INSTALL.md).

## Plugins

### accelerated-learning

Skills for accelerated learning workflows.

| Skill | Description |
|-------|-------------|
| `creating-anki-cards` | Generate Anki flashcards from course materials (slides, PDFs, lecture notes) |
| `translate-to-chinese` | Translate documents into Chinese with proper technical term handling |

## Contributing

Add new skills under `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` and register the plugin in `.claude-plugin/marketplace.json`.

## License

MIT
```

**Step 2: Create LICENSE**

Standard MIT license with "BunnyRocks" as copyright holder, year 2026.

**Step 3: Commit**

```bash
git add README.md LICENSE
git commit -m "docs: add README and MIT license"
```

---

### Task 8: Validate and test locally

**Step 1: Run marketplace validation**

Run: `claude plugin validate .`
Expected: Pass with no errors

**Step 2: Test local installation in Claude Code**

Run: `/plugin marketplace add ./`
Then: `/plugin install accelerated-learning@rabbit-hole`
Verify: Both skills appear in available skills list

**Step 3: Fix any validation or installation issues**

If validation or install fails, fix the issue and recommit.

**Step 4: Commit any fixes**

---

### Task 9: Push to GitHub

**Step 1: Create the remote repo (if not exists)**

```bash
gh repo create BunnyRocks/rabbit-hole --public --description "Plugin marketplace for AI coding assistants" --source=. --remote=origin
```

**Step 2: Push**

```bash
git push -u origin main
```

**Step 3: Verify marketplace can be added from GitHub**

```
/plugin marketplace add BunnyRocks/rabbit-hole
```
