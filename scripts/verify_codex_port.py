#!/usr/bin/env python3
"""Static compatibility checks that do not require Codex's Python dependencies."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "pstack"
SKILLS = PLUGIN / "skills"

LEGACY_MARKERS = {
    "disable-model-invocation": "Cursor-only skill frontmatter",
    "subagent_type": "Cursor-only named-agent field",
    "run_in_background": "Cursor-only Task field",
    "~/.cursor": "Cursor personal path",
    "agent-transcripts": "Cursor transcript layout",
    "`/loop`": "Cursor loop command",
    "AskQuestion": "Cursor question tool",
    "claude-fable-5-1-thinking-max": "unavailable Cursor model",
    "grok-4.6-fast-xhigh": "unavailable Cursor model",
    "gpt-5.6-sol-max": "invalid combined model and effort slug",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
if manifest.get("name") != "pstack":
    fail("manifest name must be pstack")
if manifest.get("skills") != "./skills/":
    fail("manifest must expose ./skills/")

skill_files = sorted(SKILLS.glob("*/SKILL.md"))
if len(skill_files) < 47:
    fail(f"expected at least 47 skills, found {len(skill_files)}")

for skill_file in skill_files:
    text = skill_file.read_text()
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        fail(f"{skill_file}: invalid frontmatter boundaries")
    end = lines.index("---", 1)
    name_lines = [line for line in lines[1:end] if line.startswith("name:")]
    if name_lines != [f"name: {skill_file.parent.name}"]:
        fail(f"{skill_file}: name must match its directory")

for path in sorted(SKILLS.rglob("*.md")):
    text = path.read_text()
    for marker, reason in LEGACY_MARKERS.items():
        if marker in text:
            fail(f"{path}: {reason}: {marker}")

for required in ("poteto-mode", "poteto-agent", "comment-sicko", "setup-pstack"):
    if not (SKILLS / required / "SKILL.md").is_file():
        fail(f"missing required skill {required}")

for entrypoint in (
    SKILLS / "poteto-mode" / "scripts" / "orch" / "orch.ts",
    SKILLS / "poteto-mode" / "scripts" / "watch-pr" / "watch-pr",
):
    first = entrypoint.read_text().splitlines()[0]
    if "node --experimental-transform-types" not in first:
        fail(f"{entrypoint}: expected Node TypeScript shebang")

print(f"Codex port static checks passed: {len(skill_files)} skills")
