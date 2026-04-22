# AO Worker Failure Investigation — 2026-04-21

## Summary

Investigation of worldarchitect AO workers on PRs `#6420` and `#6404` found that the failure was not primarily PR complexity. It was a combined orchestrator and worker-lifecycle failure:

1. at least one supposed Codex worker was actually launched as `claude-code`
2. killed sessions accumulated high SCM failure counts
3. AO repeatedly nudged stuck workers instead of failing closed quickly
4. paper ownership diverged from actual worker activity
5. overlapping reassignments created supervision churn instead of continuity

## Primary evidence

- AO lifecycle log:
  - `/Users/jleechan/.agent-orchestrator/953501c04ccc-worldarchitect.ai/lifecycle-worker.log`
- AO session archives:
  - `/Users/jleechan/.agent-orchestrator/953501c04ccc-worldarchitect.ai/sessions/archive/wa-1417_2026-04-21T22-00-57-952Z`
  - `/Users/jleechan/.agent-orchestrator/953501c04ccc-worldarchitect.ai/sessions/archive/wa-1419_2026-04-21T22-25-23-944Z`
  - `/Users/jleechan/.agent-orchestrator/953501c04ccc-worldarchitect.ai/sessions/archive/wa-1427_2026-04-21T22-40-24-213Z`
  - `/Users/jleechan/.agent-orchestrator/953501c04ccc-worldarchitect.ai/sessions/archive/wa-1428_2026-04-21T22-41-15-707Z`
  - `/Users/jleechan/.agent-orchestrator/953501c04ccc-worldarchitect.ai/sessions/archive/wa-1428_2026-04-21T22-41-53-847Z`
- Sparse worker transcript evidence:
  - `/Users/jleechan/.codex/sessions/2026/04/21/rollout-2026-04-21T15-15-28-019db21c-d852-7b41-ad97-ce3561a11919.jsonl`
  - `/Users/jleechan/.codex/sessions/2026/04/21/rollout-2026-04-21T15-33-30-019db22d-4e20-7443-803f-3ba6d9bce015.jsonl`
  - `/Users/jleechan/.claude/projects/-Users-jleechan--worktrees-worldarchitect-wa-1419/43d3a498-2e98-4707-89cc-9796c0c90fc0.jsonl`

## Findings

### `wa-1419` on PR `#6404`

- archived as `agent=claude-code`, not Codex
- launch command used `claude` with `MiniMax-M2.7`
- later AO recorded repeated stuck probes with reason `agent waiting for user feedback or permission`
- then AO killed it

Interpretation: this lane had both launch-fidelity failure and stuck-state handling failure.

### `wa-1417` on PR `#6420`

- archived as `status=killed`
- `scmFailureCount=280`
- AO lifecycle recorded `exitStatus:"killed"`
- sparse history shows the worker was also doing `#6431`-related work before a bad retask landed in shell

Interpretation: this lane had ownership drift plus heavy SCM churn, ending in kill.

### `wa-1427` and `wa-1428` on PR `#6404`

- `wa-1427` appears to have been a real Codex launch and was archived `status=pr_open`
- `wa-1428` was archived `working` and then almost immediately `killed`

Interpretation: AO started recycling ownership on the same PR instead of preserving a single healthy worker.

## Root cause

The real failure was a stack:

1. wrong agent launched at least once
2. session-health truth was weak
3. stuck sessions were nudged instead of failing closed
4. archive ownership drifted away from actual execution
5. overlapping reassignment created churn

## Operational lesson

AO supervision for this queue must fail closed on three things:

1. wrong agent type after spawn
2. repeated stuck-probe “waiting for feedback/permission”
3. PR ownership mismatch between archive metadata and actual worker transcript/worktree activity
