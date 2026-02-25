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
