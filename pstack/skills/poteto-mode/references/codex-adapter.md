# Codex runtime adapter

Read this reference when a pstack workflow delegates work, selects models, monitors a long-running operation, reads conversation history, or mentions Cursor-specific files and commands.

## Skill invocation

Invoke skills as `$skill-name` in Codex. Slash-prefixed names in retained upstream examples are legacy Cursor syntax.

## Plans and goals

Maintain a concise checklist in commentary when the workflow asks for a todo list. Use Codex's durable goal mechanism only when the user explicitly asks for a goal or long-running objective. A pstack playbook does not create that authorization by itself.

## Delegation

Use Codex collaboration tools for subtasks in the current request:

- `spawn_agent` starts a bounded subtask and returns immediately.
- `wait_agent` waits for mailbox updates. Prefer a long bounded wait over frequent polling.
- `send_message` adds context without restarting an agent.
- `followup_task` starts another turn only after an agent is idle.
- `interrupt_agent` stops work that is no longer useful.

Codex sub-agents share the current filesystem. Give concurrent writers separate git worktrees or unique output paths before spawning them. If a workflow asks for the former `poteto-agent` or `Comment Sicko` type, tell the sub-agent to explicitly use `$poteto-agent` or `$comment-sicko` in its brief.

Do not create a separate user-visible Codex task for an internal subtask. Create or fork a task only when the user explicitly requests that product action.

## Model routing

Load the first existing configuration in this order:

1. `<workspace>/.codex/pstack-models.json`
2. `~/.codex/pstack-models.json`

The value for a role is either `{ "model": "...", "reasoning_effort": "..." }`, a list of those objects for panels, or `{ "inherit_parent": true }`. Pass a model override only when the current host exposes that exact model and effort. Otherwise omit the override and inherit the parent model.

Portable defaults, subject to current host availability:

- High-judgment work: `gpt-5.6-sol`, reasoning `high` or `max`.
- Balanced implementation and review: `gpt-5.6-terra`, reasoning `high`.
- Fast mechanical work: `gpt-5.6-luna`, reasoning `medium` or `high`.
- Economical review lanes: `gpt-5.4-mini`, reasoning `high`.

Model diversity is useful but optional. A workflow must still run when only the parent model is available.

## Monitoring and unattended work

Wait on active sub-agents with `wait_agent`. When the user explicitly asks for recurring monitoring or a future follow-up, create a Codex heartbeat automation and keep it quiet until a meaningful change, completion, failure, or required user action. Do not emit raw scheduling directives or recreate a Codex heartbeat automation.

## Conversation history

Prefer the current task's visible history and thread tools when available. Do not scan broad transcript directories or unrelated tasks. If no transcript API is available, write a compact digest from the current conversation and use that as the review input.

## Paths and optional dependencies

Use `.codex/` for project-local Codex configuration and skills. Treat retained `.cursor/` paths as upstream examples unless a compatibility note explicitly maps them. Skills from `cursor-team-kit`, Origin, Bugbot, or other external products are optional. Use an available equivalent, skip the optional step with a clear reason, or report the dependency gap; never pretend the dependency exists.
