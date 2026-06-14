---
name: ""
metadata: 
  node_type: memory
  type: feedback
  date: 2026-06-05
  tags: 
    - ao-config
    - backfillAllPRs
    - spawn-storm
    - test-repos
    - mctrl-test
  originSessionId: 8dfc5e2f-2a26-4883-b6e0-f4e4556ad19b
---

# Test/harness repos MUST set `backfillAllPRs: false`

## Rule

Any project in AO config that is a test harness / not a production codebase MUST have `backfillAllPRs: false` explicitly set.

`backfillAllPRs` defaults to `true` — if not set, the lifecycle-worker will continuously spawn a new worker for every open PR on every ao-health tick.

## Why

`mctrl_test` had 30+ open PRs (merge-train test PRs, most already merged in spirit). With `backfillAllPRs` unset (defaulting to `true`):
- Lifecycle-worker spawned 19+ Gemini (`mt-*`) workers every 5 minutes
- Workers hit Gemini quota (RESOURCE_EXHAUSTED 429) and stalled
- Stalled workers reported no completion back to lifecycle-worker
- Lifecycle-worker respawned on each ao-health tick (every 300s)
- System load reached 104+; DNS became starved

## Impact of the storm

- 19 stalled sessions had to be manually killed via `ao stop`
- 12 "MERGEABLE" PRs were already merged by earlier workers
- 10 conflicting (merge-train test) PRs remain open, require manual close

## Fix

```yaml
# ~/.hermes/agent-orchestrator.yaml
projects:
  mctrl-test:
    backfillAllPRs: false   # ← add this for test/harness repos
```

## How to apply

When adding a new project to AO config:
- Set `backfillAllPRs: false` unless it is an active production repo that should drive ALL open PRs to green
- Test repos, proof-of-concept repos, merge-train harnesses → always `false`
- Production repos with active PRs (agent-orchestrator, worldarchitect.ai) → can leave unset (true)

## Spawn storm diagnostic

If `ao list` shows many sessions for a single project:
```bash
ao list | grep mt-   # or the project prefix
```
If count > 5 and project is a test harness → kill all + add `backfillAllPRs: false`

## See also

- `project_2026-06-05_skeptic_chain_fixed.md` — session context
- `feedback_2026-04-25_ao_spawn_gate_session_count.md` — spawn gate session count enforcement (AO hard cap 20 workers)
