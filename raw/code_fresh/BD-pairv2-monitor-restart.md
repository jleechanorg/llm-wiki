# BD-pairv2-monitor-restart

## ID
BD-pairv2-monitor-restart

## Title
pairv2: monitor restarts stuck agents instead of killing the whole flow

## Status
closed

## Type
feature

## Priority
high

## Created
2026-02-23

## Description
When an agent (coder or verifier) stalls (no log activity for 600s), the workflow
currently returns `session_status=timeout` and ends with FAIL. Per the LLM-recoverable
tenet, a stuck agent should be restarted while preserving the workspace.

## Architecture

There are TWO places where agent stalls are detected:

1. `_wait_for_implementation_ready_node` (line ~1692) — waits for CODER to finish
   - Currently: simple poll loop with wall-clock timeout → FAIL
   - Change: detect coder stall by log mtime, restart coder, continue waiting

2. `_wait_for_live_completion` (line ~2615) — waits for VERIFIER to finish
   - Currently: heartbeat stall (600s no log) → `session_status=timeout`
   - Change: detect which agent is stuck, restart it, continue waiting

## Design

### New helper: `_restart_agent(session_dir, agent_key, tmux_socket) -> bool`

```
1. Read session_info.json to get agent name, current pgid, and launch config
2. Kill old tmux session: tmux -L {socket} kill-session -t {agent_name}
3. Kill old process group: os.killpg(pgid, SIGKILL)
   *** BLOCKER FIX: Clear pgid from session_info immediately after kill.
       Do NOT keep stale pgid — next restart could target wrong process group.
       If pgid is unknown (0 or missing), skip killpg entirely.
4. Clean stale result files: remove {agent}_results_*.json from orchestration_results/
5. Re-read the saved instructions file:
   - Coder: session_dir / "coder_instructions.txt"
   - Verifier: session_dir / "verifier_instructions.txt"
6. Append restart-aware prompt suffix (see below)
7. Re-launch via TaskDispatcher.create_dynamic_agent() with SAME config:
   *** BLOCKER FIX: Read launch config from session_info.json, NOT hardcoded.
       Use: forced_cli, model, no_worktree, start_dir, workspace_config
       These must be persisted at initial launch time (see step in _launch_coder_only).
   - tmux socket, workspace root, session dir, instructions, artifact contract
   *** BLOCKER FIX: artifact_paths in session_info.json is a dict, not a string.
       Accept both dict and str: isinstance(v, dict) → use directly, isinstance(v, str) → json.loads
       Catch TypeError AND JSONDecodeError.
8. Update session_info.json:
   - Clear old pgid: set {agent_key}_pgid = 0
   - Increment {agent_key}_restart_count
   - Preserve all other fields
9. Return True if launch succeeded
```

### Persist launch config in `_launch_coder_only`

At initial launch, save to session_info.json:
```python
session_info["coder_launch_config"] = {
    "forced_cli": state["coder_cli"],
    "model": state["coder_model"] or None,
    "no_worktree": state["no_worktree"],
    "start_dir": str(shared_workspace) if shared_workspace else None,
    "workspace_config": base_workspace,
}
session_info["verifier_launch_config"] = {
    "forced_cli": state["verifier_cli"],
    "model": state["verifier_model"] or None,
    "no_worktree": state["no_worktree"],
}
```

### Restart in `_wait_for_implementation_ready_node`

```python
coder_restart_count = 0
last_restart_time = 0.0  # monotonic timestamp of last restart
RESTART_GRACE_SECONDS = 60  # wait 60s after restart before checking stall again

while True:
    # ... existing signal file check + tmux liveness check ...

    # Stall detection: coder log hasn't been written in STALL_SECONDS
    # *** BLOCKER FIX: Skip stall check during grace period after restart
    now_mono = time.monotonic()
    if last_restart_time > 0 and (now_mono - last_restart_time) < RESTART_GRACE_SECONDS:
        pass  # grace period — don't check stall yet
    elif tmux_socket and coder_agent:
        coder_log_mt = _agent_log_last_mtime(session_dir, coder_agent, 0)
        if coder_log_mt > 0:
            time_since_log = time.time() - coder_log_mt
            if time_since_log > PAIRV2_AGENT_STALL_SECONDS:
                if coder_restart_count < PAIRV2_MAX_AGENT_RESTARTS:
                    if _restart_agent(session_dir, "coder_agent", tmux_socket):
                        coder_restart_count += 1
                        last_restart_time = now_mono  # start grace period
                        continue  # keep waiting
                # else fall through to timeout
```

### Restart in `_wait_for_live_completion`

Same pattern but for both agents independently, with per-agent grace periods:
```python
coder_restart_count = 0
verifier_restart_count = 0
coder_last_restart = 0.0
verifier_last_restart = 0.0

# In the heartbeat stall block (line ~2776):
# Instead of returning timeout, check which agent is stuck

# Skip agents in grace period
coder_in_grace = coder_last_restart > 0 and (now - coder_last_restart) < RESTART_GRACE_SECONDS
verifier_in_grace = verifier_last_restart > 0 and (now - verifier_last_restart) < RESTART_GRACE_SECONDS

coder_stalled = not coder_in_grace and coder_agent and (now - coder_last_activity) > PAIRV2_AGENT_STALL_SECONDS
verifier_stalled = not verifier_in_grace and verifier_agent and (now - verifier_last_activity) > PAIRV2_AGENT_STALL_SECONDS

if coder_stalled and coder_restart_count < PAIRV2_MAX_AGENT_RESTARTS:
    if _restart_agent(session_dir, "coder_agent", tmux_socket):
        coder_restart_count += 1
        coder_last_restart = now
        last_log_activity = now  # reset heartbeat
if verifier_stalled and verifier_restart_count < PAIRV2_MAX_AGENT_RESTARTS:
    if _restart_agent(session_dir, "verifier_agent", tmux_socket):
        verifier_restart_count += 1
        verifier_last_restart = now
        last_log_activity = now

# Only return timeout if restarts exhausted AND still stalled (no grace)
all_restarts_exhausted = (
    (not coder_stalled or coder_restart_count >= PAIRV2_MAX_AGENT_RESTARTS) and
    (not verifier_stalled or verifier_restart_count >= PAIRV2_MAX_AGENT_RESTARTS)
)
if all_restarts_exhausted and (coder_stalled or verifier_stalled):
    return {"session_status": "timeout", "message": "restarts exhausted, agents still stalled"}
```

### session_info.json management

On restart:
- Clear `{agent_key}_pgid` to 0 (prevent stale pgid targeting wrong process)
- Increment `{agent_key}_restart_count` field
- Preserve all other fields (tmux_socket, workspace paths, artifact contract, launch config)

### Restart-aware prompt suffix

Append to the agent's instructions on restart:
```
RESTART NOTICE: You are restarting after a previous attempt stalled.
The workspace at {shared_workspace} already has files from the prior attempt.
DO NOT start from scratch. First:
1. Run tests to see what state the code is in: python -m pytest -v
2. Inspect what files exist and what has changed
3. Then continue from where the previous attempt left off.
```

## Scope
- `.claude/pair/pair_execute_v2.py`:
  - New: `_restart_agent(session_dir, agent_key, tmux_socket) -> bool`
  - Modified: `_wait_for_implementation_ready_node` — add coder stall detection + restart with grace period
  - Modified: `_wait_for_live_completion` — replace heartbeat timeout with per-agent restart with grace period
  - Modified: `_launch_coder_only` — save coder_instructions.txt AND launch config to session_info.json
- `.claude/pair/tests/test_pair_v2.py`:
  - New test: `test_wait_node_restarts_stalled_coder`
  - New test: `test_restart_agent_kills_and_relaunches`
  - New test: `test_restart_max_count_then_timeout`
  - New test: `test_restart_grace_period_prevents_thrash`

## Constants
- `PAIRV2_AGENT_STALL_SECONDS = 300` — stall detection threshold (5 min)
- `PAIRV2_MAX_AGENT_RESTARTS = 3` — max restarts per agent per cycle
- `PAIRV2_RESTART_GRACE_SECONDS = 60` — grace period after restart before re-checking stall

## Blocker Fixes (from paircodex review)
- [x] B1: `artifact_paths` type safety — accept both dict and str, catch TypeError
- [x] B2: Preserve original CLI/model/worktree settings — persist launch config in session_info.json
- [x] B3: Grace period after restart to prevent thrash — 60s window before re-checking stall
- [x] B4: Clear stale pgid after kill — set to 0, never keep stale pgid

## Acceptance
- [x] `_restart_agent` helper: kills tmux + pgid, cleans results, re-launches via TaskDispatcher
- [x] `_restart_agent` handles artifact_paths as both dict and str (B1)
- [x] Launch config persisted in session_info.json and reused on restart (B2)
- [x] Grace period (60s) after restart prevents thrash (B3)
- [x] Stale pgid cleared to 0 after kill (B4)
- [x] Coder stall detected in `_wait_for_implementation_ready_node` by log mtime
- [x] Verifier stall detected in `_wait_for_live_completion` by individual log mtime
- [x] Only stuck agent restarted, other agent untouched
- [x] Workspace and session_info.json preserved across restart
- [x] Restarted agent gets restart-aware prompt suffix (with "run tests first")
- [x] Max 3 restarts per agent; timeout only after exhausted
- [x] Stale result files cleaned before re-launch
- [x] coder_instructions.txt saved by `_launch_coder_only`
- [x] Tests: stall → restart → success, grace period prevents thrash, max restarts → timeout
