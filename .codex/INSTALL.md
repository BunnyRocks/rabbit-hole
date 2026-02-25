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
