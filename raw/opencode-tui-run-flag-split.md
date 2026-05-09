---
name: OpenCode TUI vs run subcommand flag split
description: --dangerously-skip-permissions is run-only; passing it to TUI invocation causes silent help-exit; TUI uses opencode -m model .
type: feedback
bead: none
---

Do not pass `--dangerously-skip-permissions` to the bare `opencode [project]` (TUI) invocation.

**Why:** `--dangerously-skip-permissions` is only accepted by `opencode run`. When passed to the TUI mode (`opencode .`), opencode interprets it as an unrecognized global flag, prints full help, and exits — no error message, just silent exit. Diagnosed via tmux: TUI launched, help printed, shell prompt returned.

**How to apply:** When writing any wrapper around opencode, split on TUI vs run:
- TUI: `opencode --model provider/model [path]` — NO `--dangerously-skip-permissions`
- Non-interactive: `opencode run --model provider/model --dangerously-skip-permissions [message]`

Also: model name for TUI must use `provider/model` format (e.g. `wafer.ai/GLM-5.1`), not bare `GLM-5.1`.
