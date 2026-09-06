# Pi Platform Adapter

- **Platform**: Pi Agent Runtime
- **Skill Format**: Markdown skills and instruction packs
- **Configuration**: `pi.json` and agent config under `~/.pi/`
- **Sub-Agent Primitive**: Pi worker process spawn / session delegator
- **Automation Support**: Shell cron / external watcher daemon

## Installation

```bash
# User global install (Pi loads from ~/.pi/agent/skills or ~/.agents/skills)
python3 scripts/install.py pi

# Project local install (loads from .agents/skills)
python3 scripts/install.py pi --project
```

## Delegation & Fallback
If Pi is running in single-turn CLI mode, multi-agent skills fall back to sequential step-by-step verification checklists.

