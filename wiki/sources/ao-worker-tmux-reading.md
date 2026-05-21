# AO Worker Tmux Reading: Idle Between Turns ≠ Frozen

**Ingested**: 2026-05-14
**Source**: `feedback_2026-05-14_ao_worker_idle_not_stuck.md`

## Core Rule

AO workers are turn-based, not autonomous loops. The orchestrator sends a prompt → worker executes tools → worker waits for NEXT orchestrator prompt. Between-turn idle at `❯` is healthy, not frozen.

## Tmux Liveness Check (Non-Invasive)

```bash
tmux list-panes -t <prefix>-ha-N -F '#{pane_pid} #{pane_current_command}'
# "<PID> claude.exe" = alive and idle
# "pane not found" = worker exited
```

## Scrollback Reading

```bash
tmux capture-pane -t <prefix>-ha-N -p -S -30
```

### What scrollback means:
1. `[Tool use: ...]` lines = worker actively executing (healthy)
2. Summary text ("I pushed...", "All checks pass...") = turn completed (healthy idle next)
3. `❯` with pre-filled text = between-turn idle (NOT a bug)
4. Stack trace / error / Python exception = actual problem
5. Empty/blank after long wait = possible hang (check pane_current_command first)

### What NOT to conclude:
- "Worker is stuck at prompt" → it's waiting for next orchestrator prompt
- "Pre-filled text failed to submit" → it's a suggestion, not a failed action
- "No new tool calls = broken" → between-turn idle is expected
- "I should kill this worker" → unless you see errors, leave it alone

## Session Prefix

Hermes-agent: `953501c04ccc-ha-N` (sessionPrefix `ha` + config hash)

## Key Commands

- `ao open <session>` — opens session in terminal tab (no `ao attach` exists)
- `ao send <session> "<prompt>"` — sends next prompt to idle worker

## References

- Session: 3dc1a846-12b5-462e-80b4-5f73dfdf1172
- PRs: [#4](https://github.com/jleechanorg/hermes-agent/pull/4), [#11](https://github.com/jleechanorg/hermes-agent/pull/11), [#12](https://github.com/jleechanorg/hermes-agent/pull/12)
