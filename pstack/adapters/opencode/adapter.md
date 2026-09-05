# OpenCode Platform Adapter

- **Platform**: OpenCode AI Assistant / CLI
- **Skill Format**: Standard Markdown `SKILL.md`
- **Extension Manifest**: `.opencode/plugins/pstack.json`
- **Sub-Agent Primitive**: Subtask tool / CLI worker delegation
- **Automation Support**: Event triggers and OpenCode workflow hooks

## Installation

```bash
# Install to OpenCode extensions directory
mkdir -p ~/.opencode/skills
cp -r skills/* ~/.opencode/skills/
```

## Delegation
OpenCode delegates subtasks via its built-in subagent tool runner or external task script triggers.

