---
name: reflect
description: Spawn three parallel reviewers over the current task history, surface durable learnings, and propose concrete skill edits. Use when the user explicitly says reflect or invokes $reflect.
---

> Cross-agent runtime: read the [Universal runtime adapter](../poteto-mode/references/universal-runtime-adapter.md) or your platform adapter under  before using delegation, model routing, sub-agents, or platform-specific paths.

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

- The user said "reflect" or invoked `$reflect`.
- A complex task (5+ tool calls) just landed cleanly and the recipe is worth keeping.
- The agent hit dead ends, found the working path, and the path generalizes.
- The user corrected the agent's approach mid-task.
- A non-trivial workflow emerged that isn't captured anywhere.

Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Capture the current task history

Use the current visible conversation and runtime conversation history tools when available. Do not scan filesystem transcript directories or unrelated tasks. If the complete history is not accessible, write a tight digest containing the user's goal, decisions, evidence, failed paths, corrections, and final artifacts.

### 2. Spawn three reviewers in parallel

Dispatch three `spawn_agent` calls with unique `task_name` values. Each brief is read-only and may use relevant read-only MCP lookups. The parent applies any approved edits.

| Lens | `model` | Prompt template |
|---|---|---|
| Judgment | your configured reflect-judgment model (default `gpt-5.6-sol`) | `references/judgment-reviewer.md` |
| Tooling | your configured reflect-tooling model (default `gpt-5.6-sol`) | `references/tooling-reviewer.md` |
| Divergent | your configured reflect-judgment model (default `gpt-5.6-sol`) | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the task history or digest where marked. Reviewers return findings in their final responses.

### 3. Synthesize

Use one `spawn_agent` call with a unique `task_name` and the configured `reflect-judgment` route when available. The synthesizer may use read-only MCP lookups to spot-check citations. Use `references/synthesizer.md` verbatim with each reviewer's output inlined. It returns Accepted / Rejected / Backlog proposals.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. The synthesizer already applies this criterion; this is a final pass before edits land. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org; do not auto-apply.

Do not file Backlog items or mutate an external tracker unless the user explicitly authorizes that write.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the `$skill-creator` skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `$skill-creator` and run its description-optimization loop.
- `new skill via create-skill: <kebab-name>`: hand creation to `$skill-creator`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
