---
title: "Agent Stall Recovery"
type: concept
tags: [pairv2, recovery, restart]
sources: []
last_updated: 2026-02-23
---

## Definition

Agent Stall Recovery is a pattern where a workflow detects when an agent (coder or verifier) has stalled (no log activity for a threshold period) and restarts it while preserving the workspace, rather than failing the entire workflow. The restart uses a grace period to avoid thrashing.

## Architecture

Two detection points in pair_execute_v2:

1. `_wait_for_implementation_ready_node` — detects coder stall by log mtime polling
2. `_wait_for_live_completion` — detects individual agent stalls via heartbeat monitoring

### Restart Helper: `_restart_agent(session_dir, agent_key, tmux_socket) -> bool`

1. Read session_info.json for agent name, pgid, and launch config
2. Kill old tmux session: `tmux -L {socket} kill-session -t {agent_name}`
3. Kill old process group: `os.killpg(pgid, SIGKILL)`
4. Clean stale result files from `orchestration_results/`
5. Re-read saved instructions file
6. Append restart-aware prompt suffix
7. Re-launch via `TaskDispatcher.create_dynamic_agent()` with same config
8. Update session_info.json: clear pgid, increment restart_count

### Critical Fixes

- **Stale pgid clearing**: Set pgid to 0 immediately after kill to prevent targeting wrong process on next restart
- **Grace period**: 60 seconds after restart before re-checking stall to prevent thrash
- **Launch config persistence**: CLI/model/worktree settings saved at initial launch and reused on restart

## Constants

- `PAIRV2_AGENT_STALL_SECONDS = 300` — stall detection threshold (5 min)
- `PAIRV2_MAX_AGENT_RESTARTS = 3` — max restarts per agent per cycle
- `PAIRV2_RESTART_GRACE_SECONDS = 60` — grace period after restart

## Interaction with Verify-Fail-Retry

These are orthogonal recovery paths:
- Stall → restart same agent with same task (hang recovery)
- FAIL → restart coder with NEW feedback (wrong code recovery)

Both share `_restart_agent` mechanics but with different prompt suffixes.

## Sources

- BD-pairv2-monitor-restart: full implementation of stall detection and restart
