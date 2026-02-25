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
