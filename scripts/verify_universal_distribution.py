#!/usr/bin/env python3
"""Static compatibility and universal cross-agent distribution checks."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "pstack"
SKILLS = PLUGIN / "skills"
ADAPTERS = PLUGIN / "adapters"

LEGACY_MARKERS = {
    "disable-model-invocation": "Cursor-only skill frontmatter",
    "subagent_type": "Cursor-only named-agent field",
    "run_in_background": "Cursor-only Task field",
    "~/.cursor": "Cursor personal path in universal skill",
    "agent-transcripts": "Cursor transcript layout",
    "`/loop`": "Cursor loop command",
    "AskQuestion": "Cursor question tool",
    "claude-fable-5-1-thinking-max": "unavailable model slug",
    "grok-4.6-fast-xhigh": "unavailable model slug",
    "gpt-5.6-sol-max": "invalid combined model and effort slug",
}

SUPPORTED_PLATFORMS = ["codex", "cursor", "pi", "opencode", "kimi", "zcode"]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


# 1. Manifest checks
manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
if manifest.get("name") != "pstack":
    fail("manifest name must be pstack")
if manifest.get("skills") != "./skills/":
    fail("manifest must expose ./skills/")

# 2. Universal skill structure checks
skill_files = sorted(SKILLS.glob("*/SKILL.md"))
if len(skill_files) < 47:
    fail(f"expected at least 47 skills, found {len(skill_files)}")

for skill_file in skill_files:
    text = skill_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        fail(f"{skill_file}: invalid frontmatter boundaries")
    end = lines.index("---", 1)
    name_lines = [line for line in lines[1:end] if line.startswith("name:")]
    if name_lines != [f"name: {skill_file.parent.name}"]:
        fail(f"{skill_file}: name must match its directory")

for path in sorted(SKILLS.rglob("*.md")):
    text = path.read_text(encoding="utf-8")
    for marker, reason in LEGACY_MARKERS.items():
        if marker in text:
            fail(f"{path}: {reason}: {marker}")

for required in ("poteto-mode", "poteto-agent", "comment-sicko", "setup-pstack"):
    if not (SKILLS / required / "SKILL.md").is_file():
        fail(f"missing required skill {required}")

# 3. Platform adapter layer checks
if not ADAPTERS.is_dir():
    fail("missing adapters directory")

for platform in SUPPORTED_PLATFORMS:
    adapter_dir = ADAPTERS / platform
    if not adapter_dir.is_dir():
        fail(f"missing adapter directory for platform: {platform}")
    adapter_doc = adapter_dir / "adapter.md"
    if not adapter_doc.is_file():
        fail(f"missing adapter.md for platform: {platform}")

# 4. Universal matrix check
matrix_doc = SKILLS / "poteto-mode" / "references" / "universal-runtime-adapter.md"
if not matrix_doc.is_file():
    fail("missing universal-runtime-adapter.md in poteto-mode")

print(f"Universal distribution checks passed: {len(skill_files)} core skills, 6 platform adapters verified.")

