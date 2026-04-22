---
title: "AO Worker Failure Investigation — 2026-04-21"
type: source
tags: [ao-worker, lifecycle-manager, scm-github, worldarchitect-ai, dead-shell]
date: 2026-04-21
---

## Summary

AO workers on worldarchitect.ai ZFC PRs were found to be dying from GitHub API failure storms, not mystery crashes. The reaper kills sessions after `scmFailureCount >= 3` while `agentDead=true`. The tmux pane stays alive, causing subsequent retask text to be interpreted as bash commands (`-bash: Refresh: command not found`). Root cause is persistent 401 auth failures on the worldarchitect project SCM, not rate limiting.

## Key Findings

### Death cause confirmed: SCM failure storm

Workers are killed by the reaper after accumulating consecutive GitHub API failures. Session archives show:

| Worker | Runtime | Target PR | scmFailureCount | killConfirmed |
|--------|---------|-----------|-----------------|--------------|
| wa-1417 | Codex | #6420 | **280** | true |
| wa-1418 | Claude | #6429 | 66 | true |
| wa-1419 | Claude | #6404 | 66 | true |
| wa-1422 | Claude | #6402 | 64 | true |
| wa-1424 | Claude | #6418 | 57 | true |
| wa-1423 | Claude | #6434 | 34 | true |
| wa-1425 | Claude | #6420 | 3 | true |
| wa-1426 | Codex | #6420 | 6 | true |

### SCM_FAILURE_THRESHOLD = 3 (hardcoded)

Location: `packages/core/src/lifecycle-manager.ts` line 597

```typescript
const SCM_FAILURE_THRESHOLD = 3;  // hardcoded, not configurable
const SCM_FAILURE_COUNT_MAX = 1_000_000;  // handles legacy overflow from bd-ara.2
```

Kill condition requires BOTH:
- `agentDead=true`
- `scmFailureCount >= SCM_FAILURE_THRESHOLD`

Counter increments:
- max 2 per poll cycle (Step 3 detectPR catch + Step 4 PR state catch)
- resets to 0 on ANY successful SCM call

### Six contributing causes after SCM death

1. **Worker liveness not verified tightly enough** — `tmux has-session` returns alive even when agent CLI has exited. Correct probe: `tmux capture-pane -t <session> -p | tail -25`
2. **Dead-shell panes treated as live ownership** — loop rechecked too slowly on troubled lanes
3. **Retask delivery not fail-closed** — dead workers received prompts as bash input
4. **Prompts stale or too generic** — older workers spent time on setup/conflict exploration
5. **AO/tmux session identity drift** — ownership looked healthier than it was
6. **Slow recheck on troubled lanes** — dead-shell panes accumulated cycles before detection

### Fix options identified

| Option | Approach | Risk |
|--------|----------|------|
| A | Increase SCM_FAILURE_THRESHOLD | Band-aid — delays kill, doesn't fix auth |
| B | Fix GitHub auth (correct root cause) | Token expired/revoked for worldarchitect |
| C | Add auth retry to ghWithRetry | Reduces single 401 from killing session |
| D | Make threshold configurable per project | Doesn't fix auth either |
| E | Kill-session reaper speedup | Process-level, not auth-level |

## Source evidence

- `/Users/jleechan/.agent-orchestrator/953501c04ccc-worldarchitect.ai/sessions/archive/wa-1417_2026-04-21T22-01-54-578Z`
- `/Users/jleechan/.agent-orchestrator/953501c04ccc-worldarchitect.ai/sessions/archive/wa-1419_2026-04-21T22-25-23-944Z`
- `/Users/jleechan/.agent-orchestrator/953501c04ccc-worldarchitect.ai/sessions/archive/wa-1427_2026-04-21T22-40-24-213Z`
- `/Users/jleechan/.claude/projects/-Users-jleechan-project-agento-agent-orchestrator/memory/feedback_2026-04-21_ao_worker_dead_shell_degradation.md`
- `packages/core/src/lifecycle-manager.ts` lines 593-907

## Connections

- [[lifecycle-manager]] — source of the kill logic and SCM failure tracking
- [[scm-github]] — the SCM plugin whose auth failures killed the workers
- [[AO Worker Degradation]] — the symptom (dead LLM, live tmux pane)
- [[bd-i9o]] — P0 bead: ao send must detect dead agent CLI and restart before pasting
- [[bd-r7hg]] — P1 bead: investigate and tune SCM_FAILURE_THRESHOLD

## Lesson

For AO-managed PR closure, spawn success is not enough. The system must verify: (1) actual agent type after launch; (2) actual liveness after retask using `tmux capture-pane | tail -25` not `tmux has-session`; (3) actual PR ownership continuity in session history. The death cause is GitHub auth failure, not model or agent instability.
