# Pi Platform Adapter

- **Platform**: Pi Agent Runtime
- **Skill Format**: Markdown skills and instruction packs
- **Configuration**: `pi.json` and agent config under `~/.pi/`
- **Sub-Agent Primitive**: Pi worker process spawn / session delegator
- **Automation Support**: Shell cron / external watcher daemon

## Installation

```bash
# Register pstack skills with Pi agent
pi skills add ./skills
# Or copy to ~/.pi/skills
mkdir -p ~/.pi/skills
cp -r skills/* ~/.pi/skills/
```

## Delegation & Fallback
If Pi is running in single-turn CLI mode, multi-agent skills fall back to sequential step-by-step verification checklists.

