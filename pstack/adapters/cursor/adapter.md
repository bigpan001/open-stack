# Cursor Platform Adapter

- **Platform**: Cursor IDE (Composer / Agent)
- **Skill Format**: Standard Markdown (`skills/*/SKILL.md`)
- **Plugin Manifest**: `pstack/.cursor-plugin/plugin.json`
- **Sub-Agent Primitive**: Cursor background tasks and agent sessions
- **Automation Support**: Composer loop / background rules
- **Rules Path**: `~/.cursor/` or project workspace `.cursorrules`

## Installation

```bash
# Link or copy skills to Cursor's global or workspace directory
mkdir -p ~/.cursor/skills
cp -r skills/* ~/.cursor/skills/
```

## Delegation
Cursor executes subagents via background tasks or sequential session switches.

