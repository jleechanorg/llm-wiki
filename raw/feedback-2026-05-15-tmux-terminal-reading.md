---
name: tmux-terminal-reading
description: "How to properly read AO worker tmux panes — distinguish idle, active, and error states; avoid stale scrollback misdiagnosis"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3dc1a846-12b5-462e-80b4-5f73dfdf1172
---

## Rule: Read tmux pane BOTTOM-UP; never diagnose from stale scrollback

AO workers are turn-based. The `❯` prompt at the bottom of a pane means idle-between-turns, not frozen.

**Why:** Across 9+ babysit loops, scrollback from previous turns was misread as "frozen" or "errored", leading to kill recommendations for healthy workers. Pre-filled text at `❯` is the CLI's suggestion for the NEXT prompt — not a failed submission.

**How to apply:**

### Reading a tmux pane correctly

1. **Bottom line is truth.** Look at the very last line of the visible pane:
   - `❯` (clean prompt, no text after it) = idle, healthy, waiting for next turn
   - `❯ <text>` (prompt with pre-filled text) = idle, CLI suggesting next input — NOT stuck
   - `<command output>` (no prompt visible) = actively executing a command
   - `❯ <text>` with error output above = previous turn's error, already handled by the worker

2. **Use `tmux capture-pane` correctly:**
   ```bash
   # Current visible content only (what's on screen right now)
   tmux capture-pane -t <pane> -p

   # Full scrollback history (use sparingly — can be huge)
   tmux capture-pane -t <pane> -p -S -

   # Last N lines of scrollback
   tmux capture-pane -t <pane> -p -S -50
   ```

3. **Verify process liveness (don't trust scrollback):**
   ```bash
   # Is the claude process still alive?
   ps -p $(tmux list-panes -t <session> -F '#{pane_pid}')

   # Or check pane directly
   tmux list-panes -t <session> -F '#{pane_pid} #{pane_current_command}'
   ```

4. **Distinguish old errors from current errors:**
   - Scrollback shows ALL output since pane creation
   - An error 50 lines up is from a PREVIOUS turn, already handled
   - Only errors on the LAST few lines (before the `❯` prompt) are current
   - If `❯` is present after the error, the worker already completed that turn

5. **Worker states reference:**
   | Visual state | Meaning | Action |
   |---|---|---|
   | `❯` alone at bottom | Idle between turns | Wait (normal) |
   | `❯ <text>` at bottom | CLI suggestion for next input | Wait (normal) |
   | Streaming output, no prompt | Worker actively executing | Wait |
   | `[Process exited]` | Worker process died | Investigate, possibly restart |
   | No pane found | tmux session gone | Check if session was cleaned up intentionally |

### Anti-patterns to avoid

- **Don't grep scrollback for "error"** — you'll find old, already-handled errors
- **Don't assume no output = frozen** — between turns, there IS no output
- **Don't kill based on scrollback** — always check if the process is still alive via `ps`
- **Don't re-send prompts based on pre-filled text** — that's the CLI's autocomplete, not a failed command

### Related

- [[ao_worker_idle_not_stuck]] — the original learning that idle ≠ frozen
- AO session prefix: `953501c04ccc-ha-N` (check via `tmux list-sessions`)
