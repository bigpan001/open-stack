# pstack to Codex migration plan

Upstream: <https://github.com/cursor/plugins/tree/main/pstack>

| Phase | Deliverable | Verification | Status |
|---|---|---|---|
| 1. Import | Preserve the upstream pstack source and record its commit | File inventory and upstream SHA match | Complete |
| 2. Package | Add a valid `.codex-plugin/plugin.json` and retain license/assets | Codex plugin validator passes | Complete |
| 3. Runtime port | Normalize skill frontmatter, convert named agents to skills, map delegation/models/monitoring to Codex | Every `SKILL.md` passes validation; no active skill depends on Cursor-only runtime fields | Complete |
| 4. Regression checks | Run shipped script tests and port-specific static checks | 52 upstream tests, TypeScript, entrypoint, schema, and compatibility checks pass | Complete |
| 5. Personal install | Publish the validated package to the personal marketplace and install it | `codex plugin list` reports `pstack@personal` enabled and the installed cache contains 47 skills | Complete |

The dormant Benny automation pack remains as upstream reference material. It is not registered as a Codex automation because its webhook and runtime contracts are Cursor-specific.

Start a new Codex task after installation to pick up the newly installed skills. Use `$poteto-mode` as the main entry point and `$setup-pstack` only when explicit per-role model routing is wanted.
