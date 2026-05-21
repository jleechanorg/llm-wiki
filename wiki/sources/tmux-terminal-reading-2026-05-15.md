# Tmux Terminal Reading: Bottom-Up, Never From Stale Scrollback

**Source**: `~/.claude/projects/-Users-jleechan--hermes/memory/feedback_2026-05-15_tmux_terminal_reading.md`
**Date**: 2026-05-15
**Classification**: Critical

## Core Rule

Read tmux panes BOTTOM-UP; never diagnose from stale scrollback.

AO workers are turn-based. The `❯` prompt at the bottom of a pane means idle-between-turns, not frozen.

## Reading Protocol

1. **Bottom line is truth.** Last visible line determines state:
   - `❯` alone = idle, healthy
   - `❯ <text>` = idle, CLI suggesting next input
   - `<command output>` (no prompt) = actively executing
   - `❯ <text>` with error above = previous turn's error, already handled

2. **Use `tmux capture-pane` correctly:**
   - `tmux capture-pane -t <pane> -p` — current visible content
   - `tmux capture-pane -t <pane> -p -S -50` — last 50 lines of scrollback

3. **Verify process liveness via `ps`, not scrollback.**

4. **Distinguish old errors from current errors:** Scrollback shows ALL output. An error 50 lines up is from a PREVIOUS turn. If `❯` is present after the error, the worker already completed that turn.

## Anti-Patterns

- Don't grep scrollback for "error" — you'll find old, already-handled errors
- Don't assume no output = frozen — between turns, there IS no output
- Don't kill based on scrollback — always check process liveness
- Don't re-send prompts based on pre-filled text — that's CLI autocomplete

## Impact

9+ incorrect "frozen" diagnoses across a babysit loop caused unnecessary kill recommendations for healthy workers.

## Related

- [[FileBasedHandoffs]] — state persistence between agent restarts
- [[ContextAnxiety]] — premature wrap-up as context fills
