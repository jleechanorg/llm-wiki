---
title: "Stale Process Group Targeting"
type: concept
tags: [agent-orchestration, process-management, race-condition, pair-programming]
sources: []
last_updated: 2026-04-11
---

## Description
When restarting a stalled agent in an orchestration loop, the old process group ID (PGID) must be cleared immediately after killing it. If PGID is not cleared, subsequent restarts may target the wrong process group — potentially killing unrelated processes that inherited that PGID.

## Symptoms
- Agent restart kills unrelated processes
- Session state corrupted between restart cycles
- Non-deterministic behavior on retry

## Root Cause
The restart sequence:
1. Read session_info.json for old PGID
2. Kill old process via `os.killpg(pgid, SIGKILL)`
3. Re-launch new agent

If step 3 fails or step 2's kill is delayed, a new process may be assigned the same PGID. When step 1 runs again (next restart), it kills the wrong process.

## Fix
Clear PGID immediately after kill — before the kill completes:
```python
# Order matters: clear PGID BEFORE kill, not after
session_info[f"{agent_key}_pgid"] = 0
try:
    os.killpg(pgid, SIGKILL)
except ProcessLookupError:
    pass  # already dead, that's fine
```

Also: check if PGID is 0 or missing before attempting kill — skip killpg if unknown.

## Connections
- [[TmuxBasedAgentOrchestration]] — tmux session management for agent restarts
- [[DeterministicFeedbackLoops]] — restart loop without stale state
