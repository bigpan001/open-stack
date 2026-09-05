# Kimi Platform Adapter

- **Platform**: Kimi for Coding / Kimi Workspace Agent
- **Skill Format**: Markdown skill blocks and prompt templates
- **Registration**: Workspace system prompt packs or agent workspace config
- **Sub-Agent Primitive**: Single-turn context handoff / Multi-step tool calls
- **Automation Support**: Scheduled runners / Webhook triggers

## Installation

```bash
# Import prompt skills into Kimi workspace or local skills folder
kimi agent import ./skills
```

## Delegation & Fallback
Kimi executes multi-phase orchestrations sequentially within the active conversation context, adhering strictly to verification gates.

