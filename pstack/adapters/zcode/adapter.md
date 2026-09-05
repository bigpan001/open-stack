# ZCode Platform Adapter

- **Platform**: ZCode IDE / Assistant
- **Skill Format**: Standard Markdown skills
- **Manifest**: `pstack/adapters/zcode/zcode-plugin.json`
- **Sub-Agent Primitive**: Sub-process worker / IDE task runner
- **Automation Support**: IDE background runner / Cron tasks

## Installation

```bash
# Link or copy to ZCode skills path
mkdir -p ~/.zcode/skills
cp -r skills/* ~/.zcode/skills/
```

## Delegation
ZCode runs sub-agent tasks using IDE background workers or sequential task decomposition.

