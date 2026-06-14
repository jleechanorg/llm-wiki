---
name: ""
metadata: 
  node_type: memory
  type: project
  date: 2026-06-05
  tags: 
    - skeptic
    - ao-config
    - chain-fix
    - agent-orchestrator
  originSessionId: 8dfc5e2f-2a26-4883-b6e0-f4e4556ad19b
---

# Skeptic chain agent-orchestrator fixed — 2026-06-05

## Fact

Skeptic chain for `agent-orchestrator` was silently broken. Fixed 2026-06-05 via two config changes in `~/.hermes/agent-orchestrator.yaml`.

## Root cause — two independent bugs

### Bug 1: Wrong reaction action

```yaml
reactions:
  worker-signals-completion:
    action: notify   # ← WRONG — fires but only calls notifyHuman()
```

Fixed to:
```yaml
reactions:
  worker-signals-completion:
    action: skeptic-review   # ← CORRECT — reads skepticModel + skepticPostComment
```

The `skepticModel`, `skepticPostComment`, and `skepticPrompt` keys are only processed by the `skeptic-review` action handler. `notify` silently discards the skeptic trigger.

### Bug 2: Missing SCM config

`projects.agent-orchestrator` had no `scm` stanza. `skeptic-cron-local.ts:153` (guard: `if (!project.scm?.plugin)`) returned silently with no PRs evaluated.

Fixed by adding:
```yaml
projects:
  agent-orchestrator:
    scm:
      plugin: github
```

## How to verify skeptic is working

```bash
# Manual trigger (dry run)
ao skeptic verify -n <PR_NUMBER> --dry-run

# Check for VERDICT comment on PR
gh api repos/jleechanorg/agent-orchestrator/issues/<N>/comments \
  --jq '.[] | select(.body | contains("skeptic-agent-verdict")) | .body' | head -5
```

## If skeptic stops auto-running again

Check these two fields first:
1. `grep -A5 "worker-signals-completion" ~/.hermes/agent-orchestrator.yaml` → must be `action: skeptic-review`
2. `grep -A5 "agent-orchestrator:" ~/.hermes/agent-orchestrator.yaml | grep scm` → must have `scm: plugin: github`

Both must be present for auto-skeptic to work. If either is missing/wrong, skeptic silently does nothing — no error, no log entry.

## Session state at fix time

- PRs #641, #633, #652, #653 all MERGED
- No open PRs in agent-orchestrator
- mctrl_test spawn storm also mitigated (see `feedback_2026-06-05_backfillallprs_test_repos.md`)

## See also

- `feedback_2026-06-05_skeptic_reaction_action_notify.md` — reaction action detail
- `feedback_2026-05-04_worldarchitect_skeptic_missing_scm.md` — SCM config pattern (worldarchitect precedent)
- `feedback_skeptic_no_api_keys_in_ci.md` — architectural decision: skeptic runs local, not GHA
