---
name: Codex slash autocomplete proof boundary
description: codex exec slash-command translation is not proof that the interactive Codex TUI autocomplete indexes a custom command.
type: feedback
bead: rev-tg5zj
---

# Codex Slash Autocomplete Proof Boundary

`codex exec --yolo` resolving a prompt that begins with `/code-standards` proves
model-side slash-command translation only. It does not prove the interactive
Codex TUI slash autocomplete indexes custom files under `~/.codex/commands` or
`~/.codex/prompts`.

In Codex CLI `0.128.0`, fresh interactive TUI and tmux tests showed only
built-ins in the native slash menu:

- `/model`
- `/fast`
- `/permissions`
- `/keymap`
- `/experimental`
- `/autoreview`
- `/memories`
- `/skills`

Typing `/code-standards` left it as plain prompt text and did not show an
autocomplete match. Enabling `external_migration = true` in
`/Users/jleechan/.codex/config.toml` did not change the behavior.

Rule: for Codex slash-command UX work, verify autocomplete in a real TUI session,
preferably with tmux capture. Do not use `codex exec` as native autocomplete
evidence.

References:

- `https://github.com/jleechanorg/worldarchitect.ai/pull/7116`
- `https://developers.openai.com/codex/cli/slash-commands`
- `https://github.com/openai/codex/issues/15941`
- `https://github.com/openai/codex/issues/9848`
- `https://github.com/openai/codex/issues/3641`
