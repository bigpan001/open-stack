---
name: setup-pstack
description: Configure the runtime models, platform adapters, and reasoning efforts pstack uses per role across Codex, Cursor, Pi, OpenCode, Kimi, and ZCode. Use for $setup-pstack, "configure pstack models", or setting platform adapters.
---

# Setup pstack for Universal Agent Runtimes

Read the [Universal runtime adapter](../poteto-mode/references/universal-runtime-adapter.md) and platform adapters under `adapters/<platform>/` before changing model or adapter configuration.

Configure only models that the current Codex host exposes. A missing configuration is valid; all pstack workflows can inherit the parent model.

## Configuration location

Use `<workspace>/.codex/pstack-models.json` by default so the repository can carry its own routing choices. Write `~/.codex/pstack-models.json` only when the user explicitly asks for a personal configuration that applies across projects.

Load project configuration first and personal configuration second. Project values override matching personal values.

## Workflow

1. Read the available model names and supported reasoning efforts from the current Codex tool schema or model selector. Do not invent slugs.
2. Router/custom prefix awareness: router models (such as `lo/*`, e.g. `lo/gemini-3.8-flash-high`, `lo/claude-opus-4.6`) and native models configured in the environment are supported as valid targets for sub-agents via `spawn_agent`.
3. Load existing project and personal configuration when present.
4. Show the effective mapping. Ask for choices only when the user requested interactive selection or an existing slug is unavailable.
5. Validate every explicit model and reasoning effort against the current host or router definitions. Use `{ "inherit_parent": true }` when no override is needed.
5. Write valid JSON atomically. Preserve unrelated keys so future pstack versions can add roles without losing user settings.
6. Re-read the file, report the effective mapping, and tell the user that a new Codex task is the safest place to test updated skill behavior.

## Schema

Each scalar role maps to one route object. Panel roles map to a non-empty array of route objects.

```json
{
  "schema_version": 1,
  "roles": {
    "feature": { "model": "gpt-5.6-terra", "reasoning_effort": "high" },
    "refactoring": { "model": "gpt-5.6-terra", "reasoning_effort": "high" },
    "bug-fix": { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
    "perf-issue": { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
    "hillclimb": { "model": "gpt-5.6-sol", "reasoning_effort": "max" },
    "judgment-and-prose": { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
    "hardest-tasks": { "model": "gpt-5.6-sol", "reasoning_effort": "max" },
    "how-explorer": { "model": "gpt-5.6-luna", "reasoning_effort": "high" },
    "how-explainer": { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
    "why-investigator": { "model": "gpt-5.6-terra", "reasoning_effort": "high" },
    "why-synthesizer": { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
    "reflect-tooling": { "model": "gpt-5.6-terra", "reasoning_effort": "high" },
    "reflect-judgment": { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
    "swarm-workers": { "model": "gpt-5.6-luna", "reasoning_effort": "high" },
    "how-critics": [
      { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
      { "model": "gpt-5.6-terra", "reasoning_effort": "high" },
      { "model": "gpt-5.4-mini", "reasoning_effort": "high" }
    ],
    "arena-runners": [
      { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
      { "model": "gpt-5.6-terra", "reasoning_effort": "high" },
      { "model": "gpt-5.6-luna", "reasoning_effort": "high" }
    ],
    "arena-cross-judge-pool": [
      { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
      { "model": "gpt-5.4-mini", "reasoning_effort": "high" }
    ],
    "architect-runners": [
      { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
      { "model": "gpt-5.6-terra", "reasoning_effort": "high" }
    ],
    "interrogate-reviewers": [
      { "model": "gpt-5.6-sol", "reasoning_effort": "high" },
      { "model": "gpt-5.6-terra", "reasoning_effort": "high" },
      { "model": "gpt-5.4-mini", "reasoning_effort": "high" }
    ]
  }
}
```

The example is a portable starting point, not an entitlement claim. Remove or replace any route not exposed by the current host. A panel may contain repeated models when only one suitable model is available.

After setup, offer `$create-verification-skill` once when the project lacks a real user-path verification harness.
