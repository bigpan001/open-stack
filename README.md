# Install pstack for your agent

This repository packages pstack for Codex, Cursor, Pi, OpenCode, Kimi, and ZCode. Use the installer from the repository root. It copies the portable skills and the adapter files for the runtime you choose.

## Install one runtime

Clone the repository, then run the installer with your runtime name.

```bash
git clone https://github.com/bigpan001/open-stack.git
cd open-stack
python scripts/install.py codex
```

Replace `codex` with `cursor`, `pi`, `opencode`, `kimi`, or `zcode` for another runtime. The installer prints `Successfully installed pstack for <runtime>!` when it finishes.

To inspect the destination before copying files, add `--dry-run`.

```bash
python scripts/install.py codex --dry-run
```

To install every supported runtime that is available on your machine, run:

```bash
python scripts/install.py all
```

## Choose a custom destination

Use `--dest` when your agent reads skills from a non-default directory.

```bash
python scripts/install.py opencode --dest /path/to/skills
```

The installer replaces existing pstack skill folders in the selected destination. Run the dry run first when you point it at a shared directory.

## Start using pstack

Start a new agent task after installation so it discovers the copied skills. Begin a task with `$poteto-mode`.

```text
$poteto-mode add a --json flag to this command. Keep text output byte-identical. Verify both paths.
```

In Codex, you can also install the personal marketplace package with `codex plugin add pstack@personal`. Use the repository installer when you need the latest checked-out version or a non-Codex runtime.

## Verify the installation

Run the dry run again to confirm the selected runtime and destination. Then start a new task and invoke `$poteto-mode`. If the agent recognizes the skill, the installation is ready.

For the full workflow guide, read [pstack/docs/guide/README.md](pstack/docs/guide/README.md). The packaged skills live in [pstack/skills](pstack/skills).
