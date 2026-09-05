# Universal Runtime Adapter & Matrix

This document defines the cross-agent portability contract for pstack skills, tools, sub-agent delegation, and installation across supported Agent runtimes: **Codex, Cursor, Pi, OpenCode, Kimi, and ZCode**.

## 1. Architectural Model: Universal Core vs. Platform Adapters

pstack separates its capabilities into two strict layers:

1. **Universal Skill Core (`pstack/skills/*`)**:
   - Pure instruction specifications adhering to standard Markdown frontmatter (`name`, `description`).
   - Agnostic to proprietary agent tools (does not hardcode vendor-locked primitives like `spawn_agent` or Cursor-only frontmatter into core skills).
   - Standardized behavioral protocols (checklists, verification gates, reflection loops, no-comment diff enforcement).

2. **Platform Adaptation Layer (`pstack/adapters/<platform>/`)**:
   - Platform discovery & plugin manifest / metadata definition.
   - Sub-agent and task delegation bridge (how multi-agent swarms execute on the host runtime).
   - Automated heartbeat, triggers, and scheduled task mechanics.
   - Environment paths, model routing tables, and install / update scripts.

---

## 2. Platform Capability Matrix

| Platform | Skill Standard | Manifest / Registration | Sub-Agent / Delegation Primitive | Automation / Loop Support | Primary Config Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Codex** | Markdown `SKILL.md` with standard frontmatter | `.codex-plugin/plugin.json` | Built-in `spawn_agent` / desktop thread fork | `automation_update` (heartbeat / cron) | `~/.codex/plugins/cache/...` or repo plugin |
| **Cursor** | Markdown `SKILL.md` | `.cursor-plugin/plugin.json` | Cursor Background Task / Subagent runner | Composer loop & background rules | Cursor home or workspace `.cursorrules` |
| **Pi** | Markdown `SKILL.md` / prompt modules | Agent config / tool extension manifest | Task-worker process spawn / Pi session call | Shell cron / watcher daemon | `~/.pi/`, `pi.json` |
| **OpenCode** | Markdown `SKILL.md` / system rules | OpenCode extension / plugin descriptor | Subtask tool / CLI worker delegation | Event triggers & workflow hooks | `~/.opencode/`, `.opencode/plugins` |
| **Kimi** | Markdown Prompt / Skill file | Agent marketplace / Workspace prompt pack | Single-turn context handoff / Multi-step tool | Scheduled runner / Webhook agent | Workspace prompts / Kimi Agent config |
| **ZCode** | Markdown `SKILL.md` / IDE skill format | IDE plugin manifest / settings JSON | Sub-process agent runner / Task worker | IDE background runner / Cron tasks | `~/.zcode/`, project workspace config |

---

## 3. Abstract Delegation Contract

When skills require multi-agent orchestration (such as `swarm`, `arena`, `poteto-agent`), use the abstract delegation protocol:

1. **Check Platform Adapter**: Inspect `adapters/<platform>/adapter.md` to identify the runtime's execution capability.
2. **Graceful Fallback**:
   - **Native Multi-Agent** (Codex, Cursor, OpenCode): Spawn specialized child workers with isolated roles and await completion.
   - **Single-Agent / Sequential Fallback** (Kimi, Pi, ZCode CLI): If sub-agents cannot be spawned concurrently by the host environment, execute tasks sequentially using strict phase gating and verification checklists within the active session.

---

## 4. Universal Distribution Layout

```
pstack/
├── skills/                  # Universal Skill Core (Portable across all 6 runtimes)
├── adapters/                # Platform Adaptation Layer
│   ├── codex/               # Codex manifest, automation, and spawn adapter
│   ├── cursor/              # Cursor plugin manifest and rules adapter
│   ├── pi/                  # Pi runtime configuration and dispatch adapter
│   ├── opencode/            # OpenCode tool and plugin adapter
│   ├── kimi/                # Kimi agent prompt and execution adapter
│   └── zcode/               # ZCode IDE integration and task runner adapter
├── scripts/                 # Universal install and verification scripts
└── README.md                # Multi-platform installation and usage guide
```
