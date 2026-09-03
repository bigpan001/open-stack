#!/usr/bin/env python3
"""Apply the repeatable mechanical part of the pstack Cursor-to-Codex port."""

from __future__ import annotations

import re
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "pstack"
SKILLS = PLUGIN / "skills"

UNSUPPORTED_FRONTMATTER = {
    "disable-model-invocation",
    "mode",
    "icon",
    "color",
    "reminder",
    "paths",
}

TEXT_REPLACEMENTS = {
    "claude-fable-5-1-thinking-max": "gpt-5.6-sol",
    "gpt-5.6-sol-max": "gpt-5.6-sol",
    "grok-4.6-fast-xhigh": "gpt-5.6-luna",
    "claude-opus-5-thinking-xhigh": "gpt-5.5",
    "@cursor-skill/poteto-mode-tools": "@codex-skill/poteto-mode-tools",
    "~/.cursor/rules/pstack-models.mdc": "`.codex/pstack-models.json` or `~/.codex/pstack-models.json`",
    "the pstack Codex model configuration": "`.codex/pstack-models.json` or `~/.codex/pstack-models.json`",
    ".cursor/skills/": ".codex/skills/",
    "Cursor's built-in `create-skill` skill": "Codex's `$skill-creator` skill",
    "Cursor's built-in create-skill skill": "Codex's `$skill-creator` skill",
    "`create-skill`": "`$skill-creator`",
    "`subagent_type: generalPurpose`": "a unique `task_name`",
    "`subagent_type: \"poteto-agent\"`": "a brief that explicitly invokes `$poteto-agent`",
    "`subagent_type: \"Comment Sicko\"`": "a brief that explicitly invokes `$comment-sicko`",
    "`run_in_background: true`": "a non-blocking `spawn_agent` call",
    "`readonly: true`": "a read-only brief",
    "`readonly: false`": "an agent-mode brief",
    "`environment: \"cloud\"`": "the shared Codex workspace",
    "`environment: \"local\"`": "the shared Codex workspace",
    "`cloud_base_branch`": "the prepared worktree branch",
    "the Task tool": "Codex collaboration tools",
    "single Task subagent": "single Codex sub-agent",
    "Task subagent": "Codex sub-agent",
    "`Task` response body": "sub-agent's final response",
    "`Task` subagent": "Codex sub-agent",
    "`Task` call": "`spawn_agent` call",
    "`Task` calls": "`spawn_agent` calls",
    "Cursor cloud agent": "Codex sub-agent",
    "Cursor cloud agents": "Codex sub-agents",
    "cloud agent": "Codex sub-agent",
    "cloud agents": "Codex sub-agents",
    "- `subagent_type`: `generalPurpose`": "- `task_name`: a short unique identifier",
    "- `readonly`: `true`": "- Brief: read-only analysis; do not modify files or external state",
    "- `readonly`: `false` (agent mode).": "- Brief: may use available read-only MCPs but must not write external state.",
    "readonly strips MCPs": "the brief must explicitly allow relevant read-only MCP lookups",
    "Readonly/Ask mode strips MCPs and defeats that.": "The brief must explicitly allow relevant read-only MCP lookups.",
    "from the Cursor environment": "from the current Codex host",
    "the `mcps/` directory Cursor exposes for enabled MCP servers": "the available MCP tool list",
    "Cursor's `/loop` command": "a Codex heartbeat automation",
    "cursor's `/loop` command": "a Codex heartbeat automation",
    "`/loop`": "a Codex heartbeat automation",
}

RUNTIME_MARKERS = (
    "subagent",
    "spawn_agent",
    "heartbeat",
    "model configuration",
    ".codex/",
    "Codex collaboration",
)


def split_frontmatter(text: str) -> tuple[list[str], str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("unterminated YAML frontmatter") from exc
    return lines[1:end], "\n".join(lines[end + 1 :]).lstrip("\n")


def normalize_skill(skill_file: Path) -> None:
    original = skill_file.read_text()
    header, body = split_frontmatter(original)
    policy_file = skill_file.parent / "agents" / "openai.yaml"
    explicit_only = policy_file.exists() or any(
        line.strip() == "disable-model-invocation: true" for line in header
    )
    skill_name = skill_file.parent.name

    normalized: list[str] = []
    for line in header:
        key = line.split(":", 1)[0].strip() if ":" in line else ""
        if key in UNSUPPORTED_FRONTMATTER:
            continue
        if key == "name":
            normalized.append(f"name: {skill_name}")
        else:
            normalized.append(line)

    for old, new in TEXT_REPLACEMENTS.items():
        body = body.replace(old, new)

    for name in sorted(path.parent.name for path in SKILLS.glob("*/SKILL.md")):
        body = body.replace(f"`/{name}", f"`${name}")
        body = re.sub(rf"(?<![.\w])/{re.escape(name)}(?=\s|$)", f"${name}", body)

    adapter = (
        "[Codex runtime adapter](../poteto-mode/references/codex-adapter.md)"
        if skill_name != "poteto-mode"
        else "[Codex runtime adapter](references/codex-adapter.md)"
    )
    if any(marker in body for marker in RUNTIME_MARKERS) and "Codex runtime adapter" not in body:
        body = (
            f"> Codex port: read the {adapter} before using delegation, model "
            "routing, monitoring, transcripts, or product-specific paths.\n\n"
            + body
        )

    skill_file.write_text("---\n" + "\n".join(normalized) + "\n---\n\n" + body + "\n")

    if explicit_only:
        policy_file.parent.mkdir(parents=True, exist_ok=True)
        write_openai_yaml(policy_file, skill_name)


def write_openai_yaml(path: Path, skill_name: str) -> None:
    display_name = skill_name.replace("-", " ").title()
    short_description = f"Run the {display_name} pstack workflow in Codex."
    default_prompt = f"Use ${skill_name} for this request."
    path.write_text(
        "interface:\n"
        f"  display_name: {json.dumps(display_name)}\n"
        f"  short_description: {json.dumps(short_description)}\n"
        f"  default_prompt: {json.dumps(default_prompt)}\n"
        "policy:\n"
        "  allow_implicit_invocation: false\n"
    )


def convert_named_agent(source: Path, skill_name: str, description: str) -> None:
    _, body = split_frontmatter(source.read_text())
    body = body.replace("`poteto-mode`", "`$poteto-mode`")
    target = SKILLS / skill_name / "SKILL.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "---\n"
        f"name: {skill_name}\n"
        f"description: \"{description}\"\n"
        "---\n\n"
        "> Codex port: this skill replaces pstack's Cursor-only named sub-agent. "
        "Invoke it explicitly in the brief sent to a Codex sub-agent.\n\n"
        + body
        + "\n"
    )
    policy = target.parent / "agents" / "openai.yaml"
    policy.parent.mkdir(parents=True, exist_ok=True)
    write_openai_yaml(policy, skill_name)


def rewrite_text_files() -> None:
    allowed = {".md", ".json", ".mjs", ".ts", ".tsx", ".sh", ".yaml", ".yml"}
    for path in PLUGIN.rglob("*"):
        if not path.is_file() or path.suffix not in allowed or path.name == "SKILL.md":
            continue
        text = path.read_text(errors="strict")
        changed = text
        for old, new in TEXT_REPLACEMENTS.items():
            changed = changed.replace(old, new)
        for name in sorted(p.parent.name for p in SKILLS.glob("*/SKILL.md")):
            changed = changed.replace(f"`/{name}", f"`${name}")
            changed = re.sub(rf"(?<![.\w])/{re.escape(name)}(?=\s|$)", f"${name}", changed)
        if changed != text:
            path.write_text(changed)


def main() -> None:
    convert_named_agent(
        PLUGIN / "agents" / "poteto-agent.md",
        "poteto-agent",
        "Apply the full pstack engineering style inside an explicitly delegated Codex subtask.",
    )
    convert_named_agent(
        PLUGIN / "agents" / "comment-sicko.md",
        "comment-sicko",
        "Perform a read-only, deletion-biased audit of comments and suppression directives.",
    )
    for skill_file in sorted(SKILLS.glob("*/SKILL.md")):
        normalize_skill(skill_file)
    rewrite_text_files()


if __name__ == "__main__":
    main()
