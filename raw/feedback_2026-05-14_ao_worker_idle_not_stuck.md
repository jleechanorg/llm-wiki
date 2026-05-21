---
name: ao-worker-idle-not-stuck
description: "AO workers between turns are idle (waiting for orchestrator prompt), NOT frozen or stuck. Includes tmux reading technique."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3dc1a846-12b5-462e-80b4-5f73dfdf1172
---

AO workers are turn-based, not autonomous loops. The orchestrator sends a prompt → worker executes tools → worker waits for NEXT orchestrator prompt. Text at the `❯` prompt is a pre-filled suggestion, not a failed submission.

**Why:** Across 9 babysit loop iterations I incorrectly called workers "frozen at prompt" and recommended killing them. They had completed their turn and were correctly waiting for the next prompt. "No new tool calls" between turns is expected idle, not a bug.

**How to apply:** When checking AO worker liveness, distinguish between:
- **Between turns** (normal): worker completed tool calls, printed summary, waiting at `❯` prompt — this is healthy idle
- **Actually stuck** (problem): worker mid-tool-call with no output for extended time, or error state
- **Pre-filled text at ❯** is a suggestion for the NEXT prompt, not evidence of a "prompt-loop bug"

## Tmux terminal reading technique for AO workers

**Liveness check (non-invasive):**
```bash
# Check pane exists and process is running
tmux list-panes -t <session-prefix>-ha-N -F '#{pane_pid} #{pane_current_command}'
# Expected: "<PID> claude.exe" or "<PID> claude" = alive and idle
# If "pane not found" → worker exited
```

**Scrollback reading (diagnostic, not for liveness):**
```bash
# Read last 30 lines of scrollback
tmux capture-pane -t <session-prefix>-ha-N -p -S -30
```

**What the scrollback tells you:**
1. Lines with `[Tool use: ...]` = worker actively executing — healthy
2. Lines with summary text ("I pushed...", "All checks pass...") = worker completed turn — healthy idle next
3. `❯` with pre-filled text = between-turn idle, NOT a bug
4. Stack trace / error / Python exception = actual problem
5. Empty/blank after long wait = possible hang, but check `pane_current_command` first

**What NOT to conclude from scrollback:**
- "The worker is stuck at the prompt" → it's waiting for the next orchestrator prompt
- "The pre-filled text failed to submit" → it's a suggestion, not a failed action
- "No new tool calls = broken" → between-turn idle is expected
- "I should kill this worker" → unless you see errors, leave it alone

**Session prefix:** Hermes-agent project uses `953501c04ccc-ha-N` (derived from `agent-orchestrator.yaml` sessionPrefix `ha` + config hash).

**Relevant commands:**
- `ao open <session>` — opens session in a new terminal tab (no `ao attach` exists)
- `ao send <session> "<prompt>"` — sends next prompt to idle worker
