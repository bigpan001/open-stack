#!/usr/bin/env python3
"""Cross-platform installer for pstack universal skill suite.

Supported targets: codex, cursor, pi, opencode, kimi, zcode.
"""

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_SRC = ROOT / "pstack" / "skills"
ADAPTERS_SRC = ROOT / "pstack" / "adapters"

TARGET_PATHS = {
    "codex": Path.home() / ".codex" / "plugins" / "cache" / "open-stack-local" / "pstack" / "0.14.7+codex.1",
    "cursor": Path.home() / ".cursor" / "skills",
    "pi": Path.home() / ".pi" / "skills",
    "opencode": Path.home() / ".opencode" / "skills",
    "kimi": Path.home() / ".kimi" / "skills",
    "zcode": Path.home() / ".zcode" / "skills",
}


def install(target: str, dest_override: str | None = None, dry_run: bool = False) -> None:
    target = target.lower()
    if target not in TARGET_PATHS:
        print(f"Error: Unknown target '{target}'. Choose from: {', '.join(TARGET_PATHS.keys())}")
        sys.exit(1)

    dest = Path(dest_override) if dest_override else TARGET_PATHS[target]
    if dry_run:
        print(f"[dry-run] Target: {target}, Path: {dest}")
        return
    dest.mkdir(parents=True, exist_ok=True)
    print(f"Installing pstack universal skills to {target} at: {dest}")

    if target == "codex":
        # Codex installs the whole plugin bundle
        plugin_root = ROOT / "pstack"
        for item in plugin_root.iterdir():
            target_path = dest / item.name
            if item.is_dir():
                if target_path.exists():
                    shutil.rmtree(target_path)
                shutil.copytree(item, target_path)
            else:
                shutil.copy2(item, target_path)
    else:
        # Copy universal skills
        for skill_dir in SKILLS_SRC.iterdir():
            if skill_dir.is_dir():
                target_skill = dest / skill_dir.name
                if target_skill.exists():
                    shutil.rmtree(target_skill)
                shutil.copytree(skill_dir, target_skill)

        # Copy target adapter documentation & configuration if present
        adapter_src = ADAPTERS_SRC / target
        if adapter_src.exists():
            target_adapter_dest = dest / ".adapter"
            target_adapter_dest.mkdir(parents=True, exist_ok=True)
            for item in adapter_src.iterdir():
                shutil.copy2(item, target_adapter_dest / item.name)

    print(f"Successfully installed pstack for {target}!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install pstack across Agent runtimes.")
    parser.add_argument("target", choices=["codex", "cursor", "pi", "opencode", "kimi", "zcode", "all"], help="Target agent platform")
    parser.add_argument("--dest", help="Custom destination path")
    parser.add_argument("--dry-run", action="store_true", help="Simulate installation without copying files")
    args = parser.parse_args()

    if args.target == "all":
        for t in ["codex", "cursor", "pi", "opencode", "kimi", "zcode"]:
            install(t, args.dest, args.dry_run)
    else:
        install(args.target, args.dest, args.dry_run)
