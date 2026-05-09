# OpenCode TUI vs run subcommand flag split

**Date**: 2026-05-07
**Type**: Anti-Pattern / feedback
**Source**: ~/.claude/projects/-Users-jleechan-projects-worktree-wafer/memory/feedback_2026-05-07_opencode-tui-run-flag-split.md

## Summary

`--dangerously-skip-permissions` is accepted only by `opencode run`, not by the TUI invocation (`opencode [project]`). Passing it to the TUI causes opencode to print help and exit silently with no error.

## Rule

- TUI: `opencode --model wafer.ai/GLM-5.1 .`
- Non-interactive: `opencode run --model wafer.ai/GLM-5.1 --dangerously-skip-permissions "message"`

## Diagnosis method

Use tmux + `tmux capture-pane` to observe TUI behavior. If opencode prints help and shell prompt returns immediately, an unrecognized global flag is the cause.

## jeffrey-oracle

Does not affect `[[jeffrey-oracle]]` — tool-specific CLI flag behavior.
