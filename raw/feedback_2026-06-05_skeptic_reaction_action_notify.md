---
name: ""
metadata: 
  node_type: memory
  type: feedback
  date: 2026-06-05
  tags: 
    - skeptic
    - ao-config
    - reactions
    - silent-failure
  originSessionId: 8dfc5e2f-2a26-4883-b6e0-f4e4556ad19b
---

# Skeptic reaction action must be `skeptic-review`, not `notify`

## Rule

`worker-signals-completion` reaction action must be `action: skeptic-review`, not `action: notify`.

`action: notify` fires on every PR state transition but only calls `notifyHuman()` — the `skepticModel`, `skepticPostComment`, and `skepticPrompt` config fields are only read by the `skeptic-review` case in the reactions handler. Using `notify` silently discards the skeptic trigger.

## Why

This bug silently disabled automatic skeptic evaluation for `agent-orchestrator` for an unknown period. Every PR completed without triggering auto-skeptic. The bug was invisible because:
- `ao skeptic verify -n N` (manual) still worked
- No error or warning was logged
- The lifecycle-worker log showed `reaction fired: worker-signals-completion` correctly — but the wrong action ran

## Root location

`~/.hermes/agent-orchestrator.yaml`:
```yaml
reactions:
  worker-signals-completion:
    action: skeptic-review   # ← must be this, NOT "notify"
    skepticModel: claude-opus-4-5
    skepticPostComment: true
```

## How to apply

When skeptic is not auto-running on new PRs, check `reactions.worker-signals-completion.action` in `~/.hermes/agent-orchestrator.yaml` **first** before deeper investigation.

Diagnostic chain:
1. `grep -A5 "worker-signals-completion" ~/.hermes/agent-orchestrator.yaml` — verify `action: skeptic-review`
2. `grep -A3 "agent-orchestrator:" ~/.hermes/agent-orchestrator.yaml | grep scm` — verify `scm: plugin: github` present (missing SCM causes silent return at `skeptic-cron-local.ts:153`)
3. Only if both are correct: check lifecycle-worker logs for dispatch errors

## See also

- `project_2026-06-05_skeptic_chain_fixed.md` — full session context
- `feedback_2026-05-04_worldarchitect_skeptic_missing_scm.md` — SCM config silent failure pattern
