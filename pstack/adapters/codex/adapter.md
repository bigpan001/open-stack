# Codex Platform Adapter

- **Platform**: Codex Desktop / CLI
- **Skill Format**: Standard Markdown with frontmatter (`skills/*/SKILL.md`)
- **Plugin Manifest**: `pstack/.codex-plugin/plugin.json`
- **Sub-Agent Primitive**: Built-in multi-agent delegation (`spawn_agent`, thread forks)
- **Automation Support**: `automation_update` (heartbeat / cron)
- **Model Configuration**: Model aliasing and reasoning effort via `pstack-models.json`

## Installation

```bash
# Local installation into Codex plugins cache
mkdir -p ~/.codex/plugins/cache/open-stack-local/pstack/0.14.7+codex.1
cp -r . ~/.codex/plugins/cache/open-stack-local/pstack/0.14.7+codex.1/
```

## Delegation & Swarm Execution
Codex natively supports spawning sub-agents. Multi-agent skills invoke sub-agents with specific model tags and wait for completion.

