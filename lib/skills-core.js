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
